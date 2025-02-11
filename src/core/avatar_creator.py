import aiohttp
from runware import IImageInference, Runware

from core.settings import RunwareSettings

MODELS = {
    "anime": "civitai:30240@125771",
    "cartoon": "civitai:30240@125771",
    "lego": "civitai:306814@344398",
}


async def create_avatar(model: str, prompt: str) -> str:
    runware = Runware(api_key=RunwareSettings.RUNWARE_API_KEY)
    await runware.connect()

    request_image = IImageInference(
        positivePrompt=prompt,
        model=MODELS[model],
        numberResults=1,
        height=512,
        width=512,
    )
    image_data = await runware.imageInference(requestImage=request_image)

    for data in image_data:
        return data.imageURL


async def get_image_as_bytes(img_url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as response:
            result = await response.read()
            return result
