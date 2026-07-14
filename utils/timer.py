import time
def timed_step(name, func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    print(f"{name:<25} {elapsed:.2f}s")
    return result