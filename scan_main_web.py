'''
Description:[主系统]
Author:[huan666]
Date:[2023/11/15]
update:[2024/8/19]
'''
from flask import Flask, render_template,request
from flask import session
from flask import redirect
from flask_bootstrap import Bootstrap
from flask import send_file
import basic
import subprocess
import os
import re
from flask import jsonify
from config import history_switch
import report_total
import pandas as pd
from basic import root_domain_scan
from config import ceye_key

#主系统账号密码配置导入
from config import main_username
from config import main_password


# 重点资产数量规则
from config import Shiro_rule
from config import SpringBoot_rule
from config import weblogic_rule
from config import baota_rule
from config import ruoyi_rule
from config import struts2_rule
from config import WordPress_rule
from config import jboss_rule
from config import phpMyAdmin_rule
from config import ThinkPHP_rule
from config import nacos_rule
from config import fanwei_rule
from config import finger_list
from config  import rule_options
from config import dict
from basic import select_rule



import psutil
import pymysql

# 设置session过期时间
from datetime import timedelta


# 导入线程模块
import threading

# 导入时间模块
import time
from config import info_time_controls
from config import vuln_time_controls

app = Flask(__name__,template_folder='./templates') 
app.secret_key = "DragonFire"
bootstrap = Bootstrap(app)


#IP基础信息查询
@app.route("/ipscaninterface/",methods=['post'])
def ipscaninterface():
    user = session.get('username')
    if str(user) == main_username:
        ip = request.form['ip']
        
        #状态码为200的url
        try:
            data1=basic.status_scan(ip)
        except:
            pass
    
        #状态码为200的url指纹信息
        try:
            data3 = basic.finger_scan(ip)
        except:
            pass
    
        #icp备案信息-列表返回
        try:
            data4 = basic.icp_info(ip)
        except:
            pass
    
        #公司位置信息
        try:
            companylocation = basic.amapscan(data4)
        except:
            companylocation = "接口异常"
        
        #ip归属地
        try:
            output = subprocess.check_output(["sh", "./finger.sh","location",ip], stderr=subprocess.STDOUT)
            output_list = output.decode().splitlines()
            #定义列表
            location_list = []
            for ii in output_list:
                if "地址" in ii:
                    location_list.append(ii)
            localtion_list_1 = location_list[0].replace("地址","")
            localtion_list_result = localtion_list_1.replace(":","")
        except:
            localtion_list_result = "接口异常"
        
        #端口信息
        try:
            port = basic.shodan_api(ip)
        except:
            pass
    
        #历史域名
        try:
            history_domain = basic.domain_scan(ip)
        except:
            history_domain=["接口异常"]
    
        #操作系统识别
        try:
            os_type = os.popen('bash ./finger.sh osscan'+' '+ip).read()
        except:
            pass
        
        try:
            #去掉https://或者http://
            urls_list_1 = [re.sub(r'http://|https://', '', url) for url in data1]
        except:
            pass
       
        # 存活域名列表
        try:
            urls_list = []
            for aa in urls_list_1:
                if "cn" in aa or "com" in aa or "xyz" in aa or "top" in aa:
                    urls_list.append(aa)
        except:
            pass


        #定义存放cdn结果列表
        cdn_list = []
        #定义存放子域名的列表
        subdomain_list_1 = []
        
        urls_list_root = root_domain_scan(urls_list)
        for bb in urls_list:
            #cdn存放结果
            cdn_result = basic.cdnscan(bb)
            cdn_list.append(cdn_result)

        for ab in urls_list_root:
            #子域名存放列表
            subdomain_result = basic.subdomain_scan(ab)
            subdomain_list_1.append(subdomain_result)
        try:
            flattened_list = [item for sublist in subdomain_list_1 for item in sublist]
            
        except:
            pass
       
        #CDN列表为空判断
        if len(cdn_list) == 0:
            cdn_list.append("None")
        
    
        #子域名列表去重
        subdomain_list = list(set(flattened_list))
        if len(subdomain_list) ==0:
            subdomain_list.append("None")
        
    
        #网站标题
        try:
            site_title_list_result = basic.title_scan(data1)
        except:
            pass
    
        
        #IP属性判断
        try:
            ipstatus = basic.ipstatus_scan(ip)
        except:
            pass
    
    
        return render_template('index.html',data1=data1,data2=ip,data3=data3,data4=data4
        ,data5=localtion_list_result,data6=port,data7=history_domain,data8=os_type,data9=cdn_list
        ,data10=site_title_list_result,data11=subdomain_list,data12=ipstatus,data13=companylocation,data20=str(user))
    else:
        return render_template('login.html')

#跳转首页
@app.route("/index/")
def index():
    user = session.get('username')
    if str(user) == main_username:
        return render_template('index.html',data20=str(user))
    else:
        return render_template('login.html')
    
#主系统登录实现
@app.route('/logininterface/',methods=['post'])
def logininterface():
    username = request.form['username']
    password = request.form['password']
    
    # 登录判断
    if str(username) == str(main_username) and str(password) == str(main_password):
        session['username'] = username
        session.permanent_session_lifetime = timedelta(minutes=30)  # 设置会话过期时间为30分钟

        login_status = "账号密码正确确认登录系统吗？"
        redirecturl = '/index/'

    elif str(username) == str(main_username) and str(password) != str(main_password):
        login_status = "密码错误"
        redirecturl = '/loginpage/'
    elif str(username) != str(main_username) and str(password) == str(main_password):
        login_status = "账号不存在"
        redirecturl = '/loginpage/'
    else:
        login_status = "登录失败"
        redirecturl = '/loginpage/'

    message_json = {
        'loginstatus':login_status,
        'redirect_url':redirecturl,
        'nologin':'/loginpage/'
    }    
       
    return jsonify(message_json)
    


