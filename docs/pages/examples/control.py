import asyncio
import aiocord

async def start(client):
    await client.start()
    await client.ready()
    await aiocord.widget.load(client, 'blep', './modules')

async def stop(client):
    await aiocord.widget.drop(client, 'blep')
    await client.stop()

loop = asyncio.get_event_loop()

client = aiocord.client.Client(token = ...)

loop.run_until_complete(start(client))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(stop(client))