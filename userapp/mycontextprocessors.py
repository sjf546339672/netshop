# coding: utf-8
"""定义全局上下文，所有模板页面都可以共享字典里面的数据"""


def getUserInfo(request):
    return {"suser": request.session.get("user", None)}





