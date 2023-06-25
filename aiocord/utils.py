import typing
import base64
import secrets
import asyncio

from . import model  as _model
from . import enums  as _enums
from . import events as _events
from . import client as _client


__all__ = ('get_image_data_uri', 'get_eventful_intents', 'interact')


def _get_image_data_uri(mime, data):

    data = base64.b64encode(data)

    return f'data:{mime};base64:{data}'


def get_image_date_uri(data: bytes, 
                       mime: str = 'image/png'):

    """
    Get an :ddoc:`image date uri </reference#image-data>`.

    :param data:
        The data to encode within the uri.
    :param mime:
        The data mimetype to attach. 
    """

    return _get_image_data_uri(mime, data)


_eventful_intents = {
    _events.CreateAutoModerationRule          : _enums.Intents.guild_moderation,
    _events.UpdateAutoModerationRule          : _enums.Intents.auto_moderation_configuration,
    _events.DeleteAutoModerationRule          : _enums.Intents.auto_moderation_configuration,
    _events.ExecuteAutoModerationRule         : _enums.Intents.auto_moderation_action_execution,
    _events.CreateChannel                     : _enums.Intents.guilds,
    _events.UpdateChannel                     : _enums.Intents.guilds,
    _events.DeleteChannel                     : _enums.Intents.guilds,
    _events.CreateThread                      : _enums.Intents.guilds,
    _events.UpdateThread                      : _enums.Intents.guilds,
    _events.DeleteThread                      : _enums.Intents.guilds,
    _events.SyncThreads                       : _enums.Intents.guilds,
    _events.UpdateThreadMember                : _enums.Intents.guilds,
    _events.UpdateThreadMembers               : _enums.Intents.guilds,
    _events.UpdateChannelPins                 : _enums.Intents.guilds | _enums.Intents.direct_messages,
    _events.AvailableGuild                    : _enums.Intents.guilds,
    _events.UpdateChannel                     : _enums.Intents.guilds,
    _events.CreateGuild                       : _enums.Intents.guilds,
    _events.DeleteGuild                       : _enums.Intents.guilds,
    _events.UnavailableGuild                  : _enums.Intents.guilds,
    _events.UpdateGuild                       : _enums.Intents.guilds,
    _events.CreateGuildAuditLogEntry          : _enums.Intents.guild_moderation,
    _events.CreateGuildBan                    : _enums.Intents.guild_moderation,
    _events.DeleteGuildBan                    : _enums.Intents.guild_moderation,
    _events.UpdateGuildEmojis                 : _enums.Intents.guild_emojis_and_stickers,
    _events.UpdateGuildStickers               : _enums.Intents.guild_emojis_and_stickers,
    _events.UpdateGuildIntegrations           : _enums.Intents.guild_integrations,
    _events.CreateGuildMember                 : _enums.Intents.guild_members,
    _events.DeleteGuildMember                 : _enums.Intents.guild_members,
    _events.UpdateGuildMember                 : _enums.Intents.guild_members,
    _events.CreateGuildRole                   : _enums.Intents.guilds,
    _events.UpdateGuildRole                   : _enums.Intents.guilds,
    _events.DeleteGuildRole                   : _enums.Intents.guilds,
    _events.CreateGuildScheduledEvent         : _enums.Intents.guild_scheduled_events,
    _events.UpdateGuildScheduledEvent         : _enums.Intents.guild_scheduled_events,
    _events.DeleteGuildScheduledEvent         : _enums.Intents.guild_scheduled_events,
    _events.CreateGuildScheduledEventUser     : _enums.Intents.guild_scheduled_events,
    _events.DeleteGuildScheduledEventUser     : _enums.Intents.guild_scheduled_events,
    _events.CreateIntegration                 : _enums.Intents.guild_integrations,
    _events.UpdateIntegration                 : _enums.Intents.guild_integrations,
    _events.DeleteIntegration                 : _enums.Intents.guild_integrations,
    _events.CreateInvite                      : _enums.Intents.guild_invites,
    _events.DeleteInvite                      : _enums.Intents.guild_invites,
    _events.CreateMessage                     : _enums.Intents.guild_messages | _enums.Intents.direct_messages | _enums.Intents.message_content,
    _events.UpdateMessage                     : _enums.Intents.guild_messages | _enums.Intents.direct_messages | _enums.Intents.message_content,
    _events.DeleteMessage                     : _enums.Intents.guild_messages | _enums.Intents.direct_messages,
    _events.DeleteMessages                    : _enums.Intents.guild_messages,
    _events.CreateMessageReaction             : _enums.Intents.guild_message_reactions | _enums.Intents.direct_message_reactions,
    _events.DeleteMessageReaction             : _enums.Intents.guild_message_reactions | _enums.Intents.direct_message_reactions,
    _events.DeleteAllMessageReactions         : _enums.Intents.guild_message_reactions | _enums.Intents.direct_message_reactions,
    _events.DeleteAllMessageEmojiReactions    : _enums.Intents.guild_message_reactions | _enums.Intents.direct_message_reactions,
    _events.UpdatePresence                    : _enums.Intents.guild_presences,
    _events.CreateTypingIndicator             : _enums.Intents.guild_message_typing,
    _events.UpdateVoiceState                  : _enums.Intents.guild_voice_states, # shall always be included
    _events.UpdateWebhooks                    : _enums.Intents.guild_webhooks,
    _events.CreateStageInstance               : _enums.Intents.guilds,
    _events.UpdateStageInstance               : _enums.Intents.guilds,
    _events.DeleteStageInstance               : _enums.Intents.guilds,
}


