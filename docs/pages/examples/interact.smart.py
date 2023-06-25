import aiocord
import functools

async def _interact_shop_respond(item, recipient, info: aiocord.widget.Info, core_event: aiocord.events.CreateInteraction):

    response = aiocord.model.protocols.InteractionResponse(
        type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
        data = aiocord.model.protocols.MessageInteractionResponse(
            content = f'{core_event.interaction.member.user.mention()} bought {item} for {recipient}!'
        )
    )

    return response

async def _interact_shop_item_gifting_select(item, info: aiocord.widget.Info, core_event: aiocord.events.CreateInteraction):
    # ignore timeouts
    if core_event is None:
        return
    # compose the recipient
    recipient = ' '.join(aiocord.model.mentions.user(user_id) for user_id in core_event.interaction.data.values)
    # get the response
    response = await _interact_shop_respond(item, recipient, info, core_event)
    # send the response
    return response

async def _interact_shop_item_gifting_accept(item, info: aiocord.widget.Info, core_event: aiocord.events.CreateInteraction):
    # ignore timeouts
    if core_event is None:
        return
    # compose the response
    response = aiocord.model.protocols.InteractionResponse(
        type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
        data = aiocord.model.protocols.MessageInteractionResponse(
            content = 'Who is this a gift for?',
            components = [
                aiocord.model.protocols.MessageActionRowComponent(
                    type = aiocord.model.enums.MessageComponentType.action_row,
                    components = [
                        aiocord.utils.interact(
                            info.client,
                            functools.partial(_interact_shop_item_gifting_select, item, info),
                            aiocord.model.protocols.MessageSelectMenuComponent(
                                type = aiocord.model.enums.MessageComponentType.user_select
                            )
                        )
                    ]
                )
            ],
            flags = aiocord.model.enums.MessageFlags.ephemeral
        )
    )
    # send the response
    return response

async def _interact_shop_item_gifting_reject(item, info: aiocord.widget.Info, core_event: aiocord.events.CreateInteraction):
    # ignore timeouts
    if core_event is None:
        return
    # compose the recipient
    recipient = 'themselves'
    # get the response
    response = await _interact_shop_respond(item, recipient, info, core_event)
    # send the response
    return response

async def _interact_shop_stock_select(stock, info: aiocord.widget.Info, core_event: aiocord.events.CreateInteraction):
    # ignore timeouts
    if core_event is None:
        return
    # get the item name from stock
    item = stock[core_event.interaction.data.values[0]]['name']
    # compose the response
    response = aiocord.model.protocols.InteractionResponse(
        type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
        data = aiocord.model.protocols.MessageInteractionResponse(
            content = 'Is it a gift for someone?',
            components = [
                aiocord.model.protocols.MessageActionRowComponent(
                    type = aiocord.model.enums.MessageComponentType.action_row,
                    components = [
                        aiocord.utils.interact(
                            info.client,
                            functools.partial(_interact_shop_item_gifting_accept, item, info),
                            aiocord.model.protocols.MessageButtonComponent(
                                type = aiocord.model.enums.MessageComponentType.button,
                                label = 'Yes',
                                style = aiocord.model.enums.MessageButtonComponentStyle.primary
                            )
                        ),
                        aiocord.utils.interact(
                            info.client,
                            functools.partial(_interact_shop_item_gifting_reject, item, info),
                            aiocord.model.protocols.MessageButtonComponent(
                                type = aiocord.model.enums.MessageComponentType.button,
                                label = 'No',
                                style = aiocord.model.enums.MessageButtonComponentStyle.secondary
                            )
                        ),
                    ]
                )
            ],
            flags = aiocord.model.enums.MessageFlags.ephemeral
        )
    )
    # send the response
    return response

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
        }, 
    }
    # compose the response
    response = aiocord.model.protocols.InteractionResponse(
        type = aiocord.model.enums.InteractionResponseType.channel_message_with_source,
        data = aiocord.model.protocols.MessageInteractionResponse(
            content = 'What would you like to buy?',
            components = [
                aiocord.model.protocols.MessageActionRowComponent(
                    type = aiocord.model.enums.MessageComponentType.action_row,
                    components = [
                        aiocord.utils.interact(
                            info.client,
                            functools.partial(_interact_shop_stock_select, stock, info),
                            aiocord.model.protocols.MessageSelectMenuComponent(
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
                        )
                    ]
                )
            ],
            flags = aiocord.model.enums.MessageFlags.ephemeral
        )
    )
    # send the response
    return response