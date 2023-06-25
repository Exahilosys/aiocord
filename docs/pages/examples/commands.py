import aiocord

commands = [
    aiocord.model.protocols.ApplicationCommand(
        name = 'blep',
        type = aiocord.model.enums.ApplicationCommandType.chat_input,
        description = 'blep someone',
        options = [
            aiocord.model.protocols.ApplicationCommandOption(
                name = 'user',
                description = 'the user to blep',
                type = aiocord.model.enums.ApplicationCommandOptionType.user
            )
        ]
    )
]