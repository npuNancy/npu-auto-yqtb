import re
import sys
import time
import json
import requests
import traceback
from datetime import datetime
# from rtx_helper import RTXHelper


def pushplus(msg: str, pushplus_token):
    if pushplus_token == "":
        return
    pushplus_url = 'http://www.pushplus.plus/send'
    data = {
        'token': pushplus_token,
        'title': msg,
        'content': msg,
        'template': 'json'
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(pushplus_url, data=body, headers=headers)


def yqtb(username, password, name, params):
    session = requests.session()
    url = "https://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp"
    post_url = "https://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp"
    login_url = "https://uis.nwpu.edu.cn/cas/login"
    login_data = {
        # 学号
        'username': username,
        # 密码
        'password': password,
        'currentMenu': '1',
        'execution': 'e1s1',
        "_eventId": "submit"
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    response = session.get(login_url, headers=header)
    execution = re.findall(r'name="execution" value="(.*?)"', response.text)[0]
    login_data['execution'] = execution
    response = session.post(login_url, data=login_data, headers=header)
    if "欢迎使用" in response.text:
        print(f"{name} login successfully")
    else:
        print(f"{name} login unsuccessfully")
        exit(1)
    res = ""
    for i in range(3):
        if len(res) == 0:
            response = session.get("https://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp")
            response = session.get("https://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp")
            pattern = r"url:'ry_util\.jsp\?sign=(.*).*'"
            res = re.findall(pattern, response.text)
    # print('res:' + str(res))
    if len(res) == 0:
        print("error in script, please contact to the author")
        exit(1)
    time.sleep(1)
    post_url += "?sign=" + res[0]
    html = session.get(url)
    time.sleep(1)
    session.headers.update({'referer': 'https://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp'})
    time.sleep(1)
    html = session.post(post_url, data=params, headers=header)
    result = '{"state":"1"}' in html.text
    if result:
        print(f"{name} 疫情填报成功")
    else:
        print(f"{name} 疫情填报失败!!")


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def tianbao(list, params):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "疫情填报脚本开始运行")
    try:
        params_u = params.copy()
        type = list[3]
        # 设置0为在学校，1为在家
        if type == '1':
            params_u['szcsbm'] = list[4]
            params_u['szcsmc'] = list[5]
        params_u['userLoginId'] = list[0]
        params_u['userName'] = list[2]
        yqtb(list[0], list[1], list[2], params_u)
        print(f'{list[2]} 疫情填报成功')
        pushplus(f'{list[2]} 疫情填报成功', list[6])
    except:
        print(f'{get_now()}\n {list[2]}疫情填报出现异常，详情：\n {traceback.format_exc()}')
        pushplus("疫情填报失败！！！查看log", list[6])


class Params:
    params_school = {
        # 是否核酸检测
        "hsjc": "1",
        # 西安市一码通，对应1-3，绿为1
        "xasymt": "1",
        "actionType": "addRbxx",
        # 学号，这里从list中拿，不用改
        "userLoginId": 'username',
        # 所在城市编码，学校为1
        "szcsbm": "1",
        "bdzt": "1",
        # 所在城市名称：在学校
        "szcsmc": "在学校",
        # 体温范围，从上到下依次对应0-3
        "sfyzz": "0",
        # 有无疑似症状（可多选），无对应0，发热对应1，胸闷对应6，咳嗽对应7.其他对应8
        "sfqz": "0",
        "tbly": "sso",
        # 其他情况说明
        "qtqksm": "",
        # 疑似情况说明
        "ycqksm": "",
        "userType": "2",
        "sfjkqk": "0",
        # 隔离情况
        "glqk": "0",
        # 姓名，这里从list中拿，不用改
        "userName": 'name'
    }
    params_home = {
        # 是否核酸检测
        "hsjc": "1",
        # 西安市一码通，对应1-3，绿为1
        "xasymt": "1",
        "actionType": "addRbxx",
        # 学号，这里从list中拿，不用改
        "userLoginId": 'username',
        # 所在城市编码，一般为身份证前六位
        "szcsbm": "330682",
        "bdzt": "1",
        # 家庭所在地，示例：xx省xx市xxx，具体参见疫情填报
        "szcsmc": "浙江省绍兴市上虞市",
        # 体温范围，从上到下依次对应0-3
        "sfyzz": "0",
        # 有无疑似症状（可多选），无对应0，发热对应1，胸闷对应6，咳嗽对应7.其他对应8
        "sfqz": "0",
        "tbly": "sso",
        # 其他情况说明
        "qtqksm": "",
        # 疑似情况说明
        "ycqksm": "",
        "userType": "2",
        "sfjkqk": "0",
        # 隔离情况
        "glqk": "0",
        # 姓名，这里从list中拿，不用改
        "userName": 'name'
    }


if __name__ == '__main__':
    with open("config.json", 'r', encoding='utf-8') as f:
        users = json.load(f)
    for user in users:
        info_list = list(user.values())
        params_type = Params.params_home if user["is_home"] == "1" else Params.params_school

        '''
        https://gitee.com/ju-xiang/nwpuyqtb
        前一个参数为列表，参考上面的list示例
        后一个参数为想填报的信息，在学校选择params_school，在家选择prams_home，具体参数参见注释，不定期更新
        '''
        tianbao(info_list, params_type)
