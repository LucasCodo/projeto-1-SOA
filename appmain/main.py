import asyncio
from uuid import uuid4

from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter, Context
from nicegui import ui
from starlette.responses import RedirectResponse
from settings import ENV
import httpx

async def get_stickers_rest():
    async with httpx.AsyncClient() as client:
        response = await client.get(ENV.API_REST_URL)
        return response.json().get('cards', []) if response.status_code == 200 else []

router = RabbitRouter(ENV.RABBITMQ_URL)

@router.subscriber("response")
async def consume_responses(msg: str, cor_id: str = Context("message.correlation_id")):
    #print(f"[RESPONSE-{cor_id}] ->{msg}")
    if queue :=pending_responses.get(cor_id):
        await queue.put(msg)

async def broadcast_event(queues: list[str], correlation_id: str, reply_to: str = 'response'):
    #print(f"[EMITTER] Enviando para as filas {queues} - {correlation_id}")
    for q in queues:
        await router.broker.publish(queue=q, reply_to=reply_to, correlation_id=correlation_id, priority=1)

pending_responses: dict[str, asyncio.Queue[str]] = {}

async def get_stickers_rabbitmq(queues: list[str]):
    correlation_id = str(uuid4())
    response_queue: asyncio.Queue[str] = asyncio.Queue()
    pending_responses[correlation_id] = response_queue
    try:
        await broadcast_event(queues, correlation_id)
        cards: list[str | None] = []
        try:
            for _ in queues:
                msg = await asyncio.wait_for(response_queue.get(), timeout=5.0)
                cards.append(msg)
        except asyncio.TimeoutError:
            cards.append(None)
        return cards if any(cards) else []
    finally:
        pending_responses.pop(correlation_id, None)

@router.get("/stickers")
async def stickers_endpoint():
    cards = await get_stickers_rabbitmq(ENV.QUEUES)
    return {
        "cards": cards,
    }

fastapi_app = FastAPI()
fastapi_app.include_router(router)

@fastapi_app.get('/')
def get_root():
    return RedirectResponse('/gui')

@ui.page('/')
async def show():
    with ui.header().classes('items-center justify-between'):
        ui.label('Álbum de Figurinhas').classes('text-2xl font-bold')

    album: dict[str, int] = {}

    # container onde o álbum será renderizado
    album_container = ui.row().classes(
        'mt-6 flex flex-wrap gap-4'
    )

    def render_album() -> None:
        album_container.clear()
        with album_container:
            if not album:
                ui.label('Nenhuma figurinha no álbum ainda.').classes(
                    'text-gray-500 italic'
                )
                return

            for card_code, qty in sorted(album.items()):
                with ui.card().classes(
                        'relative p-2 flex flex-col items-center w-32 shadow-md rounded-xl'
                ):

                    # imagem da carta
                    ui.image(
                        f'https://www.deckofcardsapi.com/static/img/{card_code}.png'
                    ).classes('w-18 object-contain')

                    # badge com quantidade (posicionado no canto superior direito)
                    ui.badge(
                        f'x{qty}',
                        color='red',
                        text_color='white'
                    ).props(
                        'floating'
                    )

    async def get_stickers():
        ui.notify('Pedindo figurinha...', type='ongoing', timeout=2000)

        cards_rest = await get_stickers_rest()
        cards_rabbit = await get_stickers_rabbitmq(ENV.QUEUES)
        cards = cards_rest + cards_rabbit

        if not cards:
            ui.notify('Nenhuma figurinha recebida.', type='negative')
            return

        ui.notify(f'Recebidas {len(cards)} figurinha(s)', type='positive')

        for card in cards:
            album[card] = album.get(card, 0) + 1

        render_album()

    ui.button('Pedir figurinha', on_click=get_stickers).classes('mt-4')

    render_album()



ui.run_with(
    fastapi_app,
    mount_path='/gui',
    storage_secret='pick your private secret here',
)