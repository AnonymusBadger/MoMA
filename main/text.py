from terminal import get_width


def center_text(text):
    if isinstance(text, list):
        return "\n".join([line.center(get_width()) for line in text])
