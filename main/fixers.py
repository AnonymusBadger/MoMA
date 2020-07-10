import re


def set_first_page(url):
    if "page=1&" in url:
        return url
    if "page=" in url:
        url = re.sub(r"page=([\d]*)", "page=1", url)
        return url
    url += "&page=1"
    return url
