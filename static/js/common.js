// 上线后需替换为自己的服务器IP地址
var ipvalue = "http://x.x.x.x"


function fanhui() {
    var input = document.getElementById("myInput");
    input.value = "";
    window.location.href = "/index/";
}



//nmap扫描结果预览
function nmapjumpfunc() {

    window.open("/nmapresultshow/");
}

//nuclei扫描结果预览
function nucleijumpfunc() {

    window.open("/nucleiresultshow/");
}





//ajax异步清除数据
function deletenmapfunc() {
    var input = document.getElementById("myInput");
    input.value = "";
    $.ajax({
        url: '/deletenmapresult/',
        method: 'GET',
        success: function (res) {
            console.log(res)
            console.log('已删除端口扫描报告')
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {
            alert('已删除端口扫描报告')
        }
    })
}



//xray报告预览
function xrayreportshow() {
    window.open(ipvalue + ":18888/", "_blank");
}


//urlfinder报告预览
function urlfinderreportshow() {
    window.open(ipvalue + ":16666/", "_blank");
}


//ajax异步删除xray报告
function xrayreportdelete() {
    $.ajax({
        url: '/deletexrayreport/',
        method: 'GET',
        success: function (res) {
            console.log(res)
            console.log('已删除xray报告')
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {
            alert('已删除xray报告')
        }
    })
}


//ajax异步删除链接扫描报告
function deleteurlfinderreportfunc() {
    $.ajax({
        url: '/deleteurlfinderreport/',
        method: 'GET',
        success: function (res) {
            console.log(res)
            console.log('已删除链接报告')
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {
            alert('已删除链接报告')
        }
    })
}



//ajax异步关闭xray和rad引擎进程
function killxrayandradfunc() {
    $.ajax({
        url: '/killprocess/',
        method: 'GET',
        success: function (res) {
            console.log(res)
            console.log('已关闭xray和rad引擎')
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {
            alert('已关闭xray和rad引擎')
        }
    })
}


//文本框内容添加
function sendtextareadata() {
    // 获取textarea的值  
    const text = document.getElementById('myTextarea').value;
    // 按换行符分割文本为数组  
    const lines = text.split('\n');
    // 使用jQuery的$.ajax方法发送POST请求到Flask后端  
    $.ajax({
        url: '/submit_data/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ lines: lines }),
        dataType: 'json',
        success: function (info) {
            alert(info.file_line)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    });
}

//启动xray和rad提示


function startradandxray() {
    alert("进入命令行分别开启xray和rad" + "\n" + "启动rad：python3 /TIP/batch_scan_domain/radscan.py" + "\n" +
        "启动xray：bash /TIP/batch_scan_domain/start.sh startxray")
}


//ajax异步启动nuclei
function startnucleifunc() {
    var poc_dir = $('select[name="poc_dir"]').val();
    $.ajax({
        url: '/startnuclei/',
        method: 'POST',
        data: {
            poc_dir: poc_dir
        },
        success: function (info) {
            alert(info.nuclei_status_result)

        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//ajax异步查看历史url
function historyurlfunc() {
    $.ajax({
        url: '/historyshow/',
        method: 'GET',
        success: function (info) {
            alert(info.otx_status_result)
        },
        error: function () {
            alert('出现内部错误')

        },
        complete: function () {

        }
    })

}




//ajax异步关闭otx历史url查询接口
function killotxhistory_func() {
    $.ajax({
        url: '/killotxhistory/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_otx_url_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}



//历史url预览
function historyurlpreviewfunc() {

    window.open("/previewhistoryurl/");
}


//文本框内容展示
function textinfoshowfunc() {

    // 定义一个函数来处理AJAX请求
    function fetchData() {
        $.ajax({
            url: '/textareashowinterface/',
            method: 'GET',
            success: function (info) {

                $('#opbyid3').empty();
                for (var i = 0; i < info.textvalue.length; i++) {
                    $('#opbyid3').append('<option>' + info.textvalue[i] + '</option><br>');
                }
                document.getElementById("span1").innerHTML = info.url_num;
            },
            error: function () {
                alert('出现内部错误')

            },
            complete: function () {

            }
        })
    }

    // 调用fetchData函数初始化显示
    fetchData();
    // 设置定时器，每5000毫秒（5秒）执行一次fetchData函数
    var intervalId = setInterval(fetchData, 5000);
}

// 确保在页面卸载或组件销毁时清除定时器，以防止内存泄漏
window.addEventListener("beforeunload", function () {
    clearInterval(intervalId);
});


//xray报告预览
function uniqdirfunc() {
    window.open("/pathuniqpage/", "_blank");
}


//路径去重处理函数
function processURLs() {
    var inputUrls = document.getElementById('urlInput').value.split('\n');
    var outputDiv = document.getElementById('output');
    outputDiv.innerHTML = ''; // 清空输出区域

    var uniquePaths = [];

    inputUrls.forEach(function (url) {
        var path = url.substring(0, url.lastIndexOf('/') + 1);
        if (!uniquePaths.includes(path)) {
            uniquePaths.push(path);
            var outputLine = document.createElement('p');
            outputLine.textContent = path;
            outputDiv.appendChild(outputLine);
        }
    });
}

//archive 历史url查询
function archiveurlshowfunc() {
    var inputValue = document.getElementById("myInput").value;
    window.open("https://web.archive.org/cdx/search?collapse=urlkey&fl=original&limit=10000000000000000&matchType=domain&output=text&url=" + inputValue, "_blank");
}


//启用按钮
function startbutton() {
    var button2 = document.getElementById("button2");
    button2.disabled = false;
    var button3 = document.getElementById("button3");
    button3.disabled = false;
    var button4 = document.getElementById("button4");
    button4.disabled = false;

    var button6 = document.getElementById("button6");
    button6.disabled = false;
    var button7 = document.getElementById("button7");
    button7.disabled = false;
    var button8 = document.getElementById("button8");
    button8.disabled = false;
    var button9 = document.getElementById("button9");
    button9.disabled = false;
    var button10 = document.getElementById("button10");
    button10.disabled = false;
    var button11 = document.getElementById("button11");
    button11.disabled = false;
    var button12 = document.getElementById("button12");
    button12.disabled = false;
    var button13 = document.getElementById("button13");
    button13.disabled = false;
    var button14 = document.getElementById("button14");
    button14.disabled = false;
    var button15 = document.getElementById("button15");
    button15.disabled = false;
    var button16 = document.getElementById("button16");
    button16.disabled = false;
    var button17 = document.getElementById("button17");
    button17.disabled = false;
    var button18 = document.getElementById("button18");
    button18.disabled = false;
    var button19 = document.getElementById("button19");
    button19.disabled = false;
    var button20 = document.getElementById("button20");
    button20.disabled = false;
    var button21 = document.getElementById("button21");
    button21.disabled = false;
    var button22 = document.getElementById("button22");
    button22.disabled = false;
    var button23 = document.getElementById("button23");
    button23.disabled = false;
    var button24 = document.getElementById("button24");
    button24.disabled = false;
    var button25 = document.getElementById("button25");
    button25.disabled = false;
    var button27 = document.getElementById("button27");
    button27.disabled = false;
    var button28 = document.getElementById("button28");
    button28.disabled = false;
    var button29 = document.getElementById("button29");
    button29.disabled = false;
    var button30 = document.getElementById("button30");
    button30.disabled = false;
    var button31 = document.getElementById("button31");
    button31.disabled = false;
    var button32 = document.getElementById("button32");
    button32.disabled = false;
    var button33 = document.getElementById("button33");
    button33.disabled = false;
    var button34 = document.getElementById("button34");
    button34.disabled = false;
    var button35 = document.getElementById("button35");
    button35.disabled = false;
    var button36 = document.getElementById("button36");
    button36.disabled = false;
    var button37 = document.getElementById("button37");
    button37.disabled = false;
    var button38 = document.getElementById("button38");
    button38.disabled = false;
    var button39 = document.getElementById("button39");
    button39.disabled = false;
    var button40 = document.getElementById("button40");
    button40.disabled = false;
    var button41 = document.getElementById("button41");
    button41.disabled = false;
    var button42 = document.getElementById("button42");
    button42.disabled = false;
    var button43 = document.getElementById("button43");
    button43.disabled = false;
    var button46 = document.getElementById("button46");
    button46.disabled = false;
    var button47 = document.getElementById("button47");
    button47.disabled = false;
    var button48 = document.getElementById("button48");
    button48.disabled = false;
    var button49 = document.getElementById("button49");
    button49.disabled = false;
    var button50 = document.getElementById("button50");
    button50.disabled = false;
    var button51 = document.getElementById("button51");
    button51.disabled = false;
    var button52 = document.getElementById("button52");
    button52.disabled = false;
    var button53 = document.getElementById("button53");
    button53.disabled = false;
    var button54 = document.getElementById("button54");
    button54.disabled = false;
    var button55 = document.getElementById("button55");
    button55.disabled = false;
    var button56 = document.getElementById("button56");
    button56.disabled = false;
    var button57 = document.getElementById("button57");
    button57.disabled = false;
    var button58 = document.getElementById("button58");
    button58.disabled = false;
    var button59 = document.getElementById("button59");
    button59.disabled = false;
    var button60 = document.getElementById("button60");
    button60.disabled = false;
    var button61 = document.getElementById("button61");
    button61.disabled = false;
    var button62 = document.getElementById("button62");
    button62.disabled = false;
    var button63 = document.getElementById("button63");
    button63.disabled = false;
    var button64 = document.getElementById("button64");
    button64.disabled = false;
    var button65 = document.getElementById("button65");
    button65.disabled = false;
    var button66 = document.getElementById("button66");
    button66.disabled = false;
    var button67 = document.getElementById("button67");
    button67.disabled = false;


}

//禁用按钮
function stopbutton() {
    var button2 = document.getElementById("button2");
    button2.disabled = true;
    var button3 = document.getElementById("button3");
    button3.disabled = true;
    var button4 = document.getElementById("button4");
    button4.disabled = true;
    var button6 = document.getElementById("button6");
    button6.disabled = true;
    var button7 = document.getElementById("button7");
    button7.disabled = true;
    var button8 = document.getElementById("button8");
    button8.disabled = true;
    var button9 = document.getElementById("button9");
    button9.disabled = true;
    var button10 = document.getElementById("button10");
    button10.disabled = true;
    var button11 = document.getElementById("button11");
    button11.disabled = true;
    var button12 = document.getElementById("button12");
    button12.disabled = true;
    var button13 = document.getElementById("button13");
    button13.disabled = true;
    var button14 = document.getElementById("button14");
    button14.disabled = true;
    var button15 = document.getElementById("button15");
    button15.disabled = true;
    var button16 = document.getElementById("button16");
    button16.disabled = true;
    var button17 = document.getElementById("button17");
    button17.disabled = true;
    var button18 = document.getElementById("button18");
    button18.disabled = true;
    var button19 = document.getElementById("button19");
    button19.disabled = true;
    var button20 = document.getElementById("button20");
    button20.disabled = true;
    var button21 = document.getElementById("button21");
    button21.disabled = true;
    var button22 = document.getElementById("button22");
    button22.disabled = true;
    var button23 = document.getElementById("button23");
    button23.disabled = true;
    var button24 = document.getElementById("button24");
    button24.disabled = true;
    var button25 = document.getElementById("button25");
    button25.disabled = true;
    var button27 = document.getElementById("button27");
    button27.disabled = true;
    var button28 = document.getElementById("button28");
    button28.disabled = true;
    var button29 = document.getElementById("button29");
    button29.disabled = true;
    var button30 = document.getElementById("button30");
    button30.disabled = true;
    var button31 = document.getElementById("button31");
    button31.disabled = true;
    var button32 = document.getElementById("button32");
    button32.disabled = true;
    var button33 = document.getElementById("button33");
    button33.disabled = true;
    var button34 = document.getElementById("button34");
    button34.disabled = true;
    var button35 = document.getElementById("button35");
    button35.disabled = true;
    var button36 = document.getElementById("button36");
    button36.disabled = true;
    var button37 = document.getElementById("button37");
    button37.disabled = true;
    var button38 = document.getElementById("button38");
    button38.disabled = true;
    var button39 = document.getElementById("button39");
    button39.disabled = true;
    var button40 = document.getElementById("button40");
    button40.disabled = true;
    var button41 = document.getElementById("button41");
    button41.disabled = true;
    var button42 = document.getElementById("button42");
    button42.disabled = true;
    var button43 = document.getElementById("button43");
    button43.disabled = true;
    var button46 = document.getElementById("button46");
    button46.disabled = true;
    var button47 = document.getElementById("button47");
    button47.disabled = true;
    var button48 = document.getElementById("button48");
    button48.disabled = true;
    var button49 = document.getElementById("button49");
    button49.disabled = true;
    var button50 = document.getElementById("button50");
    button50.disabled = true;
    var button51 = document.getElementById("button51");
    button51.disabled = true;
    var button52 = document.getElementById("button52");
    button52.disabled = true;
    var button53 = document.getElementById("button53");
    button53.disabled = true;
    var button54 = document.getElementById("button54");
    button54.disabled = true;
    var button55 = document.getElementById("button55");
    button55.disabled = true;
    var button56 = document.getElementById("button56");
    button56.disabled = true;
    var button57 = document.getElementById("button57");
    button57.disabled = true;
    var button58 = document.getElementById("button58");
    button58.disabled = true;
    var button59 = document.getElementById("button59");
    button59.disabled = true;
    var button60 = document.getElementById("button60");
    button60.disabled = true;
    var button61 = document.getElementById("button61");
    button61.disabled = true;
    var button62 = document.getElementById("button62");
    button62.disabled = true;
    var button63 = document.getElementById("button63");
    button63.disabled = true;
    var button64 = document.getElementById("button64");
    button64.disabled = true;
    var button65 = document.getElementById("button65");
    button65.disabled = true;
    var button66 = document.getElementById("button66");
    button66.disabled = true;
    var button67 = document.getElementById("button67");
    button67.disabled = true;


}


//跳转到目录扫描页面
function jumpdirscanpage() {
    window.open(ipvalue + ":17777/dirscanpage/", "_blank");
}


//数据处理模块
function filedeweightingfunc() {
    var fileqingxiname = $('select[name="fileqingxiname"]').val();
    $.ajax({
        url: '/uniqdirsearchtargetinterface/',
        method: 'POST',
        data: {
            fileqingxiname: fileqingxiname
        },
        success: function (res) {
            console.log(res)
            console.log('资产去重成功点击文本查看最新数据')
        },
        error: function () {
            alert('资产去重处理出错')
        },
        complete: function () {
            alert('资产去重成功点击文本查看最新数据')
        }
    })
}

//存活检测
function filterstatuscodefunc() {
    $.ajax({
        url: '/filterstatuscodebyhttpx/',
        method: 'GET',

        success: function (info) {
            alert(info.httpx_status_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}

//链接扫描
function urlfinderscanfunc() {
    $.ajax({
        url: '/starturlfinderinterface/',
        method: 'GET',
        success: function (info) {
            alert(info.urlfinder_status_result)
        },
        error: function () {
            alert('链接扫描出错')
        },
        complete: function () {

        }
    })
}

//ajax异步启动注销系统
function signoutfunc() {
    $.ajax({
        url: '/signout/',
        method: 'GET',
        success: function (info) {
            alert(info.zhuxiaostatus);
            window.location.href = info.zhuxiaoredirect_url;
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//CDN检测
function filtercdndatafunc() {
    $.ajax({
        url: '/cdn_service_recogize/',
        method: 'GET',

        success: function (res) {
            console.log(res)
            console.log('CDN检测成功点击文本查看最新数据')
        },
        error: function () {
            alert('存活检测出现错误')
        },
        complete: function () {
            alert('CDN检测成功点击文本查看最新数据')
        }
    })
}



//资产回退
function assetsbackspacefunc() {
    $.ajax({
        url: '/assetsbackspaceinterface/',
        method: 'GET',

        success: function (res) {
            console.log(res)
            console.log('资产回退成功点击文本查看最新数据')
        },
        error: function () {
            alert('资产回退出现错误')
        },
        complete: function () {
            alert('资产回退成功点击文本查看最新数据')
        }
    })
}

//weblogic_poc 扫描
function weblogicscanfunc() {
    $.ajax({
        url: '/weblogicscaninterface/',
        method: 'GET',

        success: function (res) {
            console.log(res)

        },
        error: function () {
            alert('weblogic_poc扫描出错')
        },
        complete: function () {

        }
    })
    $.getJSON("/weblogicscaninterface/",
        function (info) {
            alert(info.weblogic_status_result)
        })
}

//weblogic_poc报告预览
function weblogicreportfunc() {
    window.open("/weblogic_poc_report/", "_blank");
}

//struts2_poc报告预览
function struts2reportfunc() {
    window.open("/struts2_poc_report/", "_blank");
}


//struts2_poc 扫描
function struts2scanfunc() {
    $.ajax({
        url: '/struts2_poc_scan/',
        method: 'GET',

        success: function (info) {
            alert(info.struts2status_result)

        },
        error: function () {
            alert('struts2_poc扫描出错')
        },
        complete: function () {

        }
    })
}

//报告整合
function reporttotalfunc() {
    $.ajax({
        url: '/report_total_interface/',
        method: 'GET',

        success: function () {

        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {
            alert('已完成整合点击报告下载进行预览')
        }
    })
}

//报告下载
function reportdownloadfunc() {
    window.open("/report_download_interface/", "_blank");
}

//ehole_finger报告预览
function eholefingerreportfunc() {
    window.open("/ehole_finger_report/", "_blank");
}


//启动EHole
function eholefingerfunc() {
    $.ajax({
        url: '/ehole_finger_scan/',
        method: 'GET',

        success: function (info) {
            alert(info.finger_status_result)

        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


//bbscan敏感信息扫描
function bbscaninfofunc() {
    $.ajax({
        url: '/bbscan_info_scan/',
        method: 'GET',

        success: function (info) {
            alert(info.bbscan_status_result)
        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}

//bbscan报告预览
function showbbscanreportfunc() {
    window.open("/showbbscanreport/", "_blank");
}


//子域名结果预览
function showsubdomainfunc() {
    window.open("/showsubdomainreport/");
}



//子域名探测
function subdomainfindfunc() {
    $.ajax({
        url: '/batch_show_subdomain/',
        method: 'GET',

        success: function (res) {
            console.log(res)
            console.log('子域名探测已开启稍后查看结果')
        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {
            alert('子域名探测已开启稍后查看结果')
        }
    })
}

//vulmap漏扫报告预览
function vulmapscanreportfunc() {
    window.open("/vulmapscanreport/");
}


//启动vulmap漏扫接口
function startvulmapscanfunc() {
    var vulnname = $('select[name="vulnname"]').val();
    $.ajax({
        url: '/startvulmapinterface/',
        method: 'POST',
        data: {
            vulnname: vulnname
        },
        success: function (info) {
            alert(info.vummap_scan_result)

        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


//批量端口扫描
function batchnmapportscanfunc() {
    $.ajax({
        url: '/startbatchnmapscan/',
        method: 'GET',

        success: function (info) {
            alert(info.nmap_status_result)

        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


//目标url的值赋值给 textarea 文本框
function targeturlcopytextareafunc() {
    // 定义一个函数来处理AJAX请求
    function fetchData() {
        $.ajax({
            url: '/url_list_textarea_show/',
            method: 'GET',
            success: function (info) {
                // 假设info.textvalue是一个数组  
                var textAreaContent = ''; // 初始化一个空字符串来保存textarea的内容  

                // 遍历info.textvalue数组，为每个元素添加换行符并追加到textAreaContent  
                for (var i = 0; i < info.textvalue.length; i++) {
                    textAreaContent += info.textvalue[i] + '\n'; // 追加元素和换行符  
                }

                // 将textAreaContent的内容赋值给textarea  
                $('#myTextarea').val(textAreaContent); // 假设textarea的id是myTextarea  
            },
            error: function () {


            },
            complete: function () {

            }
        })
    }

    // 调用fetchData函数初始化显示
    fetchData();
    // 设置定时器，每5000毫秒（5秒）执行一次fetchData函数
    var intervalId = setInterval(fetchData, 5000);
}

// 确保在页面卸载或组件销毁时清除定时器，以防止内存泄漏
window.addEventListener("beforeunload", function () {
    clearInterval(intervalId);
});



//afrog报告预览
function afrogreportfun() {
    window.open(ipvalue + ":15555/", "_blank");
}


//ceye dns记录
function ceyednsfunc() {
    window.open("/ceye_dns_record/", "_blank");
}

//ceye http记录
function ceyehttpfunc() {
    window.open("/ceye_http_record/", "_blank");
}

//ajax异步删除afrog报告
function deleteafrogreportfunc() {
    $.ajax({
        url: '/deleteafrogreport/',
        method: 'GET',
        success: function (res) {
            console.log(res)
            console.log('已删除afrog报告')
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {
            alert('已删除afrog报告')
        }
    })
}


//启动afrog漏扫接口
function startafrogfunc() {

    $.ajax({
        url: '/startafrogscanprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.start_afrog_result)
        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


//ajax异步关闭afrog进程
function killafrogprocessfunc() {
    $.ajax({
        url: '/killafrogprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_afrog_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//fscan扫描结果预览
function fscanreprtfunc() {
    window.open("/fscanreportyulan/");
}

//批量fscan漏洞扫描
function batchfscanvulnfunc() {
    $.ajax({
        url: '/startfcsaninterface/',
        method: 'GET',

        success: function (info) {
            alert(info.fscan_status_result)
        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


//ajax异步关闭fscan进程
function killfscanprocessfunc() {
    $.ajax({
        url: '/killfscangprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_fscan_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//shiro扫描结果预览
function shiroscanreprtfunc() {
    window.open("/shiro_report_show/");
}


//shiro漏洞扫描
function batchshirovulnfunc() {
    $.ajax({
        url: '/startshirointerface/',
        method: 'GET',

        success: function (info) {
            alert(info.shiro_status_result)

        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


//识别重点资产
function key_data_tiqu_func() {
    $.ajax({
        url: '/key_assets_withdraw/',
        method: 'GET',

        success: function (info) {
            alert(info.key_assets_result)
        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}

// 系统管理调整为5秒自动请求1次
function openModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "block";

    // 定义一个函数来处理AJAX请求
    function fetchData() {
        $.getJSON("/systemmanagement/",
            function (info) {
                document.getElementById("spp1").innerHTML = info.nmapstatus;
                document.getElementById("spp2").innerHTML = info.nucleistatus;
                document.getElementById("spp3").innerHTML = info.xraystatus;
                document.getElementById("spp4").innerHTML = info.radstatus;
                document.getElementById("spp5").innerHTML = info.dirscanstatus;
                document.getElementById("spp6").innerHTML = info.weblogicstatus;
                document.getElementById("spp7").innerHTML = info.struts2status;
                document.getElementById("spp8").innerHTML = info.bbscanstatus;
                document.getElementById("spp9").innerHTML = info.vulmapscanstatus;
                document.getElementById("spp10").innerHTML = info.afrogscanstatus;
                document.getElementById("spp11").innerHTML = info.fscanstatus;
                document.getElementById("spp12").innerHTML = info.shirostatus;
                document.getElementById("spp13").innerHTML = info.httpxstatus;
                document.getElementById("spp14").innerHTML = info.url_file_num;
                document.getElementById("spp15").innerHTML = info.eholestatus;
                document.getElementById("spp16").innerHTML = info.shiro_num;
                document.getElementById("spp17").innerHTML = info.springboot_num;
                document.getElementById("spp18").innerHTML = info.weblogic_num;
                document.getElementById("spp19").innerHTML = info.baota_num;
                document.getElementById("spp20").innerHTML = info.ruoyi_num;
                document.getElementById("spp21").innerHTML = info.struts2_num;
                document.getElementById("spp22").innerHTML = info.WordPress_num;
                document.getElementById("spp23").innerHTML = info.cpuinfo;
                document.getElementById("spp24").innerHTML = info.memoryinfo;
                document.getElementById("spp25").innerHTML = info.jboss_num;
                document.getElementById("spp26").innerHTML = info.key_asset_rule;
                document.getElementById("spp27").innerHTML = info.current_key_asset_num;
                document.getElementById("spp28").innerHTML = info.springbootstatus;
                document.getElementById("spp29").innerHTML = info.hydrastatus;
                document.getElementById("spp30").innerHTML = info.urlfinderstatus;
                document.getElementById("spp31").innerHTML = info.key_asset_rule_origin;
                document.getElementById("spp32").innerHTML = info.assets_status;
                document.getElementById("spp33").innerHTML = info.vuln_scan_status_shijianxian;
                document.getElementById("spp34").innerHTML = info.phpmyadmin_num;
                document.getElementById("spp35").innerHTML = info.disk_read;
                document.getElementById("spp36").innerHTML = info.disk_write;
                document.getElementById("spp37").innerHTML = info.infoinfostatus;
                document.getElementById("spp38").innerHTML = info.dirsub_sys_status;
                document.getElementById("spp39").innerHTML = info.xray_report_status;
                document.getElementById("spp40").innerHTML = info.urlfinder_report_status;
                document.getElementById("spp41").innerHTML = info.afrog_report_status;
                document.getElementById("spp42").innerHTML = info.ThinkPHP_num;
                document.getElementById("spp43").innerHTML = info.thinkphpstatus;
                document.getElementById("spp44").innerHTML = info.otx_status;
            });
    }

    // 调用fetchData函数初始化显示
    fetchData();

    // 设置定时器，每5000毫秒（5秒）执行一次fetchData函数
    var intervalId = setInterval(fetchData, 5000);
}

// 确保在页面卸载或组件销毁时清除定时器，以防止内存泄漏
window.addEventListener("beforeunload", function () {
    clearInterval(intervalId);
});



// 关闭系统管理
function closeModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "none";
}




// 查询fofa语法
function fofayufa() {
    var modal1 = document.getElementById("modal1");
    modal1.style.display = "block";

}

// 关闭查询语法
function closeModal1() {
    var modal1 = document.getElementById("modal1");
    modal1.style.display = "none";
}



//nuclei查看poc yaml文件
function nuclei_poc_show_func() {
    var poc_dir = $('select[name="poc_dir"]').val();
    $.ajax({
        url: '/nuclei_poc_show/',
        method: 'POST',
        data: {
            poc_dir: poc_dir
        },
        success: function (info) {
            $('#nucleibyid1').empty();
            for (var i = 0; i < info.nuclei_poc_list_global.length; i++) {
                $('#nucleibyid1').append('<option>' + info.nuclei_poc_list_global[i] + '</option><br>');
            }
            document.getElementById("nucleibyid2").innerHTML = info.nuclei_poc_list_len;
        },
        error: function () {

        },
        complete: function () {
        }
    })
}

// 资产管理展开
function assetmanagerzhankaifunc() {
    document.getElementById('assetid1').style.display = "block";
    document.getElementById('assetid3').style.display = "block";
    document.getElementById('assetid2').style.display = "none";
}


// 资产管理折叠
function assetmanagerzhediefunc() {
    document.getElementById('assetid1').style.display = "none";
    document.getElementById('assetid3').style.display = "none";
    document.getElementById('assetid2').style.display = "block";
}


// 漏洞管理展开
function vulnmanagerzhankaifunc() {
    document.getElementById('vulnid1').style.display = "block";
    document.getElementById('vulnid3').style.display = "block";
    document.getElementById('vulnid2').style.display = "none";
}


// 漏洞管理折叠
function vulnmanagerzhediefunc() {
    document.getElementById('vulnid1').style.display = "none";
    document.getElementById('vulnid3').style.display = "none";
    document.getElementById('vulnid2').style.display = "block";
}


//springboot报告预览
function springboot_report_show_func() {

    window.open("/springboot_report_show/");
}

//springboot漏洞扫描
function start_springboot_scan_func() {
    $.ajax({
        url: '/start_springboot_vuln_scan/',
        method: 'GET',

        success: function (info) {
            alert(info.springboot_scan_status_result)

        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


//ajax异步关闭nmap进程
function killnmapfunc() {
    $.ajax({
        url: '/killnmapprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_nmap_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}

//ajax异步关闭vulmap进程
function killvulmapfunc() {
    $.ajax({
        url: '/killvulmapprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_vulmap_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//ajax异步关闭nuclei进程
function killnucleifunc() {
    $.ajax({
        url: '/killnucleiprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_nuclei_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//ajax异步关闭bbscan进程
function killbbscanfunc() {
    $.ajax({
        url: '/killbbscanprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_bbscan_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//通过fofa收集资产
function fofa_search_assets_func() {
    var part = document.getElementById("inputfofaid").value;
    var num_fofa = $('select[name="num_fofa"]').val();
    $.ajax({
        url: '/fofa_search_assets_service/',
        method: 'POST',
        data: {
            part: part,
            num_fofa: num_fofa
        },
        success: function (info) {
            // 当请求成功时调用  
            alert(info.asset_len_list);

        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })

}


//hydra扫描报告预览
function hydra_report_show_func() {
    window.open("/hydra_report_show/", "_blank");
}


// 启用hydra扫描
function start_hydra_scan_func() {
    var hydrapart = $('select[name="hydrapart"]').val();
    $.ajax({
        url: '/start_hydra_interface/',
        method: 'POST',
        data: {
            hydrapart: hydrapart
        },
        success: function (info) {
            // 当请求成功时调用  
            alert(info.hydra_scan_result);
        },
        error: function () {
            alert('接口内部出错')
        },
        complete: function () {

        }
    })
}


//ajax异步关闭hydra进程
function killhydraprocessfunc() {
    $.ajax({
        url: '/killhydraprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_hydra_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//ajax异步关闭urlfinder进程
function killurlfinderprocessfunc() {
    $.ajax({
        url: '/killurlfinderprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_urlfinder_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//ajax异步关闭EHole进程
function killEHoleprocessfunc() {
    $.ajax({
        url: '/killEHoleprocess/',
        method: 'GET',
        success: function (info) {
            alert(info.kill_EHole_result)
        },
        error: function () {
            alert('出现内部错误')
        },
        complete: function () {

        }
    })
}


//总报告预览
function total_report_yulan_func() {
    window.open("/totalreportyulan/", "_blank");
}


// 登录接口
function login_interface_func() {
    var username = document.getElementById("user").value;
    var password = document.getElementById("pass").value;
    $.ajax({
        url: '/logininterface/',
        method: 'POST',
        data: {
            username: username,
            password: password
        },
        success: function (info) {
            if (confirm(info.loginstatus)) {
                window.location.href = info.redirect_url;
            } else {
                window.location.href = info.nologin;
            }
        },
        error: function () {
            alert('接口内部出错')
        },
        complete: function () {

        }
    })
}



// 重启服务接口
function restart_service_func() {

    $.ajax({
        url: '/restartsystemservice/',
        method: 'GET',

        success: function (info) {
            if (confirm(info.comfirm)) {
                info.infoscanstatus;
            }
        },
        // 重启服务中断会跳转到error处
        error: function (info) {
            alert("服务已重启相关配置已重新加载")
        },
        complete: function () {

        }
    })
}



// 关闭后端服务
function stopbackservicefunc() {
    $.ajax({
        url: '/stopbackserviceinterface/',
        method: 'GET',
        success: function (info) {
            // 参数1：确认操作
            // 参数2：取消操作
            if (confirm(info.backcomfirm)) {
                $.ajax({
                    url: '/confirm_stop_service/',
                    method: 'POST',
                    data: {
                        action: 1
                    },
                    success: function (info) {
                        alert(info.result_status)
                        window.location.href = "/index/";
                    },
                    error: function () {
                        alert('内部出错');
                    }
                });
            } else {

                $.ajax({
                    url: '/confirm_stop_service/',
                    method: 'POST',
                    data: {
                        action: 2
                    },
                    success: function (info) {
                        alert(info.result_status)
                        window.location.href = "/index/";
                    },
                    error: function () {
                        alert('内部出错');
                    }
                });

            }

        },
        // 关闭所有服务nginx会返回502
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


// 弹出编辑筛选规则页面
function shuaixuanrule() {
    var idp1 = document.getElementById("idp1");
    idp1.style.display = "block";

}

// 隐藏编辑筛选规则页面
function fanhuishuaixuanrule() {
    var idp1 = document.getElementById("idp1");
    idp1.style.display = "none";

}


// 新增重点资产筛选规则
function add_rule_func() {
    var rule = document.getElementById("rule_input_id1").value;
    $.ajax({
        url: '/add_point_rule_interface/',
        method: 'POST',
        data: {
            rule: rule
        },
        success: function (info) {
            alert(info.result_rule)
        },

        error: function (info) {
            alert("内部出错")
        },
        complete: function () {

        }
    })
}


// 通过规则名称删除重点资产筛选规则
function delete_rule_func() {
    var rule = document.getElementById("rule_input_id1").value;
    $.ajax({
        url: '/delete_point_rule_interface/',
        method: 'POST',
        data: {
            rule: rule,
            key: 1
        },
        success: function (info) {
            alert(info.delete_rule)
        },

        error: function (info) {
            alert("内部出错")
        },
        complete: function () {

        }
    })
}


// 清空重点资产筛选规则表
function delete_rule_all_func() {
    var rule = document.getElementById("rule_input_id1").value;
    $.ajax({
        url: '/delete_point_rule_interface/',
        method: 'POST',
        data: {
            rule: rule,
            key: 2
        },
        success: function (info) {
            alert(info.delete_rule)
        },

        error: function (info) {
            alert("内部出错")
        },
        complete: function () {

        }
    })
}

//一键完成重点资产扫描
function one_click_scan_func() {
    $.ajax({
        url: '/one_click_scan/',
        method: 'GET',

        success: function (info) {
            alert(info.shiro_status_result + "\n" + info.springboot_status_result + "\n" + info.struts2_status_result + "\n" + info.weblogic_status_result + "\n")
        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


// 一键预览所有报告
function one_click_preview_all_report_finc() {
    window.open("/showsubdomainreport/");
    window.open("/showbbscanreport/");
    window.open("/ehole_finger_report/");
    window.open("/nmapresultshow/");
    window.open("/weblogic_poc_report/");
    window.open("/vulmapscanreport/");
    window.open("/struts2_poc_report/");
    window.open("/fscanreportyulan/");
    window.open("/shiro_report_show/");
    window.open("/hydra_report_show/");
    window.open("/springboot_report_show/");
    window.open(ipvalue + ":18888/");
    window.open(ipvalue + ":16666/");
    window.open(ipvalue + ":15555/");
}


// 操作按钮提示语，延迟0.5秒显示和隐藏
function caozuo1func() {
    setTimeout(function () {
        var tishisp1 = document.getElementById("tishisp1");
        tishisp1.style.display = "block";
    }, 500);
}

function caozuo11func() {
    setTimeout(function () {
        var tishisp1 = document.getElementById("tishisp1");
        tishisp1.style.display = "none";
    }, 500);
}


function caozuo2func() {
    setTimeout(function () {
        var tishisp2 = document.getElementById("tishisp2");
        tishisp2.style.display = "block";
    }, 500);
}

function caozuo22func() {
    setTimeout(function () {
        var tishisp2 = document.getElementById("tishisp2");
        tishisp2.style.display = "none";
    }, 500);
}

function caozuo3func() {
    setTimeout(function () {
        var tishisp3 = document.getElementById("tishisp3");
        tishisp3.style.display = "block";
    }, 500);
}

function caozuo33func() {
    setTimeout(function () {
        var tishisp3 = document.getElementById("tishisp3");
        tishisp3.style.display = "none";
    }, 500);
}

function caozuo4func() {
    setTimeout(function () {
        var tishisp4 = document.getElementById("tishisp4");
        tishisp4.style.display = "block";
    }, 500);
}

function caozuo44func() {
    setTimeout(function () {
        var tishisp4 = document.getElementById("tishisp4");
        tishisp4.style.display = "none";
    }, 500);
}


function caozuo5func() {
    setTimeout(function () {
        var tishisp5 = document.getElementById("tishisp5");
        tishisp5.style.display = "block";
    }, 500);
}

function caozuo55func() {
    setTimeout(function () {
        var tishisp5 = document.getElementById("tishisp5");
        tishisp5.style.display = "none";
    }, 500);
}

function caozuo6func() {
    setTimeout(function () {
        var tishisp6 = document.getElementById("tishisp6");
        tishisp6.style.display = "block";
    }, 500);
}

function caozuo66func() {
    setTimeout(function () {
        var tishisp6 = document.getElementById("tishisp6");
        tishisp6.style.display = "none";
    }, 500);
}

function caozuo7func() {
    setTimeout(function () {
        var tishisp7 = document.getElementById("tishisp7");
        tishisp7.style.display = "block";
    }, 500);
}

function caozuo77func() {
    setTimeout(function () {
        var tishisp7 = document.getElementById("tishisp7");
        tishisp7.style.display = "none";
    }, 500);
}

function caozuo8func() {
    setTimeout(function () {
        var tishisp8 = document.getElementById("tishisp8");
        tishisp8.style.display = "block";
    }, 500);
}

function caozuo88func() {
    setTimeout(function () {
        var tishisp8 = document.getElementById("tishisp8");
        tishisp8.style.display = "none";
    }, 500);
}


function caozuo9func() {
    setTimeout(function () {
        var tishisp9 = document.getElementById("tishisp9");
        tishisp9.style.display = "block";
    }, 500);
}

function caozuo99func() {
    setTimeout(function () {
        var tishisp9 = document.getElementById("tishisp9");
        tishisp9.style.display = "none";
    }, 500);
}


function caozuo9afunc() {
    setTimeout(function () {
        var tishisp9a = document.getElementById("tishisp9a");
        tishisp9a.style.display = "block";
    }, 500);
}

function caozuo99afunc() {
    setTimeout(function () {
        var tishisp9a = document.getElementById("tishisp9a");
        tishisp9a.style.display = "none";
    }, 500);
}


function caozuo9bfunc() {
    setTimeout(function () {
        var tishisp9b = document.getElementById("tishisp9b");
        tishisp9b.style.display = "block";
    }, 500);
}

function caozuo99bfunc() {
    setTimeout(function () {
        var tishisp9b = document.getElementById("tishisp9b");
        tishisp9b.style.display = "none";
    }, 500);
}

function caozuo9cfunc() {
    setTimeout(function () {
        var tishisp9c = document.getElementById("tishisp9c");
        tishisp9c.style.display = "block";
    }, 500);
}

function caozuo99cfunc() {
    setTimeout(function () {
        var tishisp9c = document.getElementById("tishisp9c");
        tishisp9c.style.display = "none";
    }, 500);
}

// 文本框重置
function textareachongzhifunc() {
    var myTextarea = document.getElementById("myTextarea");
    myTextarea.value = "";
}


//thinkphp漏洞扫描
function startthinkphpscanfunc() {
    $.ajax({
        url: '/starttpscaninterface/',
        method: 'GET',

        success: function (info) {
            alert(info.thinkphp_status_result)

        },
        error: function () {
            alert('内部出错')
        },
        complete: function () {

        }
    })
}


//thinkphp报告预览
function thinkphp_report_show_func() {

    window.open("/thinkphp_poc_report/");
}


// 漏洞扫描工具集合
function xianshipointfunc() {
    var pointid1 = document.getElementById("pointid1");
    pointid1.style.display = "block";

    var spanpointvalue = $('select[name="spanpointvalue"]').val();
    if (spanpointvalue == 1) {

        var point1 = document.getElementById("point1");
        point1.style.display = "block";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";

    } else if (spanpointvalue == 2) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "block";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";

    } else if (spanpointvalue == 3) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "block";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";

    } else if (spanpointvalue == 4) {

        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "block";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    } else if (spanpointvalue == 6) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "block";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";

    } else if (spanpointvalue == 7) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "block";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    } else if (spanpointvalue == 8) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "block";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    } else if (spanpointvalue == 9) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "block";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    } else if (spanpointvalue == 10) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "block";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    } else if (spanpointvalue == 11) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "block";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    } else if (spanpointvalue == 12) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "block";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    } else if (spanpointvalue == 13) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "block";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    } else if (spanpointvalue == 14) {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "none";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "block";
    }
    else {
        var point1 = document.getElementById("point1");
        point1.style.display = "none";
        var point2 = document.getElementById("point2");
        point2.style.display = "none";
        var point3 = document.getElementById("point3");
        point3.style.display = "none";
        var point4 = document.getElementById("point4");
        point4.style.display = "none";
        var point5 = document.getElementById("point5");
        point5.style.display = "block";
        var point6 = document.getElementById("point6");
        point6.style.display = "none";
        var point7 = document.getElementById("point7");
        point7.style.display = "none";
        var point8 = document.getElementById("point8");
        point8.style.display = "none";
        var point9 = document.getElementById("point9");
        point9.style.display = "none";
        var point10 = document.getElementById("point10");
        point10.style.display = "none";
        var point11 = document.getElementById("point11");
        point11.style.display = "none";
        var point12 = document.getElementById("point12");
        point12.style.display = "none";
        var point13 = document.getElementById("point13");
        point13.style.display = "none";
        var point14 = document.getElementById("point14");
        point14.style.display = "none";
    }
}


function guanbipointfunc() {
    var point1 = document.getElementById("point1");
    point1.style.display = "block";
    var point2 = document.getElementById("point2");
    point2.style.display = "none";
    var point3 = document.getElementById("point3");
    point3.style.display = "none";
    var point4 = document.getElementById("point4");
    point4.style.display = "none";
    var point5 = document.getElementById("point5");
    point5.style.display = "none";
    var point6 = document.getElementById("point6");
    point6.style.display = "none";
    var point7 = document.getElementById("point7");
    point7.style.display = "none";
    var point8 = document.getElementById("point8");
    point8.style.display = "none";
    var point9 = document.getElementById("point9");
    point9.style.display = "none";
    var point10 = document.getElementById("point10");
    point10.style.display = "none";
    var point11 = document.getElementById("point11");
    point11.style.display = "none";
    var point12 = document.getElementById("point12");
    point12.style.display = "none";
    var point13 = document.getElementById("point13");
    point13.style.display = "none";
    var point14 = document.getElementById("point14");
    point14.style.display = "none";
}
