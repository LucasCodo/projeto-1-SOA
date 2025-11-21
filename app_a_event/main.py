from faststream import FastStream
from faststream.rabbit import RabbitBroker
from deck import card_generator
import asyncio
import os

RABBIT_URL = os.getenv("RABBITMQ_URL", "amqp://user:password@localhost:5672/")
queue = os.getenv("RABBITMQ_QUEUE", "queue_a")

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)

get_card = card_generator()

@broker.subscriber(queue)
async def handle_event(_):
    return f"{next(get_card)}"

async def main():
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
