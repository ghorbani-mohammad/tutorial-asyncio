import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def get_page(session, url):
    async with session.get(url) as r:
        return await r.text()

async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data

# Notice because parsing is not I/O bound and it is CPU bound
# We didn't async here.
def parse(results):
    for html in results:
        soup = BeautifulSoup(html, 'html')
        print(soup.find('form', {'class': 'form-horizontal'}).text().strip())

if __name__ == "__main__":
    urls = [
        "http://books.toscrape.com/catalogue/page-1.html",
        "http://books.toscrape.com/catalogue/page-2.html",
        "http://books.toscrape.com/catalogue/page-3.html",
    ]
    results = asyncio.run(main(urls))
    parse(results)