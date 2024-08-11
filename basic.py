'''
Description:[系统调用第三方接口文件]
Author:[huan666]
Date:[2024/05/28]
'''
# shodan查询模块
import shodan
from config import shodankey
import queue
import subprocess 

# icp备案查询
from fake_useragent import UserAgent
import random


# 高德地图
from config import amap_key_list


# 通用模块
import re
import json
import os
import base64
import requests
from bs4 import BeautifulSoup
import time


# IP属性判断
from config import cloudserver
from config import exitaddress
from config import hotspot
from config import datacenter


# fofa 通过ip查询域名
from config import fofaemail
from config import fofakey
from config import fofanum


# 提取根域名
import tldextract  


# 指纹自定义列表
from config import finger_list

# MySQL操作模块
import pymysql
from config import dict
from config  import rule_options


# 根据规则分别存入不同的文件
from config import Shiro_rule
from config import SpringBoot_rule
from config import weblogic_rule
from config import struts2_rule

# 磁盘读写
import psutil

import sys

# IP基础信息端口查询通过fofa+shodan
def shodan_api(ip):

    apis = shodan.Shodan(shodankey)

    # fofa接口
    fofa_first_argv= 'ip=' + ip + ''
    fofa_first_argv_utf8 = fofa_first_argv.encode('utf-8')
    fofa_first_argv_base64=base64.b64encode(fofa_first_argv_utf8)
    fofa_argv_str=str(fofa_first_argv_base64,'utf-8')
    url = "https://fofa.info/api/v1/search/all?email="+fofaemail+"&key="+fofakey+"&size="+fofanum+"&qbase64="
    hearder={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }

    try:
        result = apis.host(ip)
    except:
        pass
    try:
        # shodan接口
        port = result['ports']
        port_list = []
        for ii in port:
            port_list.append(ii)
        if len(port_list) == 0:
            port_list.append("NULL")

        # fofa接口
        res = requests.get(url+fofa_argv_str,headers=hearder,allow_redirects=False)
        res.encoding='utf-8'
        restext = res.text
        resdic=json.loads(restext)
        resdicresult=resdic['results']
        fofa_port_list = []
        for ki in resdicresult:
            fofa_port_list.append(ki[2])
        
        fofa_port_list_uniq = list(set(fofa_port_list))
        if len(fofa_port_list_uniq) == 0:
            fofa_port_list_uniq.append("NULL")
        
        # 列表元素转int型
        fofa_port_list_uniq_int = []
        for inti in fofa_port_list_uniq:
            fofa_port_list_uniq_int.append(int(inti))

        # fofa+shodan列表组合并去重
        total_list = list(set(fofa_port_list_uniq_int+port_list))

        return total_list
        
    except:
        pass



# 从目标url中提取ip地址并存到列表
def url_convert_ip():
    url_list = []
    file = open("/TIP/batch_scan_domain/url.txt",encoding='utf-8')
    for line in file.readlines():
        url_list.append(line.strip())
    
    # 正则表达式匹配IPv4地址  
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')  
  
    # 提取IP地址  
    ip_addresses = []  
    for url in url_list:  
        # 使用findall方法找到所有的匹配项  
        matches = ip_pattern.findall(url)  
        for match in matches:  
            # 添加到结果列表中（这里我们假设每个URL只有一个IP地址）  
            ip_addresses.append(match) 
    return ip_addresses



# 目标url文件存入列表并返回
def url_file_ip_list():
    url_list = []
    file = open("/TIP/batch_scan_domain/url.txt",encoding='utf-8')
    for line in file.readlines():
        url_list.append(line.strip())
    return url_list


# 列表存入到队列中用于nmap扫描
def ip_queue_nmap():
    # 创建一个空队列
    q = queue.Queue()
    ip_list = url_convert_ip()
    for item in ip_list:
        q.put(item)
    # 取出并打印队列中的所有元素（先进先出）  
    while not q.empty():  
        ip_queue = q.get()
        result = subprocess.run(["sh", "./finger.sh","nmap_port",ip_queue], stdout=subprocess.PIPE) 

 
 # 生成一个随机的IPv4地址防止封禁IP  
def generate_random_ip():  
    return '.'.join(str(random.randint(0, 255)) for _ in range(4)) 


