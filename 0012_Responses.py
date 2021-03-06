from urllib import response
from starlette.responses import StreamingResponse
import asyncio

import uvicorn

async def slow_numbers(minimum, maximum):
    yield('<html><body><ul>')
    for number in range(minimum, maximum + 1):
        yield f'<li>{number}</li>'
        await asyncio.sleep(0.5)
    yield('</url></body></html>')

async def app(scope, receive, send):
    assert scope['type'] == 'http'
    generator = slow_numbers(1, 10)
    response = StreamingResponse(generator, media_type='text/html')
    await response(scope, receive, send)


uvicorn.run(app)