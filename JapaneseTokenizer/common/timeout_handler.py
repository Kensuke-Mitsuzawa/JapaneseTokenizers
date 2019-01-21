#! -*- coding: utf-8 -*-
from functools import wraps


class TimeoutException(Exception):
    pass


def handler_func(msg):
    raise TimeoutException()


def on_timeout(limit, handler=handler_func, hint=None):
    """
    指定した実行時間に終了しなかった場合、handlerをhint/limitを引数にして呼び出します
    @on_timeout(limit=3600, handler=notify_func, hint=u'長い計算')
    def long_time_function():
    """
    def notify_handler(signum, frame):
        handler("'%s' is not finished in %d second(s)." % (hint, limit))

    def __decorator(function):
        def __wrapper(*args, **kwargs):
            import signal
            signal.signal(signal.SIGALRM, notify_handler)
            signal.alarm(limit)
            result = function(*args, **kwargs)
            signal.alarm(0)
            return result
        return wraps(function)(__wrapper)
    return __decorator
