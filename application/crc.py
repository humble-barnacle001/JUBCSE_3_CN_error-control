from time import time_ns
from typing import Tuple, Type


def crc_verify(data: str, poly: str) -> "Tuple[Type[int],Type[bool], Type[str]]":
    t0 = time_ns()
    check_value = data[-len(poly)+1:]
    data = data[:-len(poly)+1]
    poly = poly.lstrip('0')
    len_input = len(data)
    initial_padding = check_value
    input_padded_array = list(data + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(poly)):
            input_padded_array[cur_shift + i] \
                = str(int(poly[i] != input_padded_array[cur_shift + i]))
    return ((time_ns()-t0)//1000, '1' not in ''.join(input_padded_array)[len_input:], "")
