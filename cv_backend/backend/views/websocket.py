import uuid

from django.http import HttpResponse, JsonResponse, FileResponse
from dwebsocket.decorators import *
from rest_framework.decorators import api_view

'''!------------------------WEBSOCKET--------------------------------!'''
clients = {}  # 创建客户端列表，存储所有在线客户端


# websocket链接 请求互动
@accept_websocket
def link(request):
    # 判断是不是ws请求
    if request.is_websocket():
        userid = str(uuid.uuid4())
        while True:
            message = request.websocket.wait()
            if not message:
                break
            else:
                print("客户端链接成功：" + str(message, encoding="utf-8"))
                # 保存客户端的ws对象，以便给客户端发送消息,每个客户端分配一个唯一标识
                clients[userid] = request.websocket


# 发送互动弹幕
def send(request):
    # 获取消息
    msg = request.POST.get("msg")
    # 获取到当前所有在线客户端，即clients
    # 遍历给所有客户端推送消息
    print('request:', request)
    print('request.data:', request.POST)
    if msg:
        for client in clients:
            clients[client].send(msg.encode('utf-8'))
        return HttpResponse({"msg": "success"})
    else:
        HttpResponse('发送格式错误')


def refresh():
    msg = 'refresh'
    for client in clients:
        clients[client].send(msg.encode('utf-8'))
    return HttpResponse('已让所有客户端刷新')
