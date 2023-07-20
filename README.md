# dynamic_pcre2
Dynamically linking pcre2 library to python project

Tested on Ubuntu 22.04

# Before using

check exported functions:
~~~
nm -D /usr/lib/x86_64-linux-gnu/libpcre2-8.so.0

find / -name "libpcre2-8*"
apt search libpcre2-8
apt install -y libpcre2-8-0
~~~


# Using
~~~
import pcre2_dynamic
import ctypes

subject = "1234 asdfg Liam 9876"
pattern_case_insesitive = "(?i)Jack|Noah|Liam"
pattern_bytes = pattern_case_insesitive.encode("utf-8")
compiled_pattern=PCRE2.pcre2_compile_8(pattern_bytes,
                                ctypes.c_size_t(len(pattern_bytes)),
                                pcre2_dynamic.PCRE2_ZERO_TERMINATED,
                                ctypes.byref(ctypes.c_int()),
                                ctypes.byref(ctypes.c_size_t()),
                                None)
PCRE2.pcre2_jit_compile_8(compiled_pattern, ctypes.c_uint32(0x1))

start, end = preg_match(compiled_pattern, subject)
if start > -1:
    print(f"found {subject[start:end]}")

PCRE2.pcre2_code_free_8(compiled_pattern)
~~~

