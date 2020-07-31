def slash_endswith(request):
    if not request['PATH_INFO'].endswith('/'):
        request['PATH_INFO'] += '/'
