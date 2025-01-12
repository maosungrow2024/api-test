import requests
import time
import math
import random
import string
import json

import pandas as pd

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from base64 import b64encode



# 配置请求参数
REQ_CONFIG = {
    'username': 's.mao@sungrow-emea.com',
    'password': 'QUcv8q8^77u#!',
    'appkey': 'A12BA0CD65EECFB33DC79841118C7268',
    'x_access_key': '4924f0931e50f51267433bd29225ed16',
    'domain': 'apieu.suncharger.cn'
}


# 生成随机32位字符串
def generate_nonce(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# 获取当前UNIX时间戳（毫秒）
def current_timestamp():
    return int(time.time() * 1000)


# 获取身份认证的token
def get_token(req_config):
    # 获取请求配置参数
    username = req_config.get('username')
    password = req_config.get('password')
    appkey = req_config.get('appkey')
    x_access_key = req_config.get('x_access_key')
    api_domain = req_config.get('domain')
    # 生成必要数值
    url = f"https://{api_domain}/openapi/v1/auth"
    nonce = generate_nonce()
    timestamp = current_timestamp()
    # 请求体
    auth_request = {
        "nonce": nonce,
        "data": {
            "userAccount": username,
            "password": password
        },
        "timestamp": timestamp,
        "appkey": appkey,
        "lang": "_en_US"
    }
    # 请求头
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'x-client-tz': 'GMT+8',
        'x-access-key': x_access_key
    }
    # 响应
    response = requests.post(url, headers=headers, json=auth_request)
    
    if response.status_code == 200:
        return response.json().get('data').get('token')
    else:
        print(f"身份认证失败: {response.text}")
        return None



# 查询场站列表
def get_station_list(token, req_config):
    # 获取请求配置参数
    appkey = req_config.get('appkey')
    x_access_key = req_config.get('x_access_key')
    api_domain = req_config.get('domain')
    # 生成必要数值
    url = f'https://{api_domain}/openapi/v1/getStationList'
    nonce = generate_nonce()
    timestamp = str(int(time.time() * 1000))
    # 请求体
    station_request = {
        "nonce": nonce,
        "data": {
            "curPage": 1,
            "size": 10,
            "stationStatus": "WORKING"  # 根据需求修改过滤条件
        },
        "timestamp": timestamp,
        "token": token,
        "appkey": appkey,
        "lang": "_en_US"
    }
    # 请求头
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'x-client-tz': 'GMT+8',
        'x-access-key': x_access_key
    }
    # 反馈
    response = requests.post(url, headers=headers, json=station_request)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"查询场站列表失败: {response.text}")
        return None




# 主程序
if __name__ == "__main__":

    token = get_token(REQ_CONFIG)
    
    if token:
        station_list_response = get_station_list(token, REQ_CONFIG)
        print("场站列表响应:", station_list_response)