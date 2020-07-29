def secret_middleware(request):
    request['token'] = 'secret_key'
