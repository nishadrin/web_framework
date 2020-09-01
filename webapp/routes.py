import abc


ROUTES = dict()

def add_route(path: str) -> None:
    def decorator(cls):
        ROUTES[path] = cls

        return cls
    return decorator
