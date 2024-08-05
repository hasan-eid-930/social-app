import functools
from django.shortcuts import get_object_or_404


def like_toggle(model_class):
    def decorator_like(func):
        @functools.wraps(func)
        def wrapper_like(request,*args, **kwargs):
            model=get_object_or_404(model_class, id=kwargs.get('pk'))
            # prevent user from liking thier post 
            if request.user != model.author:
                # check if current user likes the post befor
                if model.likes.filter(id=request.user.id).exists():
                    model.likes.remove(request.user)
                else:
                    model.likes.add(request.user)
            value = func(request,model)
            return value
        return wrapper_like
    return decorator_like