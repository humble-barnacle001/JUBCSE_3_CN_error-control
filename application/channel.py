from random import randint
from typing import Callable, List, Type


def bit_flip(data: str) -> str:
    ndata: str = bin(int(data, 2) ^ (2**len(data)-1))[2:]

    return ("0"*(len(data)-len(ndata)))+ndata


def bit_error(data: str) -> str:
    x = randint(0, len(data)-1)
    data = data[:x]+bit_flip(data[x])+data[x+1:]
    return data


def burst_error(data: str) -> str:
    x = randint(0, len(data)-2)
    y = randint(1, len(data)-1-x)
    data = data[:x]+bit_flip(data[x:x+y])+data[x+y:]
    return data


def random_error(data: str) -> str:
    a = randint(0, 9)
    t = [bit_error, burst_error]
    for _ in range(a):
        data = t[randint(0, 1)](data)
    return data


def errorify(data, fields: List[str], err_func: Callable[[str], str]):

    for x in fields:
        data[x]["data"] = err_func(data[x]["data"])

    return data


def channel(client_data):
    err_types = ["None", bit_error, burst_error, random_error]
#     err_types = ["None", burst_error]
    fields = ["vrc", "lrc", "crc", "cks"]
    ch = randint(0, len(err_types)-1)
    error_type = err_types[ch]
    data = client_data
    if(ch == 0):
        pass
    else:
        try:
            data = errorify(data, fields, error_type)
        except Exception as e:
            print("Exception", e)
        error_type = (error_type.__name__)[:-6]

    return (error_type, data)

