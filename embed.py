import asyncio
import base64
import zlib
from pathlib import Path

import httpx


def encode(content: bytes) -> str:
    z = zlib.compress(content, level=9)
    return base64.b85encode(z).decode("utf-8")


async def get_url(url: str) -> httpx.Response:
    async with httpx.AsyncClient(
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    ) as client:
        resp = await client.get(url, follow_redirects=True)
    resp.raise_for_status()
    return resp


async def main():
    urls = [
        "https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js",
        "https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css",
    ]

    responses = await asyncio.gather(*(get_url(url) for url in urls))

    static = Path(__file__).parent.joinpath("src/stopments/static")

    async with asyncio.TaskGroup() as tg:
        for url, resp in zip(urls, responses, strict=True):
            filename = url.split("/")[-1]
            file = static.joinpath(filename)
            task = asyncio.to_thread(file.write_bytes, resp.content)
            tg.create_task(task)


if __name__ == "__main__":
    asyncio.run(main())
