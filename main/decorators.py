from terminal import get_width as width


def spacer() -> str:
    return "".join(["=" for _ in range(width())])


def head(func):
    def wrapper(*args, **kwargs):
        print(f"{spacer()}\n")
        func(*args, **kwargs)
        print(f"\n{spacer()}")

    return wrapper


def body(func):
    def wrapper(*args, **kwargs):
        print()
        func(*args, **kwargs)
        print(f"\n{spacer()}")

    return wrapper


def footer(func):
    def wrapper(*args, **kwargs):
        print()
        func(*args, **kwargs)

    return wrapper


def center_text(func):
    def wrapper(text):
        if isinstance(text, list):
            text = "\n".join([line.center(width()) for line in text])
            return func(text)

        else:
            pass

    return wrapper
