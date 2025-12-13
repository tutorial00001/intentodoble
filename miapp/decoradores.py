from django.shortcuts import redirect
from functools import wraps

def login_requerido(vista_funcion):
    @wraps(vista_funcion)
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")
        
        try:
            response = vista_funcion(request, *args, **kwargs)
        except TypeError as e:
            
            if "username" in kwargs:
                
                kwargs.pop('username', None)
                response = vista_funcion(request, *args, **kwargs)
            else:
                raise e
        
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response
    return wrapper