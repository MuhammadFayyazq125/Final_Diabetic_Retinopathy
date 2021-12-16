from django.http import HttpResponse
from django.shortcuts import redirect

def authorized_access(view_func):
	def user_function(request, *args, **kwargs):
		if request.user.is_authenticated:
			redirect('display')
		else:
			return view_func(request, *args, **kwargs)
	return user_function

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'normal':
            return redirect('display')
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return # <- return response here (possibly a redirect to login page?)d
    return wrapper_function


def unauthenticated_user(view_func):
    def wrapper_func(request, *args , **kwargs):
        if request.user.is_authenticated:
            return redirect('display')
        else:
            return view_func(request, *args , **kwargs)
    return wrapper_func

def allowed_user(allowed_roles=[]):
    def au(view_func):
        def wrapper_func(request,*args,**kwargs):
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:                                 
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("you are not authorized User to access this page")
        return wrapper_func
    return au