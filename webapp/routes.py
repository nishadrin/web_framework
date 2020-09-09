import abc


ROUTES = dict()

def add_route(path: str):
    def decorator(cls):
        ROUTES[path] = cls

        return cls
    return decorator
