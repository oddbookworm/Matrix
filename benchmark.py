from time import perf_counter

iterations = 1_000_000


def timer(func):
    def wrapper():
        start = perf_counter()
        func()
        end = perf_counter()
        print(f"Time = {end - start} seconds")

    return wrapper


size = 4


@timer
def loop():
    for _ in range(iterations):
        for i in range(size):
            i


@timer
def hardcode():
    for _ in range(iterations):
        1
        2
        3
        4


loop()
hardcode()
