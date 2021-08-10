from time import time_ns
from typing import Tuple, Type


def lrc_verify(data: str, bits: int) -> "Tuple[Type[int],Type[bool], Type[str]]":
    t0 = time_ns()
    r = [data[i*bits: (i+1)*bits] for i in range(len(data)//bits)]

    mx = 2**bits-1
    ps = sum(map(lambda x: int(x, 2), r))

    return ((time_ns()-t0)//1000, (ps & mx) == 0, "")
