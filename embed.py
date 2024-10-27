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
        "https://unpkg.com/@stoplight/elements/web-components.min.js",
        "https://unpkg.com/@stoplight/elements/styles.min.css",
        "https://docs.stoplight.io/favicons/favicon.ico",
    ]

    responses = await asyncio.gather(*(get_url(url) for url in urls))

    mapping = {
        "src/stopments/embed/web_components.py": encode(responses[0].content),
        "src/stopments/embed/styles.py": encode(responses[1].content),
        "src/stopments/embed/favicon.py": encode(responses[2].content),
    }

    for path, content in mapping.items():
        p = Path(__file__).parent.joinpath(path)
        with p.open("w", encoding="utf-8") as file:
            file.write(f'content = """{content}"""\n')


if __name__ == "__main__":
    asyncio.run(main())
