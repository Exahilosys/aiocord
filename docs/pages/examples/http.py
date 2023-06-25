import asyncio
import aiocord

async def main(client):
    message = await client.create_message('864902189816273146', content = 'hello!')
    await client.create_reaction(message.channel_id, message.id, '🤠')

loop = asyncio.get_event_loop()

client = aiocord.client.Client(token = ...)

loop.run_until_complete(main(client))