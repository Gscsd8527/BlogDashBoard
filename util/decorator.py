from django.http import HttpResponseRedirect
from functools import wraps

# 登录限制的装饰器
def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id', False):
            return func(request, *args, **kwargs)
        else:
            next = request.get_full_path()
            red = HttpResponseRedirect('?next=' + next)
            return red
    return wrapper
