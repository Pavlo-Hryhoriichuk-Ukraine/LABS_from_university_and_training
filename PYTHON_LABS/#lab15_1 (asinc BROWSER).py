#lab15_1 (asinc BROWSER)

import asyncio
import httpx
import sys

# Налаштування для Windows, щоб коректно читати кирилицю в консолі

if sys.platform == 'win32':
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

async def get_links_from_url(article_title:str):
    url = "https://uk.wikipedia.org/w/api.php" #API для читання сторінок

    headers = {
        "User-Agent": "StudentProjectBot/1.0 (myemail@example.com)" 
    }

    params = {
        "action": "query",
        "format": "json",
        "titles": article_title,
        "prop": "links",
        "pllimit": "max",     # Беремо максимум посилань
        "plnamespace": 0      # Тільки основний простір (статті)
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url,params=params,headers=headers)
        data = response.json()

        pages = data.get("query",{}).get("pages",{})

        links_lst = []
        for page_id in pages:
            page = pages[page_id]
            if "links" in page:
                for link in page["links"]:
                    links_lst.append(link["title"])

        return links_lst

async def main():

    async with asyncio.TaskGroup() as tg:
        first_title = await asyncio.to_thread(input, "Input first title: ")
        task1 = asyncio.create_task(get_links_from_url(first_title.strip()))
        second_title = await asyncio.to_thread(input, "Input second title: ")
        task2 = asyncio.create_task(get_links_from_url(second_title.strip()))

    first_links = await task1
    second_links = await task2

    try:
        N12 = len(set(first_links).intersection(set(second_links)))
        k = 2*N12/(len(first_links) + len(second_links))
    except ZeroDivisionError:
        print("Lenght of first links list and second = 0")
    except Exception as e:
        print(f"Error, type: {e}")
    else:
        print(f"Degree of closeness of our 2 articles is: {k:.4f}")

if __name__ == "__main__":
    asyncio.run(main())