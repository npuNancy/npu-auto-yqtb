import re
import sys
import time
import requests
import traceback
from datetime import datetime
# from rtx_helper import RTXHelper


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
        print(name + "login successfully")
    else:
        print(name + "login unsuccessfully")
        exit(1)
    res = ""
    for i in range(3):
        if len(res) == 0:
            response = session.get("https://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp")
            response = session.get("https://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp")
            pattern = r"url:'ry_util\.jsp\?sign=(.*).*'"
            res = re.findall(pattern, response.text)
    print('res:' + str(res))
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
        print(name + "疫情填报成功\n")
    else:
        print(name + "疫情填报失败\n")


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def tianbao(list, params):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "疫情填报脚本开始运行")
    x = 0
    msg = ''
    for i in list:
        try:
            type = ''
            params_u = params.copy()
            type = i[3]
            # 设置0为在学校，1为在家
            if type == '1':
                params_u['szcsbm'] = i[4]
                params_u['szcsmc'] = i[5]
            params_u['userLoginId'] = i[0]
            params_u['userName'] = i[2]
            yqtb(i[0], i[1], i[2], params_u)
            msg = msg + f'\n{i[2]}疫情填报成功'
        except:
            x = x + 1
            # tianbao(list, params)
            print(f'{get_now()}\n {i[2]}疫情填报出现异常，详情：\n {traceback.format_exc()}')
            # RTXHelper.send_rtx_with_raw_data_all(f'{get_now()}\n {i[2]}疫情填报出现异常，详情：\n {traceback.format_exc()}')
            # print(traceback.format_exc())
    if x == 0:
        # RTXHelper.send_rtx_with_raw_data(f'{get_now()}{msg}')
        print("疫情填报脚本运行成功\n")
    else:
        print('疫情填报脚本出现异常,具体查看log\n')


class params:
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


class lists:
    yxk_list = [
        # 第三个参数0就是在学校，其他就是自定义
        # ['学号', '密码', '姓名', '0', 'szcsbm', 'xx省xx市xxx'],
        ['2022202661', 'npu991226YAn.', '严笑凯', '1', '330682', '浙江省绍兴市上虞市']
    ]
    wj_list = [
        # 第三个参数0就是在学校，其他就是自定义
        # ['学号', '密码', '姓名', '0', 'szcsbm', 'xx省xx市xxx'],
        ['2019302961', '555793lfw@', '王珏', '1', '330682', '浙江省绍兴市上虞市']
    ]


if __name__ == '__main__':
    '''
    https://gitee.com/ju-xiang/nwpuyqtb
    前一个参数为列表，参考上面的list示例
    后一个参数为想填报的信息，在学校选择params_school，在家选择prams_home，具体参数参见注释，不定期更新
    '''
    tianbao(lists.yxk_list, params.params_home)
    tianbao(lists.wj_list, params.params_home)
