import aiocord

async def __load__(info):
    print('loaded', __name__)

async def __drop__(info):
    print('dropped', __name__)

@aiocord.widget.callback(aiocord.events.CreateMessage)
async def _callback_create_message(info, core_event):
    print('message created!', core_event.message.content)

@aiocord.widget.interact('blep')
async def _interact_blep(info, core_event):
    users = core_event.interaction.data.resolved.users
    blepping = ' '.join(user.mention() for user in users)
    return aiocord.model.protocols.InteractionResponse(
        type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
        data = aiocord.model.protocols.MessageInteractionResponse(
            content = f'blep {blepping}'
        )
    )