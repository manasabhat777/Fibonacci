"""
    Module which generates Fibonacci numbers between given index range
"""
fib_cache = {}
def fibonacci_cache(n):
    global fib_cache
    if n in fib_cache:
        return fib_cache[n]

    if n == 1:
        fib_cache[n] = 1
        return 1
    elif n == 2:
        fib_cache[n] = 2
        return 2

    elif n > 2:
        value = fibonacci_cache(n-1) + fibonacci_cache(n-2)
        fib_cache[n] = value
        return value

def fibonacci(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    elif n > 2:
        return fibonacci(n-1) + fibonacci(n-2)

def gen_fib_index_range_cache(mn, mx):
    response_dict = {}
    fib_list = []
    for n in range(mn, mx):
        fib_list.append(fibonacci_cache(n))
    response_dict['fibonacci_numbers'] = fib_list
    return response_dict 
