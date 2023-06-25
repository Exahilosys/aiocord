import aiocord
import secrets

@aiocord.widget.interact('shop')
async def _interact_shop(info: aiocord.widget.Info, core_event: aiocord.events.CreateInteraction):
    # define the stock
    stock = {
        'ice-cream': {
            'name': 'Ice Cream',
            'emoji': '🍦'
        },
        'cake': {
            'name': 'Cake',
            'emoji': '🍰'
        }, 
        'waffle': {
            'name': 'Waffle',
            'emoji': '🧇'
        }
    }
    # unique identifier
    select_custom_id = secrets.token_hex(16)
    # compose the response
    response = aiocord.model.protocols.InteractionResponse(
        type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
        data = aiocord.model.protocols.MessageInteractionResponse(
            content = 'What would you like to buy?',
            components = [
                aiocord.model.protocols.MessageActionRowComponent(
                    type = aiocord.model.enums.MessageComponentType.action_row,
                    components = [
                        aiocord.model.protocols.MessageSelectMenuComponent(
                            custom_id = select_custom_id,
                            type = aiocord.model.enums.MessageComponentType.string_select,
                            options = [
                                aiocord.model.protocols.MessageSelectMenuComponentOption(
                                    value = key,
                                    label = item['name'],
                                    description = 'Sweet, fluffy, chunky and super tasty.',
                                    emoji = aiocord.model.protocols.Emoji(
                                        name = item['emoji']
                                    )
                                )
                                for key, item in stock.items()
                            ]
                        )
                    ]
                )
            ],
            # ensure only the invoker can see this
            flags = aiocord.model.enums.MessageFlags.ephemeral
        )
    )
    # condition for the expected interaction
    async def check(core_event: aiocord.events.CreateInteraction):
        # only accept an interaction to the identifer
        return core_event.interaction.type == aiocord.model.enums.InteractionType.message_component and core_event.interaction.data.custom_id == select_custom_id
    # make the waiter
    sentinel = info.client.wait(aiocord.events.CreateInteraction, check)
    # send the response
    await info.client.create_interaction_response(core_event.interaction.id, core_event.interaction.token, **response)
    # wait the interaction
    core_event = await sentinel
    # resolve the picked item
    item = stock[core_event.interaction.data.values[0]]['name']
    # unique identifiers
    negative_button_custom_id = secrets.token_hex(16)
    positive_button_custom_id = secrets.token_hex(16)
    # compose the response
    response = aiocord.model.protocols.InteractionResponse(
        type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
        data = aiocord.model.protocols.MessageInteractionResponse(
            content = 'Is it a gift for someone?',
            components = [
                aiocord.model.protocols.MessageActionRowComponent(
                    type = aiocord.model.enums.MessageComponentType.action_row,
                    components = [
                        aiocord.model.protocols.MessageButtonComponent(
                            custom_id = positive_button_custom_id,
                            type = aiocord.model.enums.MessageComponentType.button,
                            label = 'Yes',
                            style = aiocord.model.enums.MessageButtonComponentStyle.primary
                        ),
                        aiocord.model.protocols.MessageButtonComponent(
                            custom_id = negative_button_custom_id,
                            type = aiocord.model.enums.MessageComponentType.button,
                            label = 'No',
                            style = aiocord.model.enums.MessageButtonComponentStyle.secondary
                        )
                    ]
                )
            ],
            # ensure only the invoker can see this
            flags = aiocord.model.enums.MessageFlags.ephemeral
        )
    )
    # unique identifier group
    custom_id_button_group = [negative_button_custom_id, positive_button_custom_id]
    # condition for the expected interaction
    async def check(core_event: aiocord.events.CreateInteraction):
        # only accept an interaction to the identifers
        return core_event.interaction.type == aiocord.model.enums.InteractionType.message_component and core_event.interaction.data.custom_id in custom_id_button_group
    # make the waiter
    sentinel = info.client.wait(aiocord.events.CreateInteraction, check)
    # send the response
    await info.client.create_interaction_response(core_event.interaction.id, core_event.interaction.token, **response)
    # wait the interaction
    core_event = await sentinel
    # resolve whether positive
    is_gift = custom_id_button_group.index(core_event.interaction.data.custom_id)
    # ...is it?
    if is_gift:
        # unique identifier
        select_custom_id = secrets.token_hex(16)
        # compose the response
        response = aiocord.model.protocols.InteractionResponse(
            type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
            data = aiocord.model.protocols.MessageInteractionResponse(
                content = 'Who is this a gift for?',
                components = [
                    aiocord.model.protocols.MessageActionRowComponent(
                        type = aiocord.model.enums.MessageComponentType.action_row,
                        components = [
                            aiocord.model.protocols.MessageSelectMenuComponent(
                                custom_id = select_custom_id,
                                type = aiocord.model.enums.MessageComponentType.user_select
                            )
                        ]
                    )
                ],
                flags = aiocord.model.enums.MessageFlags.ephemeral
            )
        )
        # condition for the expected interaction
        async def check(core_event: aiocord.events.CreateInteraction):
            return core_event.interaction.type == aiocord.model.enums.InteractionType.message_component and core_event.interaction.data.custom_id == select_custom_id
        # make the waiter
        sentinel = info.client.wait(aiocord.events.CreateInteraction, check)
        # send the response
        await info.client.create_interaction_response(core_event.interaction.id, core_event.interaction.token, **response)
        # wait the interaction
        core_event = await sentinel
        # resolve the recipients
        recipient = ' '.join(aiocord.model.mentions.user(user_id) for user_id in core_event.interaction.data.values)
    else:
        recipient = 'themselves'
    # compose the response
    response = aiocord.model.protocols.InteractionResponse(
        type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
        data = aiocord.model.protocols.MessageInteractionResponse(
            # anyone can see this
            content = f'{info.client.cache.user.mention()} bought {item} for {recipient}!'
        )
    )
    # send the response
    await info.client.create_interaction_response(core_event.interaction.id, core_event.interaction.token, **response)