import asyncio
import json

import aio_pika

from core.avatar_creator import create_avatar, get_image_as_bytes
from core.settings import RabbitMQSettings
from s3.s3_handler import upload_file_to_s3


class RabbitMQClient:
    def __init__(self):
        self.amqp_url = RabbitMQSettings.AMQP_URL
        self.queue_name = "avatars_queue"
        self.connection = None

    async def connect(self):
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.amqp_url)

    async def on_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            decoded_message = message.body.decode()
            body = json.loads(decoded_message)
            model = body.get("ai_model", None)
            prompt = body.get("prompt", None)

            avatar_url = await create_avatar(model=model, prompt=prompt)

            avatar_bytes = await get_image_as_bytes(img_url=avatar_url)

            await upload_file_to_s3(file_uuid=body["uuid"], img_bytes=avatar_bytes)

    async def consume(self):
        await self.connect()
        channel = await self.connection.channel()
        queue = await channel.declare_queue(self.queue_name, durable=True)
        await queue.consume(self.on_message)

    async def start_consuming(self):
        await asyncio.create_task(self.consume())

    async def close(self):
        if self.connection:
            self.connection.close()
