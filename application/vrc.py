from time import time_ns
from typing import Tuple, Type


def vrc_verify(data: str, parity: str) -> "Tuple[Type[int],Type[bool], Type[str]]":
    t0 = time_ns()
    return ((time_ns()-t0)//1000, data.count("1") % 2 == (0 if parity == "Even" else 1), "")
