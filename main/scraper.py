import asyncio
import logging
import os
import random
from asyncio import sleep as sleep

import aiofiles
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(message)s", datefmt="%H:%M:%S",
)


async def request(url, session):
    async with session.get(url) as resp:
        logging.debug(f"Got response [{resp.status}] for URL: {url}")
        html = await resp.read()
        return BeautifulSoup(html, "html.parser")


async def get_next_page(url, session):
    logging.debug("Loading page")
    page = await request(url, session)
    if page.find("span", "next"):
        logging.debug("Next page found")
        next_url = "https://www.moma.org" + page.find("span", "next").find("a").get(
            "href"
        )
        return page, next_url
    else:
        return page, None
        logging.debug("Last page reached")


async def crawler(url, session):
    page, next_url = await get_next_page(url, session)
    while True:
        yield page
        if next_url is not None:
            page, next_url = await get_next_page(next_url, session)
        else:
            break


def get_links(page):
    return (
        f"https://www.moma.org{link.get('href')}"
        for link in page.find_all("a", class_="grid-item__link")
    )


async def get_data(url, session, **kwargs):
    logging.debug(f"Parsing Data for {url}")

    def get_info(page):
        basic_info = dict(
            zip(
                ["Author", "Title", "Date"],
                (
                    item.text.strip()
                    for item in page.find_all(
                        "span",
                        (
                            [
                                "work__short-caption__text--primary",
                                "work__short-caption__text",
                            ],
                        ),
                    )
                ),
            )
        )
        details = dict(
            zip(
                (
                    item.text.strip()
                    for item in page.find_all("dt", "work__caption__term")
                ),
                (
                    item.text.strip()
                    for item in page.find_all("dd", "work__caption__description")
                ),
            )
        )
        try:
            img = "https://www.moma.org" + page.find(
                "img", class_="link/enable link/focus picture/image"
            ).get("src")
        except AttributeError:
            img = "Unavailable"
            logging.warning(f"Image not avelable for: {url}")
        complete_info = {
            **basic_info,
            **details,
            "Artwork URL": url,
            "Img URL": img,
        }
        return complete_info

    page = await request(url, session)
    logging.debug("Parsing data")
    data = get_info(page)
    img = tuple([data["Object number"], data["Img URL"]])
    await downloader(img, session, **kwargs)
    return data


async def downloader(img, session, path):
    logging.debug("Downloading Image")
    title, url = img
    if url == "Unavailable":
        return
    file = path + f"/{title}.jpg"
    async with session.get(url) as resp:
        with open(file, "wb") as fd:
            while True:
                chunk = await resp.content.read(10)
                if not chunk:
                    logging.debug(f"Finished Downloading")
                    break
                fd.write(chunk)


async def get_pages(url, session):
    pages = crawler(url, session)
    async for page in pages:
        logging.info("Getting artworks list")
        links = get_links(page)
        logging.info("Downloading Images")
        yield links


async def chain(url, **kwargs):
    async with ClientSession() as session:
        links = get_pages(url, session)
        async for link in links:
            tasks = []
            for url in link:
                tasks.append(get_data(url, session, **kwargs))
            yield await asyncio.gather(*tasks)


async def agregator(url, **kwargs):
    result = chain(url, **kwargs)
    data = []
    async for lst in result:
        logging.info("Aggregating new artworks")
        for item in lst:
            data.append(item)
    return data


def main(url, path):
    save_path = f"{path}/Images"
    os.mkdir(save_path)
    logging.info("Starting scraping")
    data = asyncio.run(agregator(url, path=save_path))
    logging.info("Done!")
    return data
