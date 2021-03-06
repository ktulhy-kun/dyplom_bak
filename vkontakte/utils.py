from datetime import datetime
import os

import sys
from typing import Iterable

# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())


def extend_nested_list(l: list) -> Iterable:
    for item in l:
        if isinstance(item, list):
            yield from extend_nested_list(item)
        else:
            yield item


class MetaEnv(type):
    """
    Мета класс для Env
    Класс достёт из os.environ значения переменных
    """
    _cache = {}

    @classmethod
    def clear_cache(mcs):
        mcs._cache = {}

    @classmethod
    def __getattr__(mcs, item):
        if item not in mcs._cache:
            mcs._cache[item] = os.environ[item]
            try:
                mcs._cache[item] = int(mcs._cache[item])
            except ValueError:
                pass

        return mcs._cache[item]


class Env(object, metaclass=MetaEnv):
    pass


def print_line(*args, **kwargs):
    print("\r", end='')
    print(*args, **kwargs, end='')
    sys.stdout.flush()


def parse_date(s: str):
    if not s:
        return None
    try:
        dt = datetime.strptime(s, "%d.%m.%Y")
    except ValueError:
        s += ".1904"
        dt = datetime.strptime(s, "%d.%m.%Y")
    return dt


if '__main__' == __name__:
    print(Env.PYTHONUNBUFFERED)
    assert Env.PYTHONUNBUFFERED == 1
    Env.clear_cache()
    assert Env.PYTHONUNBUFFERED == 1
