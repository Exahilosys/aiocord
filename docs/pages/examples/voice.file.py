import asyncio
import aiocord

async def start(client):
    await client.start()
    await client.ready()

async def main(client):
    voice = await client.start_voice('506536485156739358', '543273600667152384')
    audio = aiocord.voice.audio.Audio(source = './song.mp3')
    await voice.player.start(audio)

async def stop(client):
    await client.stop()

loop = asyncio.get_event_loop()

client = aiocord.client.Client(token = ...)

loop.run_until_complete(start(client))

try:
    loop.run_until_complete(main(client))
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(stop(client))