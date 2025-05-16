import asyncio
import base64
import zlib
from pathlib import Path

import httpx

mapping = {
    "https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js": "web-components.min.js",
    "https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css": "styles.min.css",
    "https://cdn.jsdelivr.net/npm/@scalar/api-reference": "scalar-api-reference.js",
}


def encode(content: bytes) -> str:
    z = zlib.compress(content, level=9)
    return base64.b85encode(z).decode("utf-8")


async def download(url: str, root: Path, filename: str) -> None:
    async with httpx.AsyncClient(
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    ) as client:
        resp = await client.get(url, follow_redirects=True)
    resp.raise_for_status()
    file = root.joinpath(filename)
    await asyncio.to_thread(file.write_bytes, resp.content)


async def main():
    static = Path(__file__).parent.joinpath("src/stopments/static")
    async with asyncio.TaskGroup() as tg:
        for url, filename in mapping.items():
            task = download(url, static, filename)
            tg.create_task(task)

    print("Downloaded all files.")  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