def _get_eventful_intents(Events: list[typing.Any]):

    intents = _enums.Intents(0)

    for Event in Events:
        try:
            subinents = _eventful_intents[Event]
        except KeyError:
            continue
        intents |= subinents

    return intents


def get_eventful_intents(Events):

    """
    Get the intents required to receive the specified events.
    """

    return _get_eventful_intents(Events)


_interact_types = {
    _model.enums.InteractionType.message_component, 
    _model.enums.InteractionResponseType.modal
}


def _interact(client, callback, component, / , **kwargs):

    custom_id = secrets.token_hex(32)

    component['custom_id'] = custom_id

    async def check(core_event):
        return core_event.interaction.type in _interact_types and core_event.interaction.data.custom_id == custom_id
    
    sentinel = client.wait(_events.CreateInteraction, check, **kwargs)

    async def sub_callback(core_event):
        response = await callback(core_event)
        if not response is None:
            await client.create_interaction_response(core_event.interaction.id, core_event.interaction.token, **response)

    def done_callback(task):
        try:
            core_event = task.result()
        except TimeoutError:
            core_event = None
        asyncio.create_task(sub_callback(core_event))

    sentinel.add_done_callback(done_callback)

    return component


def interact(client   : _client.Client, 
             callback : typing.Callable[[typing.Union[typing.Any, None]], typing.Awaitable[_model.protocols.InteractionResponse | None]], 
             component: _model.protocols.MessageButtonComponent | _model.protocols.MessageSelectMenuComponent | _model.protocols.MessageTextInputComponent,
             /,
             timeout  : float = 3):
    
    """
    Invoke a callback when the component has been interacted with.

    If a :code:`.model.protocols.InteractionResponse` is returned, it is used to respond via :meth:`.client.create_interaction_response`.

    :param client:
        The client to attach the callback to.
    :param callback:
        Used with ``(event)`` if successful or ``(None)`` if timed-out.
    :param component:
        A :code:`'custom_id'` will be set for identifying interactions to it.
    :param timeout:
        Same as :paramref:`.client.wait.timeout`.
    """

    return _interact(client, callback, component, timeout = timeout)