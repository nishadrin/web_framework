from datetime import datetime


def debug():
    def decorator(func):
        def decorated_func(*args, **kwargs):
            print(f"- Running '{func.__name__}' on {datetime.now()}")
            result = func(*args, **kwargs)

            return result
        return decorated_func
    return decorator
