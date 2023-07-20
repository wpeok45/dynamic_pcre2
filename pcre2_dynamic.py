import ctypes
from ctypes.util import find_library

PCRE2_ZERO_TERMINATED = ctypes.c_uint32(0)

shared_object_name = find_library('pcre2')
#  if no alias, go directly
if shared_object_name is None:
    # docker image: python 3.10+, already contains these lib
    shared_object_name = 'libpcre2-8.so.0'
                          
PCRE2 = ctypes.CDLL(shared_object_name)
PCRE2.pcre2_compile_8.restype=ctypes.POINTER(ctypes.c_char)
PCRE2.pcre2_match_data_create_8.restype=ctypes.POINTER(ctypes.c_char)
PCRE2.pcre2_get_ovector_pointer_8.restype=ctypes.POINTER(ctypes.c_size_t*2)


def preg_match(compiled_pattern, subj: str):
    # http://pcre.org/current/doc/html/pcre2jit.html#TOC1
    start = -1
    end = -1

    subject = subj.encode("utf-8")

    try:
        match_data=PCRE2.pcre2_match_data_create_8(ctypes.c_uint32(1), None)
        ov_ptr=PCRE2.pcre2_get_ovector_pointer_8(match_data)
        ov_ptr.contents[1] = 0

        result = PCRE2.pcre2_jit_match_8(compiled_pattern, subject,
                                ctypes.c_size_t(len(subject)),
                                ctypes.c_size_t(ov_ptr.contents[1]),
                                PCRE2_ZERO_TERMINATED,
                                match_data,
                                None)
        if result > -1:
            start = ov_ptr.contents[0]
            end = ov_ptr.contents[1]
        PCRE2.pcre2_match_data_free_8(match_data)
        
    except Exception as e:
        print(f"ERROR: preg_match, pattern:{compiled_pattern}, subject:{subject}, {e.with_traceback(None)}")
        return -1
    
    return start, end

if __name__ == '__main__':
    import time
    import string
    import random
    subjects = []
    print("Generating sentences...")
    for _ in range(100000):
        subjects.append(''.join(random.choices(string.ascii_letters + '          ', k=10)))

    #pattern_case_insesitive = "(?i)Jack|Noah|Liam|Isla|Mary|Luke|Levi|Owen|Jose|Adam|Ryan|Evan|Ezra|Jace"
    pattern = "Jack|Noah|Liam|Isla|Mary|Luke|Levi|Owen|Jose|Adam|Ryan|Evan|Ezra|Jace"
  
    pattern_bytes = pattern.encode("utf-8")
    compiled_pattern=PCRE2.pcre2_compile_8(pattern_bytes,
                                    ctypes.c_size_t(len(pattern_bytes)),
                                    PCRE2_ZERO_TERMINATED,
                                    ctypes.byref(ctypes.c_int()),
                                    ctypes.byref(ctypes.c_size_t()),
                                    None)
    PCRE2.pcre2_jit_compile_8(compiled_pattern, ctypes.c_uint32(0x1))

    print("Start search...")
    found = 0
    start_time = time.time()
    for i in range (len(subjects)):
        start, end = preg_match(compiled_pattern, subjects[i])
        if start > -1:
            print(f"Line: {i}, found {subjects[i][start:end]}, in '{subjects[i]}'")
            found += 1


   

    print(f"\nComplete: found {found}, duration {round(time.time() - start_time, 3)} sec.")

    PCRE2.pcre2_code_free_8(compiled_pattern)
