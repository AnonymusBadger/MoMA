from terminal import get_width


def print_centered_text(text):
    if isinstance(text, list):
        for line in text:
            print(line.center(get_width()))
    else:
        print(line.center(get_width()))
