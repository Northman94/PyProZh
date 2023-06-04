def base_decorator(original_func):
    def wrap_func(n2):
        print(f"Some code, before original_func.")

        if callable(original_func):
            if isinstance(n2, int) or isinstance(n2, float):
                return original_func(n2)

            else:
                print("Invalid argument. Pls provide int or float.")
        else:
            print(f"Not Callable Obj is used")

        print(f"Some code, after original func.")

    return wrap_func


@base_decorator
def func_tobe_decorated(n):
    print(f"I want to be decorated.")
    return n**3


print(func_tobe_decorated(5.5))