# icp备案查询公司名称
def icp_info(ip):
    UA = UserAgent()
    url = "https://icp.chinaz.com/"
    hearder = {
        'Cookie':'cz_statistics_visitor=47200924-88b7-cc6f-e817-6e3d3d76af1c; pinghost=pay.it.10086.cn; Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1707096410,1707902350; _clck=5gzbp1%7C2%7Cfj9%7C0%7C1496; qHistory=Ly9taWNwLmNoaW5hei5jb20vX+e9keermeWkh+ahiOafpeivol/np7vliqh8Ly9pY3AuY2hpbmF6LmNvbS9f572R56uZ5aSH5qGI5p+l6K+i; JSESSIONID=B525D76194927A260AC9E9C0B72B44D2; Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1707902454; _clsk=1hj5on3%7C1707902455070%7C6%7C0%7Cw.clarity.ms%2Fcollect',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent':UA.random,
        'Host':'icp.chinaz.com',
        'X-Forwarded-For': generate_random_ip()
        }
    #历史URL列表
    domain_value = domain_scan(ip)
    
    # 提取带域名后缀以cn或者com的列表，过滤掉IP的URL
    domain_list = []
    for ii in domain_value:
        if 'cn' in ii or 'com' in ii:
            domain_list.append(ii)
    
    # 列表去重
    try:
        domain_list_uniq = list(set(domain_list))
    except:
        pass

    icp_name_list = []
    if len(domain_list_uniq) == 0:
        icp_name_list.append("None")
    else:
        try:
            for jii in domain_list_uniq:
                res = requests.get(url+str(jii),headers=hearder,allow_redirects=False)
                res.encoding = 'utf-8'
                soup=BeautifulSoup(res.text,'html.parser')
                soup_td = soup.find_all('td')
                icp_name = soup_td[25].text
                icp_name_list.append(icp_name)
        except:
            icp_name_list.append("None")
    icp_name_list_uniq = list(set(icp_name_list))
    return icp_name_list_uniq


