import aiohttp
import asyncio
from io import BytesIO

async def photo_link(photo_bytes):
    form = aiohttp.FormData()
    form.add_field(
        name='file',
        value=photo_bytes,
    )
    async with aiohttp.ClientSession() as session:
        async with session.post('https://telegra.ph/upload', data=form) as response:
            img_src = await response.json()
            link = 'http://telegra.ph/' + img_src[0]["src"]
            return link

async def main():
    with open('src/Sertifikat.png', 'rb') as photo_file:  # Bunda tirnoqlarni olib tashlang
        photo_bytes = BytesIO(photo_file.read())
        link = await photo_link(photo_bytes)
        print(f"Rasm linki: {link}")

if __name__ == "__main__":
    asyncio.run(main())