#历史URL查询
@app.route("/historyshow/")
def historyshow():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成历史url查询')
        # 每次启动前清空上次扫描结果
        os.popen('rm -rf /TIP/info_scan/result/otxhistoryurl.txt')
        os.popen('touch /TIP/info_scan/result/otxhistoryurl.txt')
        otx_domain_url_shell_status = os.popen('bash ./finger.sh otx_domain_url_shell_status').read()
        if "running" in otx_domain_url_shell_status:
            otx_status_result = "历史URL查询接口正在运行中请勿重复提交"
        else:
            try:
                os.popen('bash /TIP/info_scan/finger.sh otx_domain_url_shell')
                if "running" in otx_domain_url_shell_status:
                    otx_status_result = "历史URL查询接口已开启稍后查看结果"
                else:
                    otx_status_result = "历史URL查询接口正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)
        message_json = {
            "otx_status_result":otx_status_result
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')


#历史URL预览
@app.route("/previewhistoryurl/")
def previewhistoryurl():
    user = session.get('username')
    if str(user) == main_username:
        otx_his_num = os.popen('bash /TIP/info_scan/finger.sh otx_history_url_num').read()
        if int(otx_his_num) == 0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('/TIP/info_scan/result/otxhistoryurl.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')
    


#关闭历史URL查询接口
@app.route("/killotxhistory/")
def killotxhistory():
    user = session.get('username')
    if str(user) == main_username:
        otx_domain_url_shell_status = os.popen('bash ./finger.sh otx_domain_url_shell_status').read()
        os.popen('bash ./finger.sh kill_otx_domain_url_shell')
        if "stop" in otx_domain_url_shell_status:
            kill_otx_url_result = "已关闭历史URL查询接口"
        else:
            kill_otx_url_result = "正在关闭中......"

        message_json = {
            "kill_otx_url_result":kill_otx_url_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')
    


#关闭基于证书查询子域名接口
@app.route("/kill_crt_subdomain_shell/")
def kill_crt_subdomain_shell():
    user = session.get('username')
    if str(user) == main_username:
        crt_subdomain_shell_status = os.popen('bash ./finger.sh crt_subdomain_shell_status').read()
        os.popen('bash ./finger.sh kill_crt_subdomain_shell')
        if "stop" in crt_subdomain_shell_status:
            kill_crt_subdomain_result = "已关闭历史URL查询接口"
        else:
            kill_crt_subdomain_result = "正在关闭中......"

        message_json = {
            "kill_crt_subdomain_result":kill_crt_subdomain_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')


#nmap接口预览
@app.route("/nmapresultshow/")
def nmapresultshow():
    user = session.get('username')
    if str(user) == main_username:
        nmap_num = os.popen('bash /TIP/info_scan/finger.sh nmap_scan_num').read()
        if int(nmap_num) == 0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('./result/nmap.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')


#nuclei结果预览
@app.route("/nucleiresultshow/")
def nucleiresultshow():
    user = session.get('username')
    if str(user) == main_username:
        nuclei_num = os.popen('bash /TIP/info_scan/finger.sh nuclei_scan_num').read()
        if int(nuclei_num) == 0:
            liness = ["暂无数据"]
        else:
            lines = []
            with open('./result/nucleiresult.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
             #文件结果优化展示
            liness = []
            for line1 in lines:
                
                #页面显示优化
                pattern = re.compile(r'\x1b\[[0-9;]*m')
                clean_text = pattern.sub('', line1)
                liness.append(clean_text)
            
        return '<br>'.join(liness)
    else:
        return render_template('login.html')


#清空数据
@app.route("/deletenmapresult/")
def deletenmapresult():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('rm -rf ./result/nmap.txt')
        os.popen('touch ./result/nmap.txt')
        return render_template('index.html')
    else:
        return render_template('login.html')



#清空xray报告
@app.route("/deletexrayreport/")
def deletexrayreport():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('rm -rf /TIP/batch_scan_domain/report/*')
        return render_template('index.html')
    else:
        return render_template('login.html')


#结束进程
@app.route("/killprocess/")
def killprocess():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('bash ./server_check.sh killscan')
        return render_template('index.html')
    else:
        return render_template('login.html')


#前端文本框添加URL后端接口
@app.route('/submit_data/', methods=['POST'])  
def submit_data():
    user = session.get('username')
    if str(user) == main_username: 
        # 筛选后资产时间线更新
        basic.assets_status_update('手工录入资产完成')
        data = request.json.get('lines', [])

        if '' in  data:
            result_rule = "输入参数不能为空"

        if ' ' in data:
            result_rule = "输入参数不能包含空格"

        if 'alert' in data or 'select' in data or '<' in data or '>' in data or 'union' in data:
            result_rule = "请勿进行安全测试！"

        else:
            # 2024.8.2更新  校验非URL资产
            result_rule = ""
            for ii in data:
                if "http://"  not in ii and "https://" not in ii:
                    result_rule = "请勿输入非URL字段！"
                    break
            if not result_rule:
                # 列表中数据存入文件中
                f = open(file='/TIP/batch_scan_domain/url.txt',mode='w')
                for line in data:
                    f.write(str(line)+"\n")
                f.close()
                file_line = os.popen('bash ./finger.sh textarea_url_num').read()
                result_rule = "已成功添加"+str(file_line)+"条资产"
                #资产备份
                os.popen('cp /TIP/batch_scan_domain/url.txt /TIP/batch_scan_domain/url_back.txt')
            
        message_json = {
            "file_line":result_rule
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')


#启动nuclei
@app.route("/startnuclei/", methods=['POST'])
def startnuclei():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成nuclei漏洞扫描')
        nucleitatus = os.popen('bash ./finger.sh nucleistatus').read()
        if "running" in nucleitatus:
            nuclei_status_result = "nuclei扫描程序正在运行中请勿重复提交"
        else:
            poc_dir = request.form['poc_dir']
            if int(history_switch) == 0:
                os.popen('bash ./finger.sh startnuclei_url'+' '+poc_dir)
                nuclei_status_result = "nuclei扫描程序已开启稍后查看结果"
            elif int(history_switch) ==1:
                os.popen('bash ./finger.sh startnuclei_result')
            else:
                print("配置文件history_switch字段只允许0/1")


        message_json = {
            "nuclei_status_result":nuclei_status_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')
   


#系统管理
@app.route("/systemmanagement/")
def systemmanagement():
    user = session.get('username')
    if str(user) == main_username:

        # 扫描器运行状态
        nmapstatus =os.popen('bash ./finger.sh nmapstatus').read()
        nucleistatus =os.popen('bash ./finger.sh nucleistatus').read()
        xraystatus = os.popen('bash ./finger.sh xraystatus').read()
        radstatus =os.popen('bash ./finger.sh radstatus').read()
        dirscanstatus = os.popen('bash ./finger.sh dirsearchstatus').read()
        weblogicstatus = os.popen('bash ./finger.sh weblogic_status').read()
        struts2status = os.popen('bash ./finger.sh struts2_status').read()
        bbscanstatus = os.popen('bash ./finger.sh bbscan_status').read()
        vulmapscanstatus = os.popen('bash ./finger.sh vulmapscan_status').read()
        afrogscanstatus = os.popen('bash ./finger.sh afrogscan_status').read()
        fscanstatus = os.popen('bash ./finger.sh fscan_status').read()
        shirostatus = os.popen('bash ./finger.sh shiro_status').read()
        httpxstatus = os.popen('bash ./finger.sh httpx_status').read()
        eholestatus = os.popen('bash ./finger.sh ehole_status').read()
        springbootstatus = os.popen('bash ./finger.sh springboot_scan_status').read()
        hydrastatus = os.popen('bash ./finger.sh hydra_status').read()
        urlfinderstatus = os.popen('bash ./finger.sh urlfinder_status').read()
        thinkphpstatus = os.popen('bash ./finger.sh TPscan_status').read()
        # 目标url行数
        url_file_num = os.popen('bash ./finger.sh url_file_num').read()

        # 重点资产数量查询
       
        shiro_num = basic.key_point_assets_num(Shiro_rule)
        springboot_num = basic.key_point_assets_num(SpringBoot_rule)
        weblogic_num = basic.key_point_assets_num(weblogic_rule)
        baota_num = basic.key_point_assets_num(baota_rule)
        ruoyi_num = basic.key_point_assets_num(ruoyi_rule)
        struts2_num = basic.key_point_assets_num(struts2_rule)
        WordPress_num = basic.key_point_assets_num(WordPress_rule)
        jboss_num = basic.key_point_assets_num(jboss_rule)
        phpmyadmin_num = basic.key_point_assets_num(phpMyAdmin_rule)
        ThinkPHP_num = basic.key_point_assets_num(ThinkPHP_rule)
        nacos_num = basic.key_point_assets_num(nacos_rule)
        fanwei_num = basic.key_point_assets_num(fanwei_rule)

        # cpu占用率
        cpu_percent = psutil.cpu_percent(interval=1)

        # 获取内存信息  
        mem = psutil.virtual_memory()  
        # 计算内存占用百分比  
        memory_percent = mem.percent  

        # 资产规则
        if int(rule_options) == 1:
            key_asset_rule = str(finger_list)
            if len(finger_list) == 0:
                key_asset_rule = ['规则为空']
            key_asset_rule_origin = '数据来源: 配置文件'
        elif int(rule_options) == 2:
            key_asset_rule = select_rule()
            if len(key_asset_rule) == 0:
                key_asset_rule = ['规则为空']
            key_asset_rule_origin = '数据来源: MySQL数据库'
        else:
            key_asset_rule = ['参数只能为0/1']

        # 当前自查数量
        url_file_current_num = os.popen('bash ./finger.sh current_url_file_num').read()

        # 筛选后资产状态查询
        assets_status = basic.assets_status_show()

        # 漏洞扫描器时间线查询
        vuln_scan_status_shijianxian = basic.vuln_scan_status_show()

        # 磁盘读速率
        disk_read = basic.disk_read_write()[0]
        # 磁盘写速率
        disk_write = basic.disk_read_write()[1]

        # python后端服务状态
        infoinfostatus = os.popen('bash ./finger.sh infoinfostatus').read()
        dirsub_sys_status = os.popen('bash ./finger.sh dirsub_sys_status').read()
        xray_report_status = os.popen('bash ./finger.sh xray_report_status').read()
        urlfinder_report_status = os.popen('bash ./finger.sh urlfinder_report_status').read()
        afrog_report_status = os.popen('bash ./finger.sh afrog_report_status').read()

        otx_status = os.popen('bash ./finger.sh otx_domain_url_shell_status').read()
        crt_status = os.popen('bash ./finger.sh crt_subdomain_shell_status').read()
        weaver_status = os.popen('bash ./finger.sh weaver_status').read()
        message_json = {
            "nmapstatus":nmapstatus,
            "nucleistatus":nucleistatus,
            "xraystatus":xraystatus,
            "radstatus":radstatus,
            "dirscanstatus":dirscanstatus,
            "weblogicstatus":weblogicstatus,
            "struts2status":struts2status,
            "bbscanstatus":bbscanstatus,
            "vulmapscanstatus":vulmapscanstatus,
            "afrogscanstatus":afrogscanstatus,
            "fscanstatus":fscanstatus,
            "shirostatus":shirostatus,
            "httpxstatus":httpxstatus,
            "url_file_num":url_file_num,
            "eholestatus":eholestatus,
            "shiro_num":str(shiro_num),
            "springboot_num":str(springboot_num),
            "weblogic_num":str(weblogic_num),
            "baota_num":str(baota_num),
            "ruoyi_num":str(ruoyi_num),
            "struts2_num":str(struts2_num),
            "WordPress_num":str(WordPress_num),
            "cpuinfo":str(cpu_percent)+"%",
            "memoryinfo":str(memory_percent)+"%",
            "jboss_num":str(jboss_num),
            "phpmyadmin_num":str(phpmyadmin_num),
            "key_asset_rule":str(key_asset_rule),
            "current_key_asset_num":str(url_file_current_num),
            "springbootstatus":springbootstatus,
            "hydrastatus":hydrastatus,
            "urlfinderstatus":urlfinderstatus,
            "key_asset_rule_origin":key_asset_rule_origin,
            "assets_status":"原始资产-------->"+assets_status,
            "vuln_scan_status_shijianxian":vuln_scan_status_shijianxian,
            "disk_read":str(disk_read)+" KB/s",
            "disk_write":str(disk_write)+" KB/s",
            "infoinfostatus":infoinfostatus,
            "dirsub_sys_status":dirsub_sys_status,
            "xray_report_status":xray_report_status,
            "urlfinder_report_status":urlfinder_report_status,
            "afrog_report_status":afrog_report_status,
            "ThinkPHP_num":ThinkPHP_num,
            "thinkphpstatus":thinkphpstatus,
            "otx_status":otx_status,
            "crt_status":crt_status,
            "nacos_num":str(nacos_num),
            "fanwei_num":str(fanwei_num),
            "weaver_status":weaver_status

        }
        return jsonify(message_json)
    else:
        return render_template('login.html')

    


#文本框内容展示
@app.route("/textareashowinterface/")
def textareashowinterface():
    user = session.get('username')
    if str(user) == main_username:
        result_list = []
        file = open("/TIP/batch_scan_domain/url.txt",encoding='utf-8')
        for line in file.readlines():
            result_list.append(line.strip())
        url_num = os.popen('bash /TIP/info_scan/finger.sh textarea_url_num').read()
        message_json = {
            "textvalue":result_list,
            "url_num":"总共查出"+str(url_num)+"条数据"
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')


#资产去重
@app.route("/uniqdirsearchtargetinterface/",methods=['POST'])
def uniqdirsearchtargetinterface():
    user = session.get('username')
    if str(user) == main_username:
        # 筛选后资产时间线更新
        basic.assets_status_update('资产去重已完成')
        fileqingxiname = request.form['fileqingxiname']
        if int(fileqingxiname) == 1:
            
            #文件去重，保留IP地址
            os.popen('bash ./finger.sh withdrawip')
            return render_template('dirsearchscan.html')
        else:
            
            #文件去重，保留所有
            os.popen('bash ./finger.sh uniqfilterdirsearch')
    
            return render_template('dirsearchscan.html')
    else:
        return render_template('login.html')


#存活检测接口
@app.route("/filterstatuscodebyhttpx/",methods=['GET'])
def filterstatuscodebyhttpx():
    user = session.get('username')
    if str(user) == main_username:
        # 筛选后资产时间线更新
        basic.assets_status_update('存活检测已完成')
        httpx_status = os.popen('bash ./finger.sh httpx_status').read()
        if "running" in httpx_status:
            httpx_status_result = "httpx存活检测程序正在运行中请勿重复提交"
        else:
            try:
                os.popen('bash ./finger.sh survivaldetection')
                if "running" in httpx_status:
                    httpx_status_result = "httpx存活检测程序已开启稍后查看结果"
                else:
                    httpx_status_result = "httpx存活检测程序正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)
        message_json = {
            "httpx_status_result":httpx_status_result
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')

#链接扫描
@app.route("/starturlfinderinterface/",methods=['GET'])
def starturlfinderinterface():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成urlfinder链接扫描')
        urlfinder_status = os.popen('bash ./finger.sh urlfinder_status').read()
        if "running" in urlfinder_status:
            urlfinder_status_result = "urlfinder扫描程序正在运行中请勿重复提交"
        else:
            try:
                os.popen('bash ./finger.sh urlfinder_start')
                urlfinder_status = os.popen('bash ./finger.sh urlfinder_status').read()
                if "running" in urlfinder_status:
                    urlfinder_status_result = "urlfinder扫描程序已开启稍后查看结果"
                else:
                    urlfinder_status_result = "urlfinder正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)

        message_json = {
            "urlfinder_status_result":urlfinder_status_result
        }
        return jsonify(message_json)
    
    else:
        return render_template('login.html')


#清空链接扫描报告
@app.route("/deleteurlfinderreport/")
def deleteurlfinderreport():
    user = session.get('username')
    if str(user) == main_username:
        try:
            os.popen('rm -rf /TIP/info_scan/urlfinder_server/report/*')
        except Exception as e:
            print("捕获到异常:",e)
        return render_template('index.html')
    else:
        return render_template('login.html')



#跳转登录页
@app.route("/loginpage/")
def loginpage():
    return render_template('login.html')

#注销系统
@app.route('/signout/',methods=['get'])
def signout():
    try:
        session.clear()
    except Exception as e:
        print("捕获到异常:",e)
    message_json = {
        'zhuxiaostatus':'确认退出系统吗？',
        'zhuxiaoredirect_url':'/index/'
    }    
       
    return jsonify(message_json)


#cdn探测，将存在cdn和不存在cdn的域名分别存入不同列表中，用于过滤基础数据
# date:2024.4.3
@app.route('/cdn_service_recogize/',methods=['get'])
def cdn_service_recogize():
    user = session.get('username')
    if str(user) == main_username:
        # 筛选后资产时间线更新
        basic.assets_status_update('CDN检测已完成')    
        try:
            #遍历目标文件存入列表
            url_file = open("/TIP/batch_scan_domain/url.txt",encoding='utf-8')
            url_list = []
            for i in url_file.readlines():
                url_list.append(i)
            # url中提取域名存列表
            domain_list = []
            for j in url_list:

                domain_re = re.findall("https?://([^/]+)",j)
                domain_list.append(domain_re)

            # url中提取域名并删除掉长度为0的列表
            domain_list_result = []
            for k in domain_list:
                if len(k) > 0:
                    domain_list_result.append(k[0])
            
            # 存在cdn列表
            rule_cdn_domain_list = []
            # 不存在cdn列表
            rule_nocdn_domain_list = []
            for domain in domain_list_result:
                cdn_result = os.popen('bash ./finger.sh batch_cdn_scan'+' '+domain).read().strip() 
                
                cdn_result_origin = "有CDN"
                if str(cdn_result) == str(cdn_result_origin):
                    rule_cdn_domain_list.append(domain)
                else:
                    rule_nocdn_domain_list.append(domain)
            
            # 不存在cdn列表
            no_cdn_list_result = []
            for nocdn in rule_nocdn_domain_list:
                nocdnresult = os.popen('bash ./finger.sh recognize_no_cdn'+' '+nocdn).read().strip()
                no_cdn_list_result.append(nocdnresult)
            #列表写入到url.txt
            f = open(file='/TIP/batch_scan_domain/url.txt',mode='w')
            for fileline in no_cdn_list_result:
                f.write(str(fileline)+"\n")

        except Exception as e:
            print("捕获到异常:",e)
    return render_template('login.html')


#资产回退
@app.route("/assetsbackspaceinterface/")
def assetsbackspaceinterface():
    user = session.get('username')
    if str(user) == main_username:
        # 筛选后资产时间线更新
        basic.assets_status_update('资产回退已完成')
        os.popen('cp /TIP/batch_scan_domain/url_back.txt /TIP/batch_scan_domain/url.txt')
        return render_template('index.html')
    else:
        return render_template('login.html')
    

#weblogic_poc扫描
@app.route("/weblogicscaninterface/",methods=['get'])
def weblogicscaninterface():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成weblogic漏洞扫描')
        weblogic_status = os.popen('bash ./finger.sh weblogic_status').read()
        if "running" in weblogic_status:
            weblogic_status_result = "weblogic扫描程序正在运行中请勿重复提交"
        else:

            # 遍历目标文件存入列表
            url_list = []
            url_file = open('/TIP/batch_scan_domain/url.txt',encoding='utf-8')
            for i in url_file.readlines():
                url_list.append(i.strip())
            
            # url中匹配出域名
            domain_list = []
            for url in url_list:
                pattern = r"https?://([^/]+)"
                urls_re_1 = re.search(pattern,url)
                urls_re = urls_re_1.group(1)
                domain_list.append(urls_re)
            
            # 域名写入到weblogic_poc目标
            weblogic_file = open(file='/TIP/info_scan/weblogin_scan/target.txt', mode='w')
            for j in domain_list:
                weblogic_file.write(str(j)+"\n")
            weblogic_file.close()
    
            # weblogic_poc开始扫描
            os.popen('bash ./finger.sh weblogic_poc_scan')
            weblogic_status_result = "weblogic扫描程序已开启稍后查看结果"

        message_json = {
            "weblogic_status_result":weblogic_status_result
        }
        return jsonify(message_json)
            
    else:
        return render_template('login.html')
    

#weblogic_poc扫描结果预览
@app.route("/weblogic_poc_report/")
def weblogic_poc_report():
    user = session.get('username')
    if str(user) == main_username:
        weblogic_num = os.popen('bash /TIP/info_scan/finger.sh weblogic_scan_num').read()
        if int(weblogic_num) ==0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('./result/weblogic_poc.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')
    

# struts2_poc扫描
@app.route("/struts2_poc_scan/")
def struts2_poc_scan():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成struts2漏洞扫描')
        struts2status = os.popen('bash ./finger.sh struts2_status').read()
        if "running" in struts2status:
            struts2status_result = "struts2扫描程序正在运行中请勿重复提交"
        else:
            # 执行poc扫描
            os.popen('bash ./finger.sh struts2_poc_scan')
            struts2status_result = "struts2扫描程序已开启稍后查看结果"
        message_json = {
            "struts2status_result":struts2status_result
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')
    


#struts2_poc扫描结果预览
@app.route("/struts2_poc_report/")
def struts2_poc_report():
    user = session.get('username')
    if str(user) == main_username:
        struts2_num = os.popen('bash /TIP/info_scan/finger.sh struts2_scan_num').read()
        if int(struts2_num) ==0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('./result/struts2_poc.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')
    


# 报告整合
@app.route("/report_total_interface/")
def report_total_interface():
    user = session.get('username')
    if str(user) == main_username:
        # 执行报告整合脚本
        report_total.report_xlsx()
        return render_template('index.html')
    else:
        return render_template('login.html')

    

#ehole_finger扫描结果预览
@app.route("/ehole_finger_report/")
def ehole_finger_report():
    user = session.get('username')
    if str(user) == main_username:
        ehole_num = os.popen('bash /TIP/info_scan/finger.sh ehole_finger_num').read()
        if int(ehole_num) == 0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('./result/ehole_finger.txt', 'r') as f:
                for line in f:
                    
                    #显示优化去掉颜色字符
                    pattern = re.compile(r'\x1b\[[0-9;]*m')
                    clean_text = pattern.sub('', line)
                    lines.append(clean_text)
    
        return '<br>'.join(lines)
    else:
        return render_template('login.html')
    
# 启动EHole
@app.route("/ehole_finger_scan/")
def ehole_finger_scan():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成ehole指纹识别扫描')
        finger_status = os.popen('bash ./finger.sh ehole_status').read()
        if "running" in finger_status:
            finger_status_result = "EHole程序正在运行中请勿重复提交"
        else:
            # 执行指纹识别扫描
            os.popen('bash ./finger.sh ehole_finger_scan')
            if "running" in finger_status:
                finger_status_result = "EHole扫描程序已启动稍后查看扫描结果"
            else:
                finger_status_result = "EHole正在后台启动中......"

        message_json = {
            "finger_status_result":finger_status_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')
    

# bbscan_info_scan扫描
@app.route("/bbscan_info_scan/")
def bbscan_info_scan():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成bbscan敏感信息扫描')
        bbscan_status1 = os.popen('bash ./finger.sh bbscan_status').read()

        if "running" in bbscan_status1:
            bbscan_status_result = "敏感信息扫描程序正在运行中请勿重复提交"

        else:
            os.popen('rm -rf /TIP/info_scan/BBScan/report/*')
            # 执行敏感信息扫描
            os.popen('bash ./finger.sh bbscan_shell')
            if "running" in bbscan_status1:
                bbscan_status_result = "bbscan扫描程序已启动稍后查看扫描结果"
            else:
                bbscan_status_result = "bbscan正在后台启动中......"

        message_json = {
            "bbscan_status_result":bbscan_status_result
        }
        return jsonify(message_json)
    
    else:
        return render_template('login.html')


#bbscan扫描预览报告
@app.route("/showbbscanreport/")
def showbbscanreport():
    user = session.get('username')
    if str(user) == main_username:
        bbscan_num = os.popen('bash /TIP/info_scan/finger.sh bbscan_scan_num').read()
        if int(bbscan_num) == 0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('/TIP/info_scan/result/bbscan_info.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')
    

#通过证书批量查询目标子域名
@app.route("/batch_show_subdomain/",methods=['get'])
def batch_show_subdomain():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成子域名扫描')
        # 每次启动前清空上次扫描结果
        os.popen('rm -rf /TIP/info_scan/result/subdomain.txt')
        os.popen('touch /TIP/info_scan/result/subdomain.txt')
        crt_subdomain_shell_status = os.popen('bash ./finger.sh crt_subdomain_shell_status').read()
        if "running" in crt_subdomain_shell_status:
            crt_status_result = "基于证书查询子域名接口正在运行中请勿重复提交"
        else:
            try:
                os.popen('bash /TIP/info_scan/finger.sh crt_subdomain_shell')
                
                if "running" in crt_subdomain_shell_status:
                    crt_status_result = "基于证书查询子域名接口已开启稍后查看结果"
                else:
                    crt_status_result = "基于证书查询子域名接口正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)
        message_json = {
            "crt_status_result":crt_status_result
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')
    

#子域名预览报告
@app.route("/showsubdomainreport/")
def showsubdomainreport():
    user = session.get('username')
    if str(user) == main_username:
        subdomain_num = os.popen('bash /TIP/info_scan/finger.sh subdomain_scan_num').read()
        if int(subdomain_num) == 0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('/TIP/info_scan/result/subdomain.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')



#vulmap漏扫预览报告
@app.route("/vulmapscanreport/")
def vulmapscanreport():
    user = session.get('username')
    if str(user) == main_username:
        vulmap_num = os.popen('bash /TIP/info_scan/finger.sh vulmap_scan_num').read()
        if int(vulmap_num) == 0:
            liness = ["暂无数据"]
        else:
            lines = []
            with open('/TIP/info_scan/result/vulmapscan_info.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
             #文件结果优化展示
            liness = []
            for line1 in lines:
                
                #页面显示优化
                pattern = re.compile(r'\x1b\[[0-9;]*m')
                clean_text = pattern.sub('', line1)
                liness.append(clean_text)
        return '<br>'.join(liness)
    else:
        return render_template('login.html')



#启动vulmap漏扫程序
@app.route("/startvulmapinterface/",methods=['POST'])
def startvulmapinterface():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成vulmap漏洞扫描')
        vulnname = request.form['vulnname']
        vulmapscanstatus = os.popen('bash ./finger.sh vulmapscan_status').read()
        if "running" in vulmapscanstatus:
            vummap_scan_result = "vulmap扫描程序正在运行中请勿重复提交"
        else:
            try:
                os.popen('bash ./finger.sh vulmapscan_shell'+' '+vulnname)
                if "running" in vulmapscanstatus:
                    vummap_scan_result = "vulmap扫描程序已启动稍后查看扫描结果"
                else:
                    vummap_scan_result = "vulmap正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)

        message_json = {
            "vummap_scan_result":vummap_scan_result
        }
        return jsonify(message_json)

    else:
        return render_template('login.html')



#启动nmap批量端口扫描
@app.route("/startbatchnmapscan/",methods=['get'])
def startbatchnmapscan():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成nmap端口扫描')
        namptatus = os.popen('bash ./finger.sh nmapstatus').read()
        if "running" in namptatus:
            nmap_status_result = "nmap正在运行中请勿重复提交"
        
        else:

            try:
                # 创建线程来运行nmap任务
                nmap_thread = threading.Thread(target=basic.ip_queue_nmap())

                # 启动线程
                nmap_thread.start()
                
                if "running" in namptatus:
                    nmap_status_result = "nmap已开启稍后查看结果"
                else:
                    nmap_status_result = "nmap正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)

        message_json = {
            "nmap_status_result":nmap_status_result
        }

        return jsonify(message_json)

        
    else:
        return render_template('login.html')
    


#目标url文件存入列表回显给前端
@app.route("/url_list_textarea_show/")
def url_list_textarea_show():
    user = session.get('username')
    if str(user) == main_username:
        textvalue = basic.url_file_ip_list()
        message_json = {
            "textvalue":textvalue
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')


#ceye_dns记录
@app.route("/ceye_dns_record/")
def ceye_dns_record():
    user = session.get('username')
    if str(user) == main_username:
        result = os.popen('bash ./finger.sh ceye_dns'+' '+ceye_key).read()
        return result
    else:
        return render_template('login.html')



#ceye_http记录
@app.route("/ceye_http_record/")
def ceye_http_record():
    user = session.get('username')
    if str(user) == main_username:
        result = os.popen('bash ./finger.sh ceye_http'+' '+ceye_key).read()
        return result
    else:
        return render_template('login.html')
    

#清空afrog报告
@app.route("/deleteafrogreport/")
def deleteafrogreport():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('rm -rf /TIP/info_scan/afrog_scan/reports/*')
        return render_template('index.html')
    else:
        return render_template('login.html')


#启动afrog漏扫程序
@app.route("/startafrogscanprocess/",methods=['get'])
def startafrogscanprocess():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成afrog漏洞扫描')
        afrogscanstatus = os.popen('bash ./finger.sh afrogscan_status').read()
        if "running" in afrogscanstatus:
            start_afrog_result = "afrog正在运行中请勿重复提交"
        else:
            try:
                os.popen('bash ./finger.sh startafrogprocess')
                if "running" in afrogscanstatus:
                    start_afrog_result = "afrog已开启稍后查看结果"
                else:
                    start_afrog_result = "afrog正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)
        message_json = {
            "start_afrog_result":start_afrog_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')


#结束afrog进程
@app.route("/killafrogprocess/")
def killafrogprocess():
    user = session.get('username')
    if str(user) == main_username:
        afrogscanstatus = os.popen('bash ./finger.sh afrogscan_status').read()
        os.popen('bash ./finger.sh killafrog')
        if "stop" in afrogscanstatus:
            kill_afrog_result = "已关闭afrog扫描程序"
        else:
            kill_afrog_result = "正在关闭中......"

        message_json = {
            "kill_afrog_result":kill_afrog_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')
    


#关闭nmap进程
@app.route("/killnmapprocess/")
def killnmapprocess():
    user = session.get('username')
    if str(user) == main_username:
        nmapstatus =os.popen('bash ./finger.sh nmapstatus').read()
        os.popen('bash ./finger.sh killnmap')
        if "stop" in nmapstatus:
            kill_nmap_result = "已关闭nmap扫描程序"
        else:
            kill_nmap_result = "正在关闭中......"
        message_json = {
            "kill_nmap_result":kill_nmap_result
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')
    


#结束vulmap进程
@app.route("/killvulmapprocess/")
def killvulmapprocess():
    user = session.get('username')
    if str(user) == main_username:
        vulmapscanstatus = os.popen('bash ./finger.sh vulmapscan_status').read()
        os.popen('bash ./finger.sh killvulmap')
        if "stop" in vulmapscanstatus:
            kill_vulmap_result = "已关闭vulmap扫描程序"
        else:
            kill_vulmap_result = "正在关闭中......"
        message_json = {
            "kill_vulmap_result":kill_vulmap_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')



#结束nuclei进程
@app.route("/killnucleiprocess/")
def killnucleiprocess():
    user = session.get('username')
    if str(user) == main_username:
        nucleistatus =os.popen('bash ./finger.sh nucleistatus').read()

        os.popen('bash ./finger.sh killnuclei')
        if "stop" in nucleistatus:
            kill_nuclei_result = "已关闭nuclei扫描程序"
        else:
            kill_nuclei_result = "正在关闭中......"
        message_json = {
            "kill_nuclei_result":kill_nuclei_result
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')
    


#关闭bbscan程序
@app.route("/killbbscanprocess/")
def killbbscanprocess():
    user = session.get('username')
    if str(user) == main_username:
        bbscanstatus = os.popen('bash ./finger.sh bbscan_status').read()
        os.popen('bash ./finger.sh killbbscan')
        if "stop" in bbscanstatus:
            kill_bbscan_result = "已关闭bbscan扫描程序"
        else:
            kill_bbscan_result = "正在关闭中......"
        message_json = {
            "kill_bbscan_result":kill_bbscan_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')
    


#fscan报告预览
@app.route("/fscanreportyulan/")
def fscanreportyulan():
    user = session.get('username')
    if str(user) == main_username:
        fscan_num = os.popen('bash /TIP/info_scan/finger.sh fscan_scan_num').read()
        if int(fscan_num) ==0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('./result/fscan_vuln.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')


#启动fscan程序
@app.route("/startfcsaninterface/",methods=['POST'])
def startfcsaninterface():
    user = session.get('username')
    if str(user) == main_username:
        fscanpartname = request.form['fscanpartname']
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成fscan漏洞扫描')
        # 删除历史fscan扫描数据
        os.popen('rm -rf /TIP/info_scan/fscan_tool/result.txt')
    
        fscanstatus = os.popen('bash ./finger.sh fscan_status').read()
        if "running" in fscanstatus:
            fscan_status_result = "fscan扫描程序正在运行中请勿重复提交"
        else:
            try:
                basic.batch_fscan_interface(fscanpartname)
                
                if "running" in fscanstatus:
                    fscan_status_result = "fscan扫描程序已启动稍后查看扫描结果"
                else:
                    fscan_status_result = "fscan正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)
        message_json = {
            "fscan_status_result":fscan_status_result
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')
    

#结束fscan进程
@app.route("/killfscangprocess/")
def killfscangprocess():
    user = session.get('username')
    if str(user) == main_username:
        fscanstatus = os.popen('bash ./finger.sh fscan_status').read()
        os.popen('bash ./finger.sh killfscan')
        if "stop" in fscanstatus:
            kill_fscan_result = "已关闭fscan扫描程序"
        else:
            kill_fscan_result = "正在关闭中......"
        message_json = {
            "kill_fscan_result":kill_fscan_result
        }

        return jsonify(message_json)
        
    else:
        return render_template('login.html')



#shiro报告预览
@app.route("/shiro_report_show/")
def shiro_report_show():
    user = session.get('username')
    if str(user) == main_username:
        shiro_num = os.popen('bash /TIP/info_scan/finger.sh shiro_scan_num').read()
        if int(shiro_num) ==0:
            filtered_list_new = ["暂无数据"]
        else:
            lines = []
            with open('/TIP/info_scan/result/shiro_vuln.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
    
             #文件结果优化展示
            liness = []
            for line1 in lines:
                #页面显示优化
                pattern = re.compile(r'\x1b\[[0-9;]*m')
                clean_text = pattern.sub('', line1)
                liness.append(clean_text)
            # 使用列表推导式创建一个新列表，其中不包含以'Checking :'开头的元素  
            filtered_list = [item for item in liness if not item.startswith('Checking :')]
            filtered_list_new = []
            for fi in filtered_list:
                result = fi.replace("","")
                filtered_list_new.append(result)
        return '<br>'.join(filtered_list_new)
    else:
        return render_template('login.html')


#启动shiro程序
@app.route("/startshirointerface/")
def startshirointerface():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成shiro漏洞扫描')
        shiro_status = os.popen('bash ./finger.sh shiro_status').read()
        if "running" in shiro_status:
            shiro_status_result = "shiro扫描程序正在运行中请勿重复提交"
        else:
            try:
                basic.shiro_scan()
                shiro_status_result = "shiro扫描程序已开启稍后查看结果"
            except Exception as e:
                print("捕获到异常:", e)
        message_json = {
            "shiro_status_result":shiro_status_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')
    

#识别重点资产
@app.route("/key_assets_withdraw/")
def key_assets_withdraw():
    user = session.get('username')
    if str(user) == main_username:

        
        eholestatus = os.popen('bash ./finger.sh ehole_status').read()
        if "running" in eholestatus:
            key_assets_result = "指纹识别接口正在运行中请稍后再进行识别重点资产"
        else:

            # 根据config.py中finger_list配置进行识别，可在finger_list列表中配置多个，最终写入到全局资产文件url.txt中
            try:
                key_url_list = basic.key_point_tiqu()
               
                f = open(file='/TIP/batch_scan_domain/url.txt',mode='w')
                for line in key_url_list:
                    f.write(str(line)+"\n")
                f.close()
            except Exception as e:
                print("捕获到异常:", e)

            # 根据config.py中*_rule配置进行识别，只能配置一个关键字
            # 从资产文件url.txt中根据规则分别提取出springboot、weblogic、struts2、shiro资产并写入对应的文件
            basic.asset_by_rule_handle()

            key_assets_result = "已成功识别出重点资产"
            # 筛选后资产时间线更新
            basic.assets_status_update('识别重点资产已完成')
        
        message_json = {
            "key_assets_result":key_assets_result
        }
        return jsonify(message_json)
        
    else:
        return render_template('login.html')



#nuclei poc查询
@app.route("/nuclei_poc_show/",methods=['POST'])
def nuclei_poc_show():
    
    
    user = session.get('username')
    if str(user) == main_username:
        
        poc_dir = request.form['poc_dir']
    
        try:
            result = os.popen('bash /TIP/info_scan/finger.sh templatenuclei'+''+' '+poc_dir).read()
            nuclei_poc_list = []
            for i in result.splitlines():
                nuclei_poc_list.append(i)
            
        except Exception as e:
            print("捕获到异常:", e)

        message_json = {
            "nuclei_poc_list_global":nuclei_poc_list,
            "nuclei_poc_list_len":"总共查询到"+" "+str(len(nuclei_poc_list))+" "+"条yaml规则",
        }
        return jsonify(message_json)
    
    else:
        return render_template('login.html')

    

#springboot报告预览
@app.route("/springboot_report_show/")
def springboot_report_show():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('rm -rf /TIP/info_scan/result.txt')
        springboot_num = os.popen('bash /TIP/info_scan/finger.sh springboot_scan_num').read()
        if int(springboot_num) == 0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('./result/springboot_result.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')



#启动springboot漏洞扫描程序
@app.route("/start_springboot_vuln_scan/")
def start_springboot_vuln_scan():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成springboot漏洞扫描')
        springboot_scan_status = os.popen('bash ./finger.sh springboot_scan_status').read()
        if "running" in springboot_scan_status:
            springboot_scan_status_result = "springboot扫描程序正在运行中请勿重复提交"
        else:
            try:
                os.popen('bash /TIP/info_scan/finger.sh start_springboot')
                if "running" in springboot_scan_status:
                    springboot_scan_status_result = "springboot扫描程序已开启稍后查看结果"
                else:
                    springboot_scan_status_result = "springboot扫描程序正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)
        
        message_json = {
            "springboot_scan_status_result":springboot_scan_status_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')


# 通过fofa发现资产
@app.route("/fofa_search_assets_service/",methods=['POST'])
def fofa_search_assets_service():
    user = session.get('username')
    if str(user) == main_username:
        # 筛选后资产时间线更新
        basic.assets_status_update('通过fofa平台获取资产完成')

        part = request.form['part']
        num_fofa = request.form['num_fofa']
        if '' in  part:
            asset_len_list = "输入参数不能为空"

        if ' ' in part:
            asset_len_list = "输入参数不能包含空格"

        if 'alert' in part or 'select' in part or '<' in part or '>' in part or 'union' in part:
            asset_len_list = "请勿进行安全测试！"
        else:
            asset_len_list_1 = basic.fofa_search_assets_service_lib(part,num_fofa)
            asset_len_list = "总共发现"+" "+str(asset_len_list_1)+" "+"条资产已存入扫描目标中"
        message_json = {
            "asset_len_list":asset_len_list
        }
        return jsonify(message_json)
    else:
        return render_template('login.html')
    

#hydra报告预览
@app.route("/hydra_report_show/")
def hydra_report_show():
    user = session.get('username')
    if str(user) == main_username:
        hydra_num = os.popen('bash /TIP/info_scan/finger.sh hydra_scan_num').read()
        if int(hydra_num) == 0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('./result/hydra_result.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')
    


# 启动hydra弱口令扫描工具
@app.route("/start_hydra_interface/",methods=['POST'])
def start_hydra_interface():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成hydra弱口令扫描')
        # 调用url转ip函数写入文件
        ip_list = basic.url_convert_ip()
        f = open(file='/TIP/info_scan/result/hydra_ip.txt',mode='w')
        for line in ip_list:
            f.write(str(line)+"\n")

        # 开启扫描
        hydrapart = request.form['hydrapart']
        hydra_scan_status = os.popen('bash ./finger.sh hydra_status').read()

        if "running" in hydra_scan_status:
            hydra_scan_result = "hydra扫描程序正在运行中请勿重复提交"
        else:
            basic.start_hydra_lib(hydrapart)
            hydra_scan_result = "hydra扫描程序已开启稍后查看扫描结果"

        message_json = {
            "hydra_scan_result":hydra_scan_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')

    

#关闭hydra进程
@app.route("/killhydraprocess/")
def killhydraprocess():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('bash ./finger.sh killhydra')
        hydra_scan_status = os.popen('bash ./finger.sh hydra_status').read()
        if "stop" in hydra_scan_status:
            kill_hydra_result = "已关闭hydra扫描程序"
        else:
            kill_hydra_result = "正在关闭中......"
        message_json = {
            "kill_hydra_result":kill_hydra_result
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')



#关闭urlfinder进程
@app.route("/killurlfinderprocess/")
def killurlfinderprocess():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('bash ./finger.sh killurlfinder')
        urlfinderstatus = os.popen('bash ./finger.sh urlfinder_status').read()
        if "stop" in urlfinderstatus:
            kill_urlfinder_result = "已关闭URLFinder扫描程序"
        else:
            kill_urlfinder_result = "正在关闭中......"
        message_json = {
            "kill_urlfinder_result":kill_urlfinder_result
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')
    

#关闭EHole进程
@app.route("/killEHoleprocess/")
def killEHoleprocess():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('bash ./finger.sh killEHole')
        EHolestatus = os.popen('bash ./finger.sh ehole_status').read()
        if "stop" in EHolestatus:
            kill_EHole_result = "已关闭EHole扫描程序"
        else:
            kill_EHole_result = "正在关闭中......"
        message_json = {
            "kill_EHole_result":kill_EHole_result
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')
    

# 报告预览
@app.route('/totalreportyulan/')
def totalreportyulan():
    file_path = '/TIP/info_scan/result/vuln_report.xlsx'
    file_path_warn = '/TIP/info_scan/result/vuln_report_warn.xlsx'
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # 读取Excel文件的所有sheets
        xls = pd.ExcelFile(file_path)
        result_data = {sheet_name: pd.read_excel(file_path, sheet_name=sheet_name).to_dict(orient='records') 
                       for sheet_name in xls.sheet_names}
    else:
        text_list = ["{\"status\":\"failed\",\"errorcode\":500,\"describe\":\"正在进行报告整合...\"}"]
        df_a = pd.DataFrame(text_list, columns=['警告信息'])
        with pd.ExcelWriter('/TIP/info_scan/result/vuln_report_warn.xlsx', engine='openpyxl') as writer:
        # 将 DataFrame 写入不同的工作表  
            df_a.to_excel(writer, sheet_name='正在整合中...', index=False)
        # 读取Excel文件的所有sheets
        xls = pd.ExcelFile(file_path_warn)
        result_data = {sheet_name: pd.read_excel(file_path_warn, sheet_name=sheet_name).to_dict(orient='records') 
                       for sheet_name in xls.sheet_names}
    # 使用模板渲染HTML表格
    return render_template('preview.html', data=result_data)




# 报告下载
@app.route("/report_download_interface/",methods=['get'])
def report_download_interface():
    user = session.get('username')
    if str(user) == main_username:
        # 判断vuln_report.xlsx是否存在
        file_path = '/TIP/info_scan/result/vuln_report.xlsx'
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, download_name='vuln_report.xlsx')
        else:
            text_list = ["{\"status\":\"failed\",\"errorcode\":500,\"describe\":\"正在进行报告整合...\"}"]
            df_a = pd.DataFrame(text_list, columns=['警告信息'])
            with pd.ExcelWriter('/TIP/info_scan/result/vuln_report_warn.xlsx', engine='openpyxl') as writer:
            # 将 DataFrame 写入不同的工作表  
                df_a.to_excel(writer, sheet_name='sheet1', index=False)
            file_path1 = '/TIP/info_scan/result/vuln_report_warn.xlsx'
            return send_file(file_path1, as_attachment=True, download_name='vuln_report_warn.xlsx')
    
    else:
        return render_template('login.html')


#前端软重启系统服务
@app.route("/restartsystemservice/")
def restartsystemservice():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('bash ./finger.sh restartinfoscan')
        infoscanstatus = os.popen('bash ./finger.sh infoscanstatus').read()
        if "running" in infoscanstatus:
            infoscanstatus = "服务已启动"
        else:
            infoscanstatus = "正在重启中..."
        message_json = {
            "infoscanstatus":infoscanstatus,
            "comfirm":"确定重新启动服务吗?"
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')



# 关闭后端所有服务
@app.route("/stopbackserviceinterface/")
def stopbackserviceinterface():
    user = session.get('username')
    if str(user) == main_username:

        message_json = {
            "backcomfirm":"确定关闭所有后端服务吗?请谨慎操作，重启需登录服务器后台操作！"
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')
    
# 确认关闭后端所有服务
@app.route("/confirm_stop_service/",methods=['post'])
def confirm_stop_service():
    user = session.get('username')
    if str(user) == main_username:
        action = request.form['action']
        if action == '1':
            os.popen('bash /TIP/info_scan/finger.sh stopallserver')
            result_status = "关闭后端服务指令已开启"
        else:
            result_status = "关闭后端服务指令已取消"

        message_json = {
            "result_status":result_status
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')

    

# 识别重点资产中新增筛选规则接口
@app.route("/add_point_rule_interface/",methods=['post'])
def add_point_rule_interface():
    user = session.get('username')

    if str(user) == main_username:
        rule = request.form['rule']
        if '' in  rule:
            result_rule = "输入参数不能为空"

        if ' ' in rule:
            result_rule = "输入参数不能包含空格"

        if 'alert' in rule or 'select' in rule or '<' in rule or '>' in rule or 'union' in rule:
            result_rule = "请勿进行安全测试！"

        else:
            db= pymysql.connect(host=dict['ip'],user=dict['username'],  
            password=dict['password'],db=dict['dbname'],port=dict['portnum']) 
            cur = db.cursor()
            
            # 判断数据库中是否存在传入的数据
            sql_select = "select rule FROM rule_table where rule = '%s' "%(rule)
            cur.execute(sql_select)
            result = cur.fetchone()
            if result:
                result_rule = rule+" "+"规则已存在不要重复添加"
            else:
                sql_insert = "insert into rule_table(rule)  values('%s')" %(rule)
                cur.execute(sql_insert)  
                db.commit()
                result_rule = rule+" "+"规则已添加成功"
        message_json = {
            "result_rule":result_rule
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')


# 重点资产识别根据筛选规则名称删除
@app.route("/delete_point_rule_interface/",methods=['post'])
def delete_point_rule_interface():
    user = session.get('username')

    if str(user) == main_username:
        rule = request.form['rule']
        key = request.form['key']
        if '' in  rule:
            result_rule = "输入参数不能为空"

        if ' ' in rule:
            result_rule = "输入参数不能包含空格"

        if 'alert' in rule or 'select' in rule or '<' in rule or '>' in rule or 'union' in rule:
            result_rule = "请勿进行安全测试！"

        else:
            db= pymysql.connect(host=dict['ip'],user=dict['username'],  
            password=dict['password'],db=dict['dbname'],port=dict['portnum']) 
            cur = db.cursor()

            if int(key) == 1:
                # 判断是否删除成功
                sql1 = "select * from rule_table where rule = '%s' " %(rule)
                cur.execute(sql1)
                result = cur.fetchone()
                if result == None:
                    result_rule = rule+" "+"删除成功"

                else:

                    # 前端传递过来1为根据规则名称删除
                    sql="DELETE from rule_table WHERE rule = '%s' " %(rule)
                    cur.execute(sql)
                    db.commit()
                    db.rollback()

                    # 二次判断是否删除成功
                    sql1 = "select * from rule_table where rule = '%s' " %(rule)
                    cur.execute(sql1)
                    result = cur.fetchone()
                    if result == None:
                        result_rule = rule+" "+"删除完成,不要重复操作"

            elif int(key) ==2:
                

                # 判断是否删除成功
                sql1 = "select * from rule_table"
                cur.execute(sql1)
                result = cur.fetchone()
                if result == None:
                    result_rule = "规则已清空,不要重复操作"
                else:
                    # 前端传递过来2为清空筛选规则表
                    sql2="DELETE from rule_table"
                    cur.execute(sql2)
                    db.commit()
                    db.rollback()
                    
                    # 二次判断是否删除成功
                    sql1 = "select * from rule_table"
                    cur.execute(sql1)
                    result = cur.fetchone()
                    if result == None:
                        result_rule = "已清空所有规则"

            else:
                print("参数值只允许1/2")
            
            
        message_json = {
            "delete_rule":result_rule
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')




#启动tpscan程序
@app.route("/starttpscaninterface/")
def starttpscaninterface():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成thinkphp漏洞扫描')
        tpscan_status = os.popen('bash ./finger.sh TPscan_status').read()
        if "running" in tpscan_status:
            thinkphp_status_result = "thinkphp扫描程序正在运行中请勿重复提交"
        else:
            try:
                basic.thinkphp_scan()
                if "running" in tpscan_status:
                    thinkphp_status_result = "thinkphp扫描程序已开启稍后查看结果"
                else:
                    thinkphp_status_result = "thinkphp扫描程序正在后台启动中......"
 
            except Exception as e:
                print("捕获到异常:", e)
        message_json = {
            "thinkphp_status_result":thinkphp_status_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')
    


#thinkphp_poc扫描结果预览
@app.route("/thinkphp_poc_report/")
def thinkphp_poc_report():
    user = session.get('username')
    if str(user) == main_username:
        thinkphp_num = os.popen('bash /TIP/info_scan/finger.sh thinkphp_scan_num').read()
        if int(thinkphp_num) == 0:
            lines = ["暂无数据"]
        else:
            lines = []
            with open('/TIP/info_scan/result/thinkphp_vuln.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
        return '<br>'.join(lines)
    else:
        return render_template('login.html')
    



#开启泛微OA漏洞扫描
@app.route("/startweavervulnscan/",methods=['GET'])
def startweavervulnscan():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成泛微OA漏洞扫描')
        weaver_status = os.popen('bash ./finger.sh weaver_status').read()
        if "running" in weaver_status:
            weaver_status_result = "泛微OA漏洞扫描程序正在运行中请勿重复提交"
        else:
            try:
                os.popen('bash ./finger.sh weaver_exp_scan')
                weaver_status = os.popen('bash ./finger.sh weaver_status').read()
                if "running" in weaver_status:
                    weaver_status_result = "泛微OA漏洞扫描程序已开启稍后查看结果"
                else:
                    weaver_status_result = "泛微OA漏洞扫描程序正在后台启动中......"
            except Exception as e:
                print("捕获到异常:", e)

        message_json = {
            "weaver_status_result":weaver_status_result
        }
        return jsonify(message_json)
    
    else:
        return render_template('login.html')



#泛微扫描结果预览
@app.route("/weaverresultshow/")
def weaverresultshow():
    user = session.get('username')
    if str(user) == main_username:
        os.popen('rm -rf /TIP/info_scan/weaver_exp/*.zip')
        weaver_scan_num = os.popen('bash /TIP/info_scan/finger.sh weaver_scan_num').read()
        if int(weaver_scan_num) == 0:
            liness = ["暂无数据"]
        else:
            lines = []
            with open('./result/weaver_vuln.txt', 'r') as f:
                for line in f:
                    lines.append(line.strip())
             #文件结果优化展示
            liness = []
            for line1 in lines:
                
                #页面显示优化
                pattern = re.compile(r'\x1b\[[0-9;]*m')
                clean_text = pattern.sub('', line1)
                liness.append(clean_text)
            
        return '<br>'.join(liness)
    else:
        return render_template('login.html')



#关闭泛微OA漏洞扫描程序
@app.route("/killweavervulnscan/")
def killweavervulnscan():
    user = session.get('username')
    if str(user) == main_username:
        weaver_status = os.popen('bash ./finger.sh weaver_status').read()
        os.popen('bash ./finger.sh kill_weaver_scan')
        if "stop" in weaver_status:
            kill_weaver_result = "已关闭历史URL查询接口"
        else:
            kill_weaver_result = "正在关闭中......"

        message_json = {
            "kill_weaver_result":kill_weaver_result
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')



# 前端复选框批量开启信息收集工具接口
@app.route("/infoscan_check_back/",methods=['post'])
def infoscan_check_back():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成开启批量信息收集')
        data = request.get_json()  # 使用 get_json 解析 JSON 请求体
        info_front_list = data['info_front_list']
        # 接收前端传入的值转为int型
        info_value_list = []
        for i in info_front_list:
            info_value_list.append(int(i))

        # 遍历列表判断调用哪个扫描器
        for j in info_value_list:
            if '1' in str(j):
                # 获取系统当前时间
                current_time = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes = basic.info_time_shijian_cha(1)

                if int(diff_time_minutes) > info_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.last_time_update_lib(current_time,1)
                    # 提交扫描任务
                    bbscan_status1 = os.popen('bash ./finger.sh bbscan_status').read()
                    if "running" in bbscan_status1:
                        bbscan_status_result = "敏感信息扫描程序正在运行中请勿重复提交"
                    else:
                        os.popen('rm -rf /TIP/info_scan/BBScan/report/*')
                        # 执行敏感信息扫描
                        os.popen('bash ./finger.sh bbscan_shell')
                        if "running" in bbscan_status1:
                            bbscan_status_result = "bbscan扫描程序已启动稍后查看扫描结果"
                        else:
                            bbscan_status_result = "bbscan正在后台启动中......"
                else:
                    bbscan_status_result = "bbscan扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
                
                
            elif '2' in str(j):
                # 获取系统当前时间
                current_time2 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes2 = basic.info_time_shijian_cha(2)
                if int(diff_time_minutes2) > info_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.last_time_update_lib(current_time2,2)
                    # 提交扫描任务

                    finger_status = os.popen('bash ./finger.sh ehole_status').read()
                    if "running" in finger_status:
                        finger_status_result = "EHole程序正在运行中请勿重复提交"
                    else:
                        # 执行指纹识别扫描
                        os.popen('bash ./finger.sh ehole_finger_scan')
                        if "running" in finger_status:
                            finger_status_result = "EHole扫描程序已启动稍后查看扫描结果"
                        else:
                            finger_status_result = "EHole正在后台启动中......"
                else:
                    finger_status_result = "EHole扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif '3' in str(j):
                # 获取系统当前时间
                current_time3 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes3 = basic.info_time_shijian_cha(3)
                if int(diff_time_minutes3) > info_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.last_time_update_lib(current_time3,3)
                    # 提交扫描任务
                    # 每次启动前清空上次扫描结果
                    os.popen('rm -rf /TIP/info_scan/result/otxhistoryurl.txt')
                    os.popen('touch /TIP/info_scan/result/otxhistoryurl.txt')
                    otx_domain_url_shell_status = os.popen('bash ./finger.sh otx_domain_url_shell_status').read()
                    if "running" in otx_domain_url_shell_status:
                        otx_status_result = "历史URL查询接口正在运行中请勿重复提交"
                    else:
                        try:
                            os.popen('bash /TIP/info_scan/finger.sh otx_domain_url_shell')
                            if "running" in otx_domain_url_shell_status:
                                otx_status_result = "历史URL查询接口已开启稍后查看结果"
                            else:
                                otx_status_result = "历史URL查询接口正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                else:
                    otx_status_result = "历史URL查询接口"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif '4' in str(j):
                # 获取系统当前时间
                current_time4 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes4 = basic.info_time_shijian_cha(4)
                if int(diff_time_minutes4) > info_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.last_time_update_lib(current_time4,4)
                    # 提交扫描任务
                    # 每次启动前清空上次扫描结果
                    os.popen('rm -rf /TIP/info_scan/result/subdomain.txt')
                    os.popen('touch /TIP/info_scan/result/subdomain.txt')
                    crt_subdomain_shell_status = os.popen('bash ./finger.sh crt_subdomain_shell_status').read()
                    if "running" in crt_subdomain_shell_status:
                        crt_status_result = "基于证书查询子域名接口正在运行中请勿重复提交"
                    else:
                        try:
                            os.popen('bash /TIP/info_scan/finger.sh crt_subdomain_shell')
                            
                            if "running" in crt_subdomain_shell_status:
                                crt_status_result = "基于证书查询子域名接口已开启稍后查看结果"
                            else:
                                crt_status_result = "基于证书查询子域名接口正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                else:
                    crt_status_result = "基于证书查询子域名接口"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif '5' in str(j):
                # 获取系统当前时间
                current_time5 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes5 = basic.info_time_shijian_cha(5)
                if int(diff_time_minutes5) > info_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.last_time_update_lib(current_time5,5)
                    # 提交扫描任务
                    # 每次启动前清空上次扫描结果
                    os.popen('rm -rf /TIP/info_scan/result/nmap.txt')
                    os.popen('touch /TIP/info_scan/result/nmap.txt')
                    namptatus = os.popen('bash ./finger.sh nmapstatus').read()
                    if "running" in namptatus:
                        nmap_status_result = "nmap正在运行中请勿重复提交"
                    
                    else:
            
                        try:
                            
                            # 创建线程来运行nmap任务
                            nmap_thread = threading.Thread(target=basic.ip_queue_nmap())
    
                            # 启动线程
                            nmap_thread.start()
    
                            if "running" in namptatus:
                                nmap_status_result = "nmap已开启稍后查看结果"
                            else:
                                nmap_status_result = "nmap正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                else:
                    nmap_status_result = "nmap端口扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            else:
                print("参数正在完善中...")

        try:
            bbscan_status_result1 = bbscan_status_result
        except:
            bbscan_status_result1 = ""
        try:
            finger_status_result1 = finger_status_result
        except:
            finger_status_result1 = ""

        try:
            otx_status_result1 = otx_status_result
        except:
            otx_status_result1 = ""
        try:
            crt_status_result1 = crt_status_result
        except:
            crt_status_result1 = ""
        try:
            nmap_status_result1 = nmap_status_result
        except:
            nmap_status_result1 = ""
        
        dict = {
            "key1":bbscan_status_result1,
            "key2":finger_status_result1,
            "key3":otx_status_result1,
            "key4":crt_status_result1,
            "key5":nmap_status_result1
        }
        message_json = {
            "dictkey1":dict['key1'],
            "dictkey2":dict['key2'],
            "dictkey3":dict['key3'],
            "dictkey4":dict['key4'],
            "dictkey5":dict['key5'],
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')





# 前端复选框批量开启漏洞扫描工具接口
@app.route("/vulnscan_check_back/",methods=['post'])
def vulnscan_check_back():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成开启批量漏洞扫描')
        # 使用 get_json 解析 JSON 请求体,接收前端传递过来的json
        data = request.get_json()  
        vuln_front_list = data['vuln_front_list']
        fscanpartname = int(data['fscanpartname'])
        hydrapart = int(data['hydrapart'])
        vulnname = data['vulnname']
        poc_dir = data['poc_dir']
        
        # 遍历列表判断调用哪个扫描器
        for k in vuln_front_list:
            if '1' in str(k):
                print("struts2")
                # 获取系统当前时间
                current_time1 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes1 = basic.vuln_time_shijian_cha(1)
                if int(diff_time_minutes1) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time1,1)
                    # 提交扫描任务

                    struts2status = os.popen('bash ./finger.sh struts2_status').read()
                    if "running" in struts2status:
                        struts2status_result = "struts2扫描程序正在运行中请勿重复提交"
                    else:
                        # 执行poc扫描
                        os.popen('bash ./finger.sh struts2_poc_scan')
                        struts2status_result = "struts2扫描程序已开启稍后查看结果"
                else:
                    struts2status_result = "struts2扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"

            elif '2' in str(k):
                print("weblogic")
                # 获取系统当前时间
                current_time2 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes2 = basic.vuln_time_shijian_cha(2)
                if int(diff_time_minutes2) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time2,2)
                    # 提交扫描任务
                    weblogic_status = os.popen('bash ./finger.sh weblogic_status').read()
                    if "running" in weblogic_status:
                        weblogic_status_result = "weblogic扫描程序正在运行中请勿重复提交"
                    else:
            
                        # 遍历目标文件存入列表
                        url_list = []
                        url_file = open('/TIP/batch_scan_domain/url.txt',encoding='utf-8')
                        for i in url_file.readlines():
                            url_list.append(i.strip())
                        
                        # url中匹配出域名
                        domain_list = []
                        for url in url_list:
                            pattern = r"https?://([^/]+)"
                            urls_re_1 = re.search(pattern,url)
                            urls_re = urls_re_1.group(1)
                            domain_list.append(urls_re)
                        
                        # 域名写入到weblogic_poc目标
                        weblogic_file = open(file='/TIP/info_scan/weblogin_scan/target.txt', mode='w')
                        for j in domain_list:
                            weblogic_file.write(str(j)+"\n")
                        weblogic_file.close()
                
                        # weblogic_poc开始扫描
                        os.popen('bash ./finger.sh weblogic_poc_scan')
                        weblogic_status_result = "weblogic扫描程序已开启稍后查看结果"
                    
                else:
                    weblogic_status_result = "weblogic扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"

            elif '3' in str(k):
                print("shiro")
                # 获取系统当前时间
                current_time3 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes3 = basic.vuln_time_shijian_cha(3)
                if int(diff_time_minutes3) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time3,3)
                    # 提交扫描任务
                    shiro_status = os.popen('bash ./finger.sh shiro_status').read()
                    if "running" in shiro_status:
                        shiro_status_result = "shiro扫描程序正在运行中请勿重复提交"
                    else:
                        try:
                            basic.shiro_scan()
                            shiro_status_result = "shiro扫描程序已开启稍后查看结果"
                        except Exception as e:
                            print("捕获到异常:", e)
                    
                else:
                    shiro_status_result = "shiro扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"

            elif '4' in str(k):
                print("springboot")
                # 获取系统当前时间
                current_time4 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes4 = basic.vuln_time_shijian_cha(4)
                if int(diff_time_minutes4) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time4,4)
                    # 提交扫描任务
                    springboot_scan_status = os.popen('bash ./finger.sh springboot_scan_status').read()
                    if "running" in springboot_scan_status:
                        springboot_scan_status_result = "springboot扫描程序正在运行中请勿重复提交"
                    else:
                        try:
                            os.popen('bash /TIP/info_scan/finger.sh start_springboot')
                            if "running" in springboot_scan_status:
                                springboot_scan_status_result = "springboot扫描程序已开启稍后查看结果"
                            else:
                                springboot_scan_status_result = "springboot扫描程序正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                                
                else:
                    springboot_scan_status_result = "springboot扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif '5' in str(k):
                print("thinkphp")
                # 获取系统当前时间
                current_time5 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes5 = basic.vuln_time_shijian_cha(5)
                if int(diff_time_minutes5) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time5,5)
                    # 提交扫描任务
                    tpscan_status = os.popen('bash ./finger.sh TPscan_status').read()
                    if "running" in tpscan_status:
                        thinkphp_status_result = "thinkphp扫描程序正在运行中请勿重复提交"
                    else:
                        try:
                            basic.thinkphp_scan()
                            if "running" in tpscan_status:
                                thinkphp_status_result = "thinkphp扫描程序已开启稍后查看结果"
                            else:
                                thinkphp_status_result = "thinkphp扫描程序正在后台启动中......"
             
                        except Exception as e:
                            print("捕获到异常:", e)
                                
                else:
                    thinkphp_status_result = "thinkphp扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif '6' in str(k):
                print("afrog")
                # 获取系统当前时间
                current_time6 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes6 = basic.vuln_time_shijian_cha(6)
                if int(diff_time_minutes6) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time6,6)
                    # 提交扫描任务
                    afrogscanstatus = os.popen('bash ./finger.sh afrogscan_status').read()
                    if "running" in afrogscanstatus:
                        start_afrog_result = "afrog正在运行中请勿重复提交"
                    else:
                        try:
                            os.popen('bash ./finger.sh startafrogprocess')
                            if "running" in afrogscanstatus:
                                start_afrog_result = "afrog已开启稍后查看结果"
                            else:
                                start_afrog_result = "afrog正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                                
                else:
                    start_afrog_result = "afrog扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif '7' in str(k):
                print("fscan")
                # 获取系统当前时间
                current_time7 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes7 = basic.vuln_time_shijian_cha(7)
                if int(diff_time_minutes7) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time7,7)
                    # 提交扫描任务
                    # 删除历史fscan扫描数据
                    os.popen('rm -rf /TIP/info_scan/fscan_tool/result.txt')
                
                    fscanstatus = os.popen('bash ./finger.sh fscan_status').read()
                    if "running" in fscanstatus:
                        fscan_status_result = "fscan扫描程序正在运行中请勿重复提交"
                    else:
                        try:
                            basic.batch_fscan_interface(fscanpartname)
                            
                            if "running" in fscanstatus:
                                fscan_status_result = "fscan扫描程序已启动稍后查看扫描结果"
                            else:
                                fscan_status_result = "fscan正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                                
                else:
                    fscan_status_result = "fscan扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif '8' in str(k):
                print("弱口令")
                # 获取系统当前时间
                current_time8 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes8 = basic.vuln_time_shijian_cha(8)
                if int(diff_time_minutes8) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time8,8)
                    # 提交扫描任务
                    # 调用url转ip函数写入文件
                    ip_list = basic.url_convert_ip()
                    f = open(file='/TIP/info_scan/result/hydra_ip.txt',mode='w')
                    for line in ip_list:
                        f.write(str(line)+"\n")
                    
                    # 开启扫描
                    hydra_scan_status = os.popen('bash ./finger.sh hydra_status').read()
            
                    if "running" in hydra_scan_status:
                        hydra_scan_result = "hydra扫描程序正在运行中请勿重复提交"
                    else:
                        basic.start_hydra_lib(hydrapart)
                        hydra_scan_result = "hydra扫描程序已开启稍后查看扫描结果"
                                            
                else:
                    hydra_scan_result = "hydra扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif '9' in str(k):
                print("api接口")
                # 获取系统当前时间
                current_time9 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes9 = basic.vuln_time_shijian_cha(9)
                if int(diff_time_minutes9) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time9,9)
                    # 提交扫描任务
                    urlfinder_status = os.popen('bash ./finger.sh urlfinder_status').read()
                    if "running" in urlfinder_status:
                        urlfinder_status_result = "urlfinder扫描程序正在运行中请勿重复提交"
                    else:
                        try:
                            os.popen('bash ./finger.sh urlfinder_start')
                            urlfinder_status = os.popen('bash ./finger.sh urlfinder_status').read()
                            if "running" in urlfinder_status:
                                urlfinder_status_result = "urlfinder扫描程序已开启稍后查看结果"
                            else:
                                urlfinder_status_result = "urlfinder正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                                            
                else:
                    urlfinder_status_result = "urlfinder扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif 'a' in str(k):
                print("vulmap")
                # 获取系统当前时间
                current_time10 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes10 = basic.vuln_time_shijian_cha(10)
                if int(diff_time_minutes10) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time10,10)
                    # 提交扫描任务
                    vulmapscanstatus = os.popen('bash ./finger.sh vulmapscan_status').read()
                    if "running" in vulmapscanstatus:
                        vummap_scan_result = "vulmap扫描程序正在运行中请勿重复提交"
                    else:
                        try:
                            os.popen('bash ./finger.sh vulmapscan_shell'+' '+vulnname)
                            if "running" in vulmapscanstatus:
                                vummap_scan_result = "vulmap扫描程序已启动稍后查看扫描结果"
                            else:
                                vummap_scan_result = "vulmap正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                                            
                else:
                    vummap_scan_result = "vulmap扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif 'b' in str(k):
                print("nuclei")
                # 获取系统当前时间
                current_time11 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes11 = basic.vuln_time_shijian_cha(11)
                if int(diff_time_minutes11) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time11,11)
                    # 提交扫描任务
                    nucleitatus = os.popen('bash ./finger.sh nucleistatus').read()
                    if "running" in nucleitatus:
                        nuclei_status_result = "nuclei扫描程序正在运行中请勿重复提交"
                    else:
                        
                        if int(history_switch) == 0:
                            os.popen('bash ./finger.sh startnuclei_url'+' '+poc_dir)
                            nuclei_status_result = "nuclei扫描程序已开启稍后查看结果"
                        elif int(history_switch) ==1:
                            os.popen('bash ./finger.sh startnuclei_result')
                        else:
                            print("配置文件history_switch字段只允许0/1")
                                            
                else:
                    nuclei_status_result = "nuclei扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif 'c' in str(k):
                print("泛微OA")
                # 获取系统当前时间
                current_time12 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes12 = basic.vuln_time_shijian_cha(12)
                if int(diff_time_minutes12) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time12,12)
                    # 提交扫描任务
                    weaver_status = os.popen('bash ./finger.sh weaver_status').read()
                    if "running" in weaver_status:
                        weaver_status_result = "泛微OA漏洞扫描程序正在运行中请勿重复提交"
                    else:
                        try:
                            os.popen('bash ./finger.sh weaver_exp_scan')
                            weaver_status = os.popen('bash ./finger.sh weaver_status').read()
                            if "running" in weaver_status:
                                weaver_status_result = "泛微OA漏洞扫描程序已开启稍后查看结果"
                            else:
                                weaver_status_result = "泛微OA漏洞扫描程序正在后台启动中......"
                        except Exception as e:
                            print("捕获到异常:", e)
                                            
                else:
                    weaver_status_result = "泛微OA扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            elif 'd' in str(k):
                print("重点资产")
                # 获取系统当前时间
                current_time13 = time.time()
                # 当前时间和数据库中的作时间差
                diff_time_minutes13 = basic.vuln_time_shijian_cha(13)
                if int(diff_time_minutes13) > vuln_time_controls:
                    # 超过单位时间更新数据库中的时间
                    basic.vuln_last_time_update_lib(current_time13,13)
                    # 提交扫描任务
                    # 从资产文件url.txt中根据规则分别提取出springboot、weblogic、struts2、shiro资产并写入对应的文件
                    basic.asset_by_rule_handle()
                    
                    # 计算shiro_file文件行数，如果为0不开启，否则开启
                    shiro_num =  os.popen('bash ./finger.sh zhongdian_file_num shiro_file.txt').read()
                    if int(shiro_num) == 0:
                        all_shiro_status_result = "shiro资产为空无法开启扫描"
                    else:
                        # 开启shiro
                        shiro_status = os.popen('bash ./finger.sh shiro_status').read()
                        if "running" in shiro_status:
                            all_shiro_status_result = "shiro扫描程序正在运行中请勿重复提交"
                        else:
                            try:
                                basic.shiro_scan()
                                if "running" in shiro_status:
                                    all_shiro_status_result = "shiro扫描程序已开启稍后查看结果"
                                else:
                                    all_shiro_status_result = "shiro扫描程序正在后台启动中......"
                            except Exception as e:
                                print("捕获到异常:", e)
                    
            
                    # 计算springboot_file文件行数，如果为0不开启，否则开启
                    springboot_num =  os.popen('bash ./finger.sh zhongdian_file_num springboot_file.txt').read()
                    if int(springboot_num) == 0:
                        all_springboot_status_result = "springboot资产为空无法开启扫描"
                    else:
                        # 开启springboot
                        springboot_scan_status = os.popen('bash ./finger.sh springboot_scan_status').read()
                        if "running" in springboot_scan_status:
                            all_springboot_status_result = "springboot扫描程序正在运行中请勿重复提交"
                        else:
                            try:
                                os.popen('bash /TIP/info_scan/finger.sh start_springboot')
                                if "running" in springboot_scan_status:
                                    all_springboot_status_result = "springboot扫描程序已开启稍后查看结果"
                                else:
                                    all_springboot_status_result = "springboot扫描程序正在后台启动中......"
                            except Exception as e:
                                print("捕获到异常:", e)
            
            
                    # 计算struts2_file文件行数，如果为0不开启，否则开启
                    struts2_num =  os.popen('bash ./finger.sh zhongdian_file_num struts2_file.txt').read()
                    if int(struts2_num) == 0:
                        all_struts2_status_result = "struts2资产为空无法开启扫描"
                    else:
                        # 开启struts2
                        struts2status = os.popen('bash ./finger.sh struts2_status').read()
                        if "running" in struts2status:
                            all_struts2_status_result = "struts2扫描程序正在运行中请勿重复提交"
                        else:
                            try:
                                os.popen('bash ./finger.sh struts2_poc_scan')
                                if "running" in struts2status:
                                    all_struts2_status_result = "struts2扫描程序已开启稍后查看结果"
                                else:
                                    all_struts2_status_result = "struts2扫描程序正在后台启动中......"
                            except Exception as e:
                                print("捕获到异常:", e)
                            
            
            
                    # 计算weblogic_file文件行数，如果为0不开启，否则开启
                    weblogic_num =  os.popen('bash ./finger.sh zhongdian_file_num weblogic_file.txt').read()
                    if int(weblogic_num) == 0:
                        all_weblogic_status_result = "weblogic资产为空无法开启扫描"
                    else:
                        # 开启weblogic
                        weblogic_status = os.popen('bash ./finger.sh weblogic_status').read()
                        if "running" in weblogic_status:
                            all_weblogic_status_result = "weblogic扫描程序正在运行中请勿重复提交"
                        else:
                
                            # 遍历目标文件存入列表
                            url_list = []
                            url_file = open('/TIP/batch_scan_domain/url.txt',encoding='utf-8')
                            for i in url_file.readlines():
                                url_list.append(i.strip())
                            
                            # url中匹配出域名
                            domain_list = []
                            for url in url_list:
                                pattern = r"https?://([^/]+)"
                                urls_re_1 = re.search(pattern,url)
                                urls_re = urls_re_1.group(1)
                                domain_list.append(urls_re)
                            
                            # 域名写入到weblogic_poc目标
                            weblogic_file = open(file='/TIP/info_scan/weblogin_scan/target.txt', mode='w')
                            for j in domain_list:
                                weblogic_file.write(str(j)+"\n")
                            weblogic_file.close()
                    
                            # weblogic_poc开始扫描
                            os.popen('bash ./finger.sh weblogic_poc_scan')
                            if "running" in weblogic_status:
                                all_weblogic_status_result = "weblogic扫描程序已开启稍后查看结果"
                            else:
                                all_weblogic_status_result = "weblogic扫描程序正在后台启动中......"

                    point_all_result = all_shiro_status_result+" "+all_springboot_status_result+" "+all_struts2_status_result+" "+all_weblogic_status_result
                                            
                else:
                    point_all_result = "重点资产扫描程序"+str(info_time_controls)+"分钟内不允许重复扫描"
            else:
                print("其他扫描器正在完善中......")
        try:
            struts2status_result1 = struts2status_result
        except:
            struts2status_result1 = ""
        try:
            weblogic_status_result1 = weblogic_status_result
        except:
            weblogic_status_result1 = ""

        try:
            shiro_status_result1 = shiro_status_result
        except:
            shiro_status_result1 = ""

        try:
            springboot_scan_status_result1 = springboot_scan_status_result
        except:
            springboot_scan_status_result1 = ""
        try:
            thinkphp_status_result1 = thinkphp_status_result
        except:
            thinkphp_status_result1 = ""
        try:
            start_afrog_result1 = start_afrog_result
        except:
            start_afrog_result1 = ""

        try:
            fscan_status_result1 = fscan_status_result
        except:
            fscan_status_result1 = ""

        try:
            hydra_scan_result1 = hydra_scan_result
        except:
            hydra_scan_result1 = ""

        try:
            urlfinder_status_result1 = urlfinder_status_result
        except:
            urlfinder_status_result1 = ""

        try:
            vummap_scan_result1 = vummap_scan_result
        except:
            vummap_scan_result1 = ""
        try:
            nuclei_status_result1 = nuclei_status_result
        except:
            nuclei_status_result1 = ""

        try:
            weaver_status_result1 = weaver_status_result
        except:
            weaver_status_result1 = ""
        
        try:
            point_all_result1 = point_all_result
        except:
            point_all_result1 = ""
        message_json = {
            "struts2status_result":struts2status_result1,
            "weblogic_status_result":weblogic_status_result1,
            "shiro_status_result":shiro_status_result1,
            "springboot_scan_status_result":springboot_scan_status_result1,
            "thinkphp_status_result":thinkphp_status_result1,
            "start_afrog_result":start_afrog_result1,
            "fscan_status_result":fscan_status_result1,
            "hydra_scan_result":hydra_scan_result1,
            "urlfinder_status_result":urlfinder_status_result1,
            "vummap_scan_result":vummap_scan_result1,
            "nuclei_status_result":nuclei_status_result1,
            "weaver_status_result":weaver_status_result1,
            "point_all_result":point_all_result1
        }

        return jsonify(message_json)
    else:
        return render_template('login.html')



# 前端复选框批量关闭信息收集工具接口
@app.route("/stop_infoscan_back/",methods=['post'])
def stop_infoscan_back():
    user = session.get('username')
    if str(user) == main_username:
        # 漏洞扫描器时间线更新
        basic.vuln_scan_status_update('已完成关闭批量信息收集')
        data = request.get_json()  # 使用 get_json 解析 JSON 请求体
        info_front_list = data['info_front_list']
        # 接收前端传入的值转为int型
        info_value_list = []
        for i in info_front_list:
            info_value_list.append(int(i))

        # 遍历列表判断关闭哪个扫描器
        for j in info_value_list:
            if '1' in str(j):
                bbscanstatus = os.popen('bash ./finger.sh bbscan_status').read()
                os.popen('bash ./finger.sh killbbscan')
                if "stop" in bbscanstatus:
                    kill_bbscan_result = "已关闭bbscan扫描程序"
                else:
                    kill_bbscan_result = "正在关闭中......"
            elif '2' in str(j):
                os.popen('bash ./finger.sh killEHole')
                EHolestatus = os.popen('bash ./finger.sh ehole_status').read()
                if "stop" in EHolestatus:
                    kill_EHole_result = "已关闭EHole扫描程序"
                else:
                    kill_EHole_result = "正在关闭中......"
            elif '3' in str(j):
                otx_domain_url_shell_status = os.popen('bash ./finger.sh otx_domain_url_shell_status').read()
                os.popen('bash ./finger.sh kill_otx_domain_url_shell')
                if "stop" in otx_domain_url_shell_status:
                    kill_otx_url_result = "已关闭历史URL查询接口"
                else:
                    kill_otx_url_result = "正在关闭中......"
            elif '4' in str(j):
                crt_subdomain_shell_status = os.popen('bash ./finger.sh crt_subdomain_shell_status').read()
                os.popen('bash ./finger.sh kill_crt_subdomain_shell')
                if "stop" in crt_subdomain_shell_status:
                    kill_crt_subdomain_result = "已关闭历史URL查询接口"
                else:
                    kill_crt_subdomain_result = "正在关闭中......"
            elif '5' in str(j):
                nmapstatus =os.popen('bash ./finger.sh nmapstatus').read()
                os.popen('bash ./finger.sh killnmap')
                if "stop" in nmapstatus:
                    kill_nmap_result = "已关闭nmap扫描程序"
                else:
                    kill_nmap_result = "正在关闭中......"
            else:
                print("参数正在完善中...")

        try:
            kill_bbscan_result1 = kill_bbscan_result
        except:
            kill_bbscan_result1 = ""
        try:
            kill_EHole_result1 = kill_EHole_result
        except:
            kill_EHole_result1 = ""

        try:
            kill_otx_url_result1 = kill_otx_url_result
        except:
            kill_otx_url_result1 = ""
        try:
            kill_crt_subdomain_result1 = kill_crt_subdomain_result
        except:
            kill_crt_subdomain_result1 = ""
        try:
            kill_nmap_result1 = kill_nmap_result
        except:
            kill_nmap_result1 = ""
        
        dict = {
            "key11":kill_bbscan_result1,
            "key21":kill_EHole_result1,
            "key31":kill_otx_url_result1,
            "key41":kill_crt_subdomain_result1,
            "key51":kill_nmap_result1
        }
        message_json = {
            "dictkey11":dict['key11'],
            "dictkey21":dict['key21'],
            "dictkey31":dict['key31'],
            "dictkey41":dict['key41'],
            "dictkey51":dict['key51'],
        }

        return jsonify(message_json)
    
    else:
        return render_template('login.html')


if __name__ == '__main__':  
    app.run(host="127.0.0.1",port=80)