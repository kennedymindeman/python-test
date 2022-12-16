import concurrent.futures
import time
import sys


def print_time_taken(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end - start} seconds')

    return wrapper


@print_time_taken
def start_in_order_function_instances(func, num_funcs, *args, **kwargs) -> None:
    for _ in range(num_funcs):
        func(*args, **kwargs)


@print_time_taken
def start_threaded_function_instances(func, thread_count, *args, **kwargs) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as e:
        futures = []
        for _ in range(thread_count):
            futures.append(e.submit(func, *args, **kwargs))

        for future in futures:
            future.result()


@print_time_taken
def start_multiprocess_function_instances(func, thread_count, *args, **kwargs) -> None:
    with concurrent.futures.ProcessPoolExecutor(max_workers=thread_count) as p:
        futures = []
        for _ in range(thread_count):
            futures.append(p.submit(func, *args, **kwargs))

        for future in futures:
            future.result()


if __name__ == '__main__':
    num_threads = int(sys.argv[1])
    start_threaded_function_instances(time.sleep, num_threads, 1)
    start_multiprocess_function_instances(time.sleep, num_threads, 1)
    start_in_order_function_instances(time.sleep, num_threads, 1)