# 网站标题
def title_scan(url_list):
    hearder={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    url_title_list = []

    if len(url_list) == 0:
        url_title_list.append("None")
    else:
        
        for url in url_list:
            try:
                # 忽略 SSL 验证，可以使用 Session 对象来避免重复设置 verify=False
                session = requests.Session()  
                session.verify = False
                res = session.get(url,headers=hearder,allow_redirects=False)
            except:
                url_title_list.append("请求出错")
            try:
                res.encoding='utf-8'
                title_1 = re.findall("<title>.*</title>",res.text)
                title_11 = title_1[0]
                title_2 = title_11.replace("<title>","")
                titleinfo = title_2.replace("</title>","")
                url_title_list.append(titleinfo)
            except:
                pass
    return url_title_list
            



# 调用高德地图接口查询公司位置信息
def amapscan(company_list_list):
    key = random.choice(amap_key_list)
    hearder={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
    company_location_list = []
    if len(company_list_list) == 0:
        company_location_list.append("None")
    else:
        try:
            for company in company_list_list:
                # 判断公司名为空时公司位置直接返回空
                if company == "None":
                    company_location_list.append("None")
                else:
                    url = "https://restapi.amap.com/v3/place/text?keywords="+company+"&offset=20&page=1&key="+key+"&extensions=all"
                    res = requests.get(url,headers=hearder,allow_redirects=False)
                    res.encoding='utf-8'
                    restext = res.text
                    resdic=json.loads(restext)
                    companylocation = resdic['pois'][0]['address']
                    company_location_list.append(companylocation)
        except:
            company_location_list.append("None")
    company_location_list_uniq = list(set(company_location_list))
    return company_location_list_uniq
      
    

# 基于证书查询子域名
def subdomain_scan(domain):
    url = "https://crt.sh/?q="
    hearder={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    try:
        res = requests.get(url+domain,headers=hearder,allow_redirects=False)
        res.encoding='utf-8'
        restext = res.text
        domain  = re.findall("<TD>.*</TD",restext)
        subdomain_list = []
        for ii in domain:
            if "com" in ii or "cn" in ii:
                subdomain_list.append(ii)
        subdomain_list_result = list(set(subdomain_list))
        subdomain_list_result_1 = []
        for jj in subdomain_list_result:
            if "<BR>" not in jj:
                jj1 = jj.replace("<TD>","")
                jj2 = jj1.replace("</TD","")
                subdomain_list_result_1.append(jj2)
        subdomain_list_result_11 = []
        for kk in subdomain_list_result_1:
            if "<A" not in kk:
                subdomain_list_result_11.append(kk)
        return subdomain_list_result_11
    
    except:
        pass



# 指纹识别接口
def finger_scan(ip1):
    result = status_scan(ip1)
    finger_list = []
    for i in result:
        result = os.popen('bash ./finger.sh finger'+''+' '+i).read()
        #页面显示优化
        pattern = re.compile(r'\x1b\[[0-9;]*m')
        clean_text = pattern.sub('', result)
        clean_text_1 = clean_text.replace("|","")
        finger_list.append(clean_text_1)
    
    #清空列表为空的数据
    while '' in finger_list:
        finger_list.remove('')
    #列表为空返回None
    if len(finger_list) == 0:
        finger_list.append("None")
    
    return finger_list



# IP属性判断
def ipstatus_scan(ip):
    try:
        output = subprocess.check_output(["sh", "./finger.sh","location1",ip], stderr=subprocess.STDOUT)
        output_list = output.decode().splitlines()
        
        ip_list = []
        for ii in output_list:
            if "数据二" in ii:
                ip_list.append(ii)
        ip_list_status = ip_list[0]
        ip_status_list_result = []
       
        #云主机判断
        for a1 in cloudserver:
            if a1 in ip_list_status:
                ip_status_list_result.append("云服务器")
        
        #出口地址判断
        for a2 in exitaddress:
            if a2 in ip_list_status:
                ip_status_list_result.append("企业专线或家庭宽带")

        #手机热点
        for a3 in hotspot:
            if a3 in ip_list_status:
                ip_status_list_result.append("手机热点")

        #数据中心
        for a4 in datacenter:
            if a4 in ip_list_status:
                ip_status_list_result.append("数据中心")

        return ip_status_list_result[0]
    
    except:
        pass


# fofa查询模块通过IP反查域名
def domain_scan(ip):

    fofa_first_argv= 'ip=' + ip + ''
    fofa_first_argv_utf8 = fofa_first_argv.encode('utf-8')
    fofa_first_argv_base64=base64.b64encode(fofa_first_argv_utf8)
    fofa_argv_str=str(fofa_first_argv_base64,'utf-8')
    url = "https://fofa.info/api/v1/search/all?email="+fofaemail+"&key="+fofakey+"&size="+fofanum+"&qbase64="
    hearder={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }

    try:
        
        res = requests.get(url+fofa_argv_str,headers=hearder,allow_redirects=False)
        res.encoding='utf-8'
        restext = res.text
        resdic=json.loads(restext)
        resdicresult=resdic['results']
      
        fofa_list = []
        for i in resdicresult:
            matches1 = re.findall(r"(http(s)?://\S+)", i[0])
            for match in matches1:

                fofa_list.append(match)
        
        fofa_list_result = []
        for j in fofa_list:
            fofa_list_result.append(j[0])
        
        fofa_list_result_uniq = list(set(fofa_list_result))
        
        return fofa_list_result_uniq
    
    except:
        pass



# cdn识别
def cdnscan(domain):
    try:
        result = os.popen('bash ./finger.sh CDN_scan'+' '+domain).read()
    except:
        pass
    return result


# 根域名提取
def root_domain_scan(domain_list):
    try:
        root_domains = []  
        for url in domain_list:  
            extract = tldextract.extract(url)  
            root_domain = f"{extract.domain}.{extract.suffix}"
            root_domains.append(root_domain)
        return root_domains
    except:
        pass


# 提取状态码为200的url
def status_scan(ip1):

    domain_list = domain_scan(ip1)
    f = open(file='./result/domain.txt', mode='w')
    for k in domain_list:
        f.write(str(k)+"\n")
    f.close()

    #判断状态码为200的url
    output = subprocess.check_output(["sh", "./httpxstatus.sh"], stderr=subprocess.STDOUT)
    output_list = output.decode().splitlines()
    
    #提取带http关键字的字符串
    status_code_list = []
    for ii in output_list:
        if "http" in ii:
            status_code_list.append(ii)
    
    if len(status_code_list) == 0:
        status_code_list.append("None")

    return status_code_list


# fscan批量扫描
def batch_fscan_interface():
    ip_list = url_convert_ip()
    f = open(file='/TIP/info_scan/fscan_tool/ip.txt', mode='w')
    for k in ip_list:
        f.write(str(k)+"\n")
    f.close()
    try:
        os.popen('bash /TIP/info_scan/finger.sh startfscanprocess')
    except Exception as e:
            print("捕获到异常:", e)


# shiro漏洞扫描
def shiro_scan():
    # 清空上一次扫描结果
    os.popen('rm -rf /TIP/info_scan/result/shiro_vuln.txt')
    # 遍历url列表
    url_list = url_file_ip_list()
    try:
        for i in url_list:
            os.popen('bash /TIP/info_scan/finger.sh shiro_scan'+' '+str(i)+'')
    except Exception as e:
        print("捕获到异常:", e)



# 重点系统关键字列表，在config.py配置，用于过滤重点目标，并进行针对性扫描
# 2024.6.12优化
def key_point_tiqu():
    # 提取通过自定义列表过滤出的目标，并提取这些目标的关键字作为字典，存入列表中
    filter_list_result = []
   
    # 配置文件或者MySQL数据库
    if int(rule_options) == 1:
        key_rule_list = str(finger_list)
    elif int(rule_options) == 2:
        key_rule_list = select_rule()
    else:
        key_rule_list = ['参数只能为0/1']

    try:
        for i in key_rule_list:
            result = os.popen('bash /TIP/info_scan/finger.sh finger_filter_shell'+' '+i).read()
            filter_list_result.append(result)
    
    except Exception as e:
        print("捕获到异常:", e)

    try:
        f2 = open(file='/TIP/info_scan/result/finger_filter_text.txt', mode='w')
        for j in filter_list_result:
            j1 = j.replace("[","")
            j2 = j1.replace("]","")
            j3 = j2.replace("|","")
            f2.write(str(j3))
        f2.close()
    except Exception as e:
        print("捕获到异常:", e)
    
    try:
        filter_list_result_final = []
        f3 = open("/TIP/info_scan/result/finger_filter_text.txt",encoding='utf-8')
        for k in f3.readlines():
            #页面显示优化
            pattern = re.compile(r'\x1b\[[0-9;]*m')
            clean_text = pattern.sub('', k)
            clean_text_1 = clean_text.replace("\x1b38;2;237;64;35m ","")
            clean_text_2 = clean_text_1.replace(" \x1b0m","")
            filter_list_result_final.append(clean_text_2.strip())
            
    except Exception as e:
        print("捕获到异常:", e)

    finger_url_list_final = []
    for item in filter_list_result_final:
        url = item.split()[0]
        finger_url_list_final.append(url)
        finger_url_list_final_uniq = list(set(finger_url_list_final))
    return finger_url_list_final_uniq



# 重点资产数量
def key_point_assets_num(assets_finger_list):
    # 提取通过自定义列表过滤出的目标，并提取这些目标的关键字作为字典，存入列表中
    filter_list_result = []
    try:
        for i in assets_finger_list:
            result = os.popen('bash /TIP/info_scan/finger.sh finger_filter_shell'+' '+i).read()
            filter_list_result.append(result)
    except Exception as e:
        print("捕获到异常:", e)

    try:
        f2 = open(file='/TIP/info_scan/result/finger_filter_text.txt', mode='w')
        for j in filter_list_result:
            j1 = j.replace("[","")
            j2 = j1.replace("]","")
            j3 = j2.replace("|","")
            f2.write(str(j3))
        f2.close()
    except Exception as e:
        print("捕获到异常:", e)
    
    try:
        filter_list_result_final = []
        f3 = open("/TIP/info_scan/result/finger_filter_text.txt",encoding='utf-8')
        for k in f3.readlines():
            #页面显示优化
            pattern = re.compile(r'\x1b\[[0-9;]*m')
            clean_text = pattern.sub('', k)
            clean_text_1 = clean_text.replace("\x1b38;2;237;64;35m ","")
            clean_text_2 = clean_text_1.replace(" \x1b0m","")
            filter_list_result_final.append(clean_text_2.strip())
            
    except Exception as e:
        print("捕获到异常:", e)

    try:
        finger_url_list_final = []
        for item in filter_list_result_final:
            url = item.split()[0]
            finger_url_list_final.append(url)
    except:
        pass
    
    if len(finger_url_list_final) == 0:
        assets_len = 0
    else:
        finger_url_list_final_uniq = list(set(finger_url_list_final))
        assets_len = len(finger_url_list_final_uniq)
    
    return assets_len




# 识别重点资产存入文件
def key_point_assets_file(assets_finger_list):
    # 提取通过自定义列表过滤出的目标，并提取这些目标的关键字作为字典，存入列表中
    filter_list_result = []
    try:
        for i in assets_finger_list:
            result = os.popen('bash /TIP/info_scan/finger.sh finger_filter_shell'+' '+i).read()
            filter_list_result.append(result)
    except Exception as e:
        print("捕获到异常:", e)

    try:
        f2 = open(file='/TIP/info_scan/result/finger_filter_text.txt', mode='w')
        for j in filter_list_result:
            j1 = j.replace("[","")
            j2 = j1.replace("]","")
            j3 = j2.replace("|","")
            f2.write(str(j3))
        f2.close()
    except Exception as e:
        print("捕获到异常:", e)
    
    try:
        filter_list_result_final = []
        f3 = open("/TIP/info_scan/result/finger_filter_text.txt",encoding='utf-8')
        for k in f3.readlines():
            #页面显示优化
            pattern = re.compile(r'\x1b\[[0-9;]*m')
            clean_text = pattern.sub('', k)
            clean_text_1 = clean_text.replace("\x1b38;2;237;64;35m ","")
            clean_text_2 = clean_text_1.replace(" \x1b0m","")
            filter_list_result_final.append(clean_text_2.strip())
            
    except Exception as e:
        print("捕获到异常:", e)

    try:
        finger_url_list_final = []
        for item in filter_list_result_final:
            url = item.split()[0]
            finger_url_list_final.append(url)
    except:
        pass
    finger_url_list_final_uniq = list(set(finger_url_list_final))
    return finger_url_list_final_uniq



# fofa资产发现
def fofa_search_assets_service_lib(parameter,num_fofa):

    fofa_first_argv_utf8 = parameter.encode('utf-8')
    fofa_first_argv_base64=base64.b64encode(fofa_first_argv_utf8)
    fofa_argv_str=str(fofa_first_argv_base64,'utf-8')
    url = "https://fofa.info/api/v1/search/all?email="+fofaemail+"&key="+fofakey+"&size="+num_fofa+"&qbase64="
    hearder={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }

    try:
        
        res = requests.get(url+fofa_argv_str,headers=hearder,allow_redirects=False)
        res.encoding='utf-8'
        restext = res.text
        resdic=json.loads(restext)
        resdicresult=resdic['results']
      
        fofa_list = []
        for i in resdicresult:
            matches1 = re.findall(r"(http(s)?://\S+)", i[0])
            for match in matches1:

                fofa_list.append(match)
        
        fofa_list_result = []
        for j in fofa_list:
            fofa_list_result.append(j[0])
        
        fofa_list_result_uniq = list(set(fofa_list_result))
        
        # 遍历列表存入目标资产
        f = open(file='/TIP/batch_scan_domain/url.txt', mode='w')
        for k in fofa_list_result_uniq:
            f.write(str(k)+"\n")
        f.close()

        # 资产备份
        os.popen('cp /TIP/batch_scan_domain/url.txt /TIP/batch_scan_domain/url_back.txt')

        return len(fofa_list_result_uniq)
    
    except:
        pass


# 启动hydra弱口令扫描库文件
def start_hydra_lib(part):
    if int(part) == 1:
        try:
            os.popen('bash /TIP/info_scan/finger.sh mysql_weak_password')
        except Exception as e:
            print("捕获到异常:", e)
    elif int(part) == 2:
        try:
            os.popen('bash /TIP/info_scan/finger.sh ssh_weak_password')
        except Exception as e:
            print("捕获到异常:", e)
    elif int(part) == 3:
        try:
            os.popen('bash /TIP/info_scan/finger.sh ftp_weak_password')
        except Exception as e:
            print("捕获到异常:", e)
    elif int(part) == 4:
        try:
            os.popen('bash /TIP/info_scan/finger.sh redis_weak_password')
        except Exception as e:
            print("捕获到异常:", e)

    elif int(part) == 5:
        try:
            os.popen('bash /TIP/info_scan/finger.sh mssql_weak_password')
        except Exception as e:
            print("捕获到异常:", e)
    else:
        print("接收的参数为1-5")



# 重点资产中筛选规则查询
def select_rule():
    try:
        db= pymysql.connect(host=dict['ip'],user=dict['username'],  
        password=dict['password'],db=dict['dbname'],port=dict['portnum']) 
        cur = db.cursor()
        sql="select rule FROM rule_table"
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)
        list_result = []
        for i in list_data:
            list_result.append(i[0])
    except:
        list_result = ['MySQL连接失败']

    return list_result


# 筛选后资产状态查询
def assets_status_show():
    try:
        db= pymysql.connect(host=dict['ip'],user=dict['username'],  
        password=dict['password'],db=dict['dbname'],port=dict['portnum']) 
        cur = db.cursor()
        sql="SELECT status_value FROM status_table where id = 1"
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)
        status_value = []
        for i in list_data:
            status_value.append(i[0])
        status_value_result = status_value[0]
    except:
        status_value_result = "MySQL连接失败"
    return status_value_result


# 筛选后资产状态更新
def assets_status_update(part):
    try:
        db= pymysql.connect(host=dict['ip'],user=dict['username'],  
        password=dict['password'],db=dict['dbname'],port=dict['portnum']) 
        cur = db.cursor()
        sql="UPDATE status_table SET status_value = '%s' WHERE id = 1"%(part)
        cur.execute(sql)
        db.commit()
        db.rollback()
        
    except Exception as e:
            print("捕获到异常:", e)



# 扫描器时间线查询
def vuln_scan_status_show():
    try:
        db= pymysql.connect(host=dict['ip'],user=dict['username'],  
        password=dict['password'],db=dict['dbname'],port=dict['portnum']) 
        cur = db.cursor()
        sql="SELECT status_value FROM status_table where id = 2"
        cur.execute(sql)
        data = cur.fetchall()
        list_data = list(data)
        status_value = []
        for i in list_data:
            status_value.append(i[0])
        vuln_status_value_result = status_value[0]
    except:
        vuln_status_value_result = "MySQL连接失败"
    return vuln_status_value_result



# 扫描器时间线更新
def vuln_scan_status_update(part):
    try:
        db= pymysql.connect(host=dict['ip'],user=dict['username'],  
        password=dict['password'],db=dict['dbname'],port=dict['portnum']) 
        cur = db.cursor()
        sql="UPDATE status_table SET status_value = '%s' WHERE id = 2"%(part)
        cur.execute(sql)
        db.commit()
        db.rollback()
        
    except Exception as e:
            print("捕获到异常:", e)



# 从资产文件url.txt中根据规则分别提取出springboot、weblogic、struts2、shiro资产并写入对应的文件
def asset_by_rule_handle():

    # shiro
    try:
        shiro_file_list = key_point_assets_file(Shiro_rule)
        f_shiro = open(file='/TIP/info_scan/result/keyasset/shiro_file.txt',mode='w')
        for shiro_line in shiro_file_list:
            f_shiro.write(str(shiro_line)+"\n")
        f_shiro.close()
    except Exception as e:
        print("捕获到异常:", e)

    # springboot
    try:
        springboot_file_list = key_point_assets_file(SpringBoot_rule)
        f_springboot = open(file='/TIP/info_scan/result/keyasset/springboot_file.txt',mode='w')
        for springboot_line in springboot_file_list:
            f_springboot.write(str(springboot_line)+"\n")
        f_springboot.close()
    except Exception as e:
        print("捕获到异常:", e)

    # struts2
    try:
        struts2_file_list = key_point_assets_file(struts2_rule)
        f_struts2 = open(file='/TIP/info_scan/result/keyasset/struts2_file.txt',mode='w')
        for struts2_line in struts2_file_list:
            f_struts2.write(str(struts2_line)+"\n")
        f_struts2.close()
    except Exception as e:
        print("捕获到异常:", e)

    # weblogic
    try:
        weblogic_file_list = key_point_assets_file(weblogic_rule)
        f_weblogic = open(file='/TIP/info_scan/result/keyasset/weblogic_file.txt',mode='w')
        for weblogic_line in weblogic_file_list:
            f_weblogic.write(str(weblogic_line)+"\n")
        f_weblogic.close()
    except Exception as e:
        print("捕获到异常:", e)



# 磁盘读写状态查询
def disk_read_write():
    try:
        # 获取磁盘的读写速度，单位是字节每秒
        read_speed_bytes_per_sec = psutil.disk_io_counters().read_bytes
        write_speed_bytes_per_sec = psutil.disk_io_counters().write_bytes
    
        # 将字节转换为千字节
        read_speed_kb_per_sec = read_speed_bytes_per_sec / 1024
        write_speed_kb_per_sec = write_speed_bytes_per_sec / 1024
    
        
    except Exception as e:
        print("捕获到异常:", e)
    tuple_list = [read_speed_kb_per_sec,write_speed_kb_per_sec]
    return tuple_list


# thinkphp漏洞扫描
def thinkphp_scan():
    # 清空上一次扫描结果
    os.popen('rm -rf /TIP/info_scan/result/thinkphp_vuln.txt')
    # 遍历url列表
    url_list = url_file_ip_list()
    try:
        for i in url_list:
            os.popen('bash /TIP/info_scan/finger.sh thinkphp_vuln_scan'+' '+str(i)+'')
    except Exception as e:
        print("捕获到异常:", e)


# 利用otx网站查询域名绑定url
def otx_domain_url_lib():
    UA = UserAgent()
    try:
        # url.txt转换为列表
        url_list = url_file_ip_list()
        # 提取根域名
        root_domain_list = root_domain_scan(url_list)
        # 根域名去重
        root_domain_list_uniq = list(set(root_domain_list))
        domain_list_uniq_result = []
        for i in root_domain_list_uniq:
            if "cn" in i or "com" in i or "net" in i:
                domain_list_uniq_result.append(i)
    except Exception as e:
        print("捕获到异常:", e)

    
    for domain in domain_list_uniq_result:
        print("\n\n")
        print("[+]"+domain)
        time.sleep(2)
        try:
            url = "https://otx.alienvault.com/api/v1/indicators/domain/" + domain + "/url_list?limit=500&page=1"  
            headers={
            'Cookie':'Hm_lvt_ecdd6f3afaa488ece3938bcdbb89e8da=1615729527; Hm_lvt_d39191a0b09bb1eb023933edaa468cd5=1617883004,1617934903,1618052897,1618228943; Hm_lpvt_d39191a0b09bb1eb023933edaa468cd5=1618567746',
            'Host':'otx.alienvault.com',
            'User-Agent':UA.random
            }
            res = requests.get(url, headers=headers, allow_redirects=False)  
            res.raise_for_status() 
            res_json = res.json()
        
            data = res_json.get('url_list', [])

            # 打印结果 
            for item in data:
                url_text = item.get('url','')
                print(url_text)
        except Exception as e:
            # 出现异常继续下一下
            print("捕获到异常:", e)
            continue


def crt_subdomain_lib():
    try:
        # url.txt转换为列表
        url_list = url_file_ip_list()
        # 提取根域名
        root_domain_list = root_domain_scan(url_list)
        # 根域名去重
        root_domain_list_uniq = list(set(root_domain_list))
        # domain_list_uniq_result = []
        for i in root_domain_list_uniq:
            if "cn" in i or "com" in i or "net" in i:
                print("\n")
                print("[+]"+i)
                print("\n")
                try:
                    subdomain_list = []
                    time.sleep(1)
                    subdomain = subdomain_scan(i)
                    subdomain_list.append(subdomain)
                    subdomain_list_all = []
                    for item in subdomain_list:
                        subdomain_list_all.extend(item)
                    for kk in subdomain_list_all:
                        print(kk)
                except Exception as e:
                    print("捕获到异常:", e)
    except Exception as e:
        print("捕获到异常:", e)

    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        func_name = sys.argv[1]
        if func_name == 'otx_domain_url_lib':
            otx_domain_url_lib()
        elif func_name == 'crt_subdomain_lib':
            crt_subdomain_lib()
        else:
            print("Invalid function number")
    else:
        print("No function number provided")