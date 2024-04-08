import typing

from . import model as _model
from . import voice     as _voice


__all__ = (
    'Ready', 'UpdateApplicationCommandPermission', 'CreateAutoModerationRule', 
    'UpdateAutoModerationRule', 'DeleteAutoModerationRule', 
    'ExecuteAutoModerationRule', 'CreateChannel', 'UpdateChannel', 
    'DeleteChannel', 'CreateThread', 'UpdateThread', 'DeleteThread', 
    'SyncThreads', 'UpdateThreadMember', 'UpdateThreadMembers', 
    'UpdateChannelPins', 'CreateGuild', 'AvailableGuild', 'DeleteGuild', 
    'UnavailableGuild', 'UpdateGuild', 'CreateGuildAuditLogEntry', 
    'CreateGuildBan', 'DeleteGuildBan', 'UpdateGuildEmojis', 
    'UpdateGuildStickers', 'UpdateGuildIntegrations', 'CreateGuildMember', 
    'DeleteGuildMember', 'UpdateGuildMember', 'ReceiveGuildMembers', 
    'CreateGuildRole', 'UpdateGuildRole', 'DeleteGuildRole', 
    'CreateGuildScheduledEvent', 'UpdateGuildScheduledEvent', 
    'DeleteGuildScheduledEvent', 'CreateGuildScheduledEventUser', 
    'DeleteGuildScheduledEventUser', 'CreateIntegration', 'UpdateIntegration', 
    'DeleteIntegration', 'CreateInvite', 'DeleteInvite', 'CreateMessage', 
    'UpdateMessage', 'DeleteMessage', 'DeleteMessages',
    'CreateMessageReaction', 'DeleteMessageReaction', 
    'DeleteAllMessageReactions', 'DeleteAllMessageEmojiReactions', 
    'UpdatePresence', 'CreateTypingIndicator', 'UpdateSelfUser', 
    'UpdateVoiceState', 'UpdateVoiceServer', 'UpdateWebhooks', 
    'CreateInteraction', 'CreateStageInstance', 'UpdateStageInstance', 
    'DeleteStageInstance', 'EnterVoice', 'LeaveVoice', 'Speak'
)


class Ready(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.ready`.
    """


class UpdateApplicationCommandPermission(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_application_command_permissions`.
    """

    guild                          : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    application_command_permissions: _model.objects.GuildApplicationCommandPermissions
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class CreateAutoModerationRule(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.GatewayEvent.create_auto_moderation_rule`.
    """

    guild               : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    auto_moderation_rule: _model.objects.AutoModerationRule
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """

class UpdateAutoModerationRule(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.GatewayEvent.update_auto_moderation_rule`.
    """

    guild               : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    auto_moderation_rule: _model.objects.AutoModerationRule
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """
  

class DeleteAutoModerationRule(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_auto_moderation_rule`.
    """

    guild               : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    auto_moderation_rule: _model.objects.AutoModerationRule
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """
  

class ExecuteAutoModerationRule(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.GatewayEvent.execute_auto_moderation_action`.
    """

    guild                 : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    auto_moderation_action: _model.objects.AutoModerationAction
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`action`
          - 
    """
    auto_moderation_rule  : _model.objects.AutoModerationRule
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`rule_id`
          - :attr:`~.model.objects.AutoModerationRule.id`
        * - :code:`rule_trigger_type`
          - :attr:`~.model.objects.AutoModerationRule.trigger_type`
    """
    user                  : _model.objects.User
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.User.id`
    """
    channel               : _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    source_message        : _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`message_id`
          - :attr:`~.model.objects.Message.id`
        * - :code:`content`
          - :attr:`~.model.objects.Message.content`
    """
    system_message        : _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`alert_system_message_id`
          - :attr:`~.model.objects.Message.id`
    """
    matched_keyword       : _model.types.String
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`matched_keyword`
          - 
    """
    matched_content       : _model.types.String
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`matched_content`
          - 
    """
  

class CreateChannel(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_channel`.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """


class UpdateChannel(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_channel`.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """


class DeleteChannel(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_channel`.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """


class CreateThread(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_thread`.
    """

    guild : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    thread: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class UpdateThread(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_thread`.
    """

    guild : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    thread: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class DeleteThread(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_thread`.
    """

    guild : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    thread: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class SyncThreads(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.sync_threads`.
    """

    guild : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    threads: _model.types.Collection[_model.objects.Channel]
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`threads`
          -
    """


class UpdateThreadMember(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_thread_member`.
    """

    guild        : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    thread       : _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`id`
          - :attr:`~.model.objects.Channel.id`
    """
    thread_member: _model.objects.ThreadMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class UpdateThreadMembers(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_thread_members`.
    """

    guild                 : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    thread                : _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`id`
          - :attr:`~.model.objects.Channel.id`
    """
    created_thread_members: _model.types.Collection[_model.objects.ThreadMember]
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`added_members`
          - 
    """
    deleted_thread_members: _model.types.Collection[_model.objects.ThreadMember]
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`removed_member_ids`
          - :attr:`~.model.objects.Channel.id`
    """


class UpdateChannelPins(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.GatewayEvent.update_channel_pins`.
    """

    guild    : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel  : _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    timestamp: _model.types.ISO8601Timestamp
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`last_pin_timestamp`
          - 
    """


class CreateGuild(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_guild` when the guild is created.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class AvailableGuild(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_guild` when the guild is available.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class DeleteGuild(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_guild` when the guild is deleted.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class UnavailableGuild(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.` when the guild is unavailable.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class UpdateGuild(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_guild`.

    Copiable with data before updating.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class CreateGuildAuditLogEntry(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_guild_audit_log_entry`.

    Copiable with data before updating.
    """

    guild                : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_audit_log_entry: _model.objects.AuditLogEntry
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class CreateGuildBan(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_guild_ban`.

    Copiable with data before updating.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    user : _model.objects.User
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user`
          -
    """


class DeleteGuildBan(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_guild_ban`.

    Copiable with data before updating.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    user : _model.objects.User
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user`
          -
    """


class UpdateGuildEmojis(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_guild_emojis`.

    Copiable with data before updating.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    emojis: _model.types.Collection[_model.objects.Emoji]
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`emojis`
          - 
    """


class UpdateGuildStickers(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_guild_stickers`.

    Copiable with data before updating.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    emojis: _model.types.Collection[_model.objects.Emoji]
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`stickers`
          - 
    """


class UpdateGuildIntegrations(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_guild_integrations`.

    Copiable with data before updating.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """


class CreateGuildMember(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_guild_member`.

    Copiable with data before updating.
    """

    guild       : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_member: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class DeleteGuildMember(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_guild_member`.

    Copiable with data before updating.
    """

    guild       : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_member: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user`
          -  :attr:`~.model.objects.GuildMember.user`
    """


class UpdateGuildMember(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_guild_member`.

    Copiable with data before updating.
    """

    guild       : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_member: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class ReceiveGuildMembers(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.receive_guild_members`.

    Copiable with data before updating.
    """

    guild          : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_members  : _model.types.Collection[_model.objects.GuildMember]
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`members`
          -
    """
    guild_presences: _model.types.Collection[_model.objects.Presence]
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`members`
          -
    """
    chunk_index    : int
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`chunk_index`
          -
    """
    chunk_indexes  : set[int]
    """
    The remaining indexes (receiving is complete when this is empty).

    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - internal
          -
    """


class CreateGuildRole(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_guild_role`.

    Copiable with data before updating.
    """

    guild     : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_role: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`role`
          -
    """


class UpdateGuildRole(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_guild_role`.

    Copiable with data before updating.
    """

    guild     : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_role: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`role`
          -
    """


class DeleteGuildRole(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_guild_role`.

    Copiable with data before updating.
    """

    guild     : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_role: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`role_id`
          - :attr:`~.model.objects.Role.id`
    """


class CreateGuildScheduledEvent(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_guild_scheduled_event`.

    Copiable with data before updating.
    """

    guild          : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_scheduled_event: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class UpdateGuildScheduledEvent(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_guild_scheduled_event`.

    Copiable with data before updating.
    """

    guild          : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_scheduled_event: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class DeleteGuildScheduledEvent(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_guild_scheduled_event`.

    Copiable with data before updating.
    """

    guild          : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_scheduled_event: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class CreateGuildScheduledEventUser(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_guild_scheduled_event_user`.

    Copiable with data before updating.
    """

    guild          : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_scheduled_event: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_scheduled_event_id`
          - :attr:`~.model.objects.GuildScheduledEvent.id`
    """
    guild_member         : _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.GuildMember.user`\'s :attr:`~.model.objects.User.id`
    """


class DeleteGuildScheduledEventUser(typing.NamedTuple):
  
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_guild_scheduled_event_user`.

    Copiable with data before updating.
    """

    guild          : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_scheduled_event: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_scheduled_event_id`
          - :attr:`~.model.objects.GuildScheduledEvent.id`
    """
    guild_member         : _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.GuildMember.user`\'s :attr:`~.model.objects.User.id`
    """


class CreateIntegration(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_integration`.
    """

    guild      : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    integration: _model.objects.Integration
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """


class UpdateIntegration(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_integration`.
    """

    guild      : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    integration: _model.objects.Integration
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """


class DeleteIntegration(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_integration`.
    """

    guild      : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    integration: _model.objects.Integration
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """


class CreateInvite(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_invite`.
    """

    guild  : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    invite : _model.objects.Invite
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """


class DeleteInvite(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_invite`.
    """

    guild  : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    invite : _model.objects.Invite
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`code`
          - :attr:`~.model.objects.Invite.code`
    """


class CreateMessage(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_message`.
    """

    guild  : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
        * - :code:`last_message_id`
          - :attr:`~.model.objects.Channel.last_message_id`
    """
    message: _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class UpdateMessage(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_message`.
    """

    guild  : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
        * - :code:`last_message_id`
          - :attr:`~.model.objects.Channel.last_message_id`
    """
    message: _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class DeleteMessage(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_message`.
    """

    guild  : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
        * - :code:`last_message_id`
          - :attr:`~.model.objects.Channel.last_message_id`
    """
    message: _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`id`
          - :attr:`~.model.objects.Message.id`
    """


class DeleteMessages(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_messages`.
    """

    guild   : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel : _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
        * - :code:`last_message_id`
          - :attr:`~.model.objects.Channel.last_message_id`
    """
    messages: _model.types.Collection[_model.objects.Message]
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`ids` (each)
          - :attr:`~.model.objects.Message.id`
    """


class CreateMessageReaction(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_message_reaction`.
    """

    guild       : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_member: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`member`
          -
    """
    user        : _model.objects.User
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.User.id`
    """
    channel     : _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    message     : _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`message_id`
          - :attr:`~.model.objects.Message.id`
    """
    emoji       : _model.objects.Emoji
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`emoji`
          -
    """


class DeleteMessageReaction(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_message_reaction`.
    """

    guild       : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_member: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.GuildMember.user`\'s :attr:`~.model.objects.User.id`
    """
    user        : _model.objects.User
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.User.id`
    """
    channel     : _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    message     : _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`message_id`
          - :attr:`~.model.objects.Message.id`
    """
    emoji       : _model.objects.Emoji
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`emoji`
          -
    """


class DeleteAllMessageReactions(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_all_message_reactions`.
    """

    guild  : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    message: _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`message_id`
          - :attr:`~.model.objects.Message.id`
    """


class DeleteAllMessageEmojiReactions(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_all_message_emoji_reactions`.
    """

    guild  : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    message: _model.objects.Message
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`message_id`
          - :attr:`~.model.objects.Message.id`
    """
    emoji  : _model.objects.Emoji
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`emoji`
          -
    """


class UpdatePresence(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_presence`.
    """

    guild   : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    presence: _model.objects.Presence
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class CreateTypingIndicator(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_typing_indicator`.
    """

    guild       : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    guild_member: _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`member`
          - 
    """
    user        : _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.User.id`
    """
    channel     : _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """
    timestamp   : _model.types.Timestamp
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`timestamp`
          - 
    """


class UpdateSelfUser(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_self_user`.
    """

    user: _model.objects.User
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """
    

class UpdateVoiceState(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_voice_state`.
    """

    guild      : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    voice_state: _model.objects.VoiceState
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          - 
    """
    voice      : _voice.client.Client | None
    """
    The self's voice client.
    """


class UpdateVoiceServer(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.GatewayEvent.update_voice_server`.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    token: _model.types.String
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`token`
          -
    """
    uri: _model.types.String
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`uri`
          -
    """


class UpdateWebhooks(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_webhooks`.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`guild_id`
          - :attr:`~.model.objects.Guild.id`
    """
    channel: _model.objects.Channel
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`channel_id`
          - :attr:`~.model.objects.Channel.id`
    """


class CreateInteraction(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_interaction`.
    """

    interaction: _model.objects.Interaction
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class CreateStageInstance(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_stage_instance`.
    """

    stage_instance: _model.objects.StageInstance
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class UpdateStageInstance(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.update_stage_instance`.
    """

    stage_instance: _model.objects.StageInstance
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class DeleteStageInstance(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_stage_instance`.
    """

    stage_instance: _model.objects.StageInstance
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - body
          -
    """


class CreateEntitlement(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.create_entitlement`.
    """

    entitlement: _model.objects.Entitlement
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :attr: body
          -
    """


class UpdateEntitlement(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_entitlement`.
    """

    entitlement: _model.objects.Entitlement
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :attr: body
          -
    """

  
class DeleteEntitlement(typing.NamedTuple):
    
    """
    Dispatched on :attr:`.enums.GatewayEvent.delete_entitlement`.
    """

    entitlement: _model.objects.Entitlement
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :attr: body
          -
    """

  
class EnterVoice(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.VoiceEvent.enter`.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :attr:`~.voice.client.Client.guild_id`
          - :attr:`~.model.objects.User.id`
    """
    user : _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.GuildMember.user`\'s :attr:`~.model.objects.User.id`
    """


class LeaveVoice(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.VoiceEvent.leave`.
    """

    guild: _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :attr:`~.voice.client.Client.guild_id`
          - :attr:`~.model.objects.User.id`
    """
    user : _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.GuildMember.user`\'s :attr:`~.model.objects.User.id`
    """


class Speak(typing.NamedTuple):

    """
    Dispatched on :attr:`.enums.VoiceEvent.speak`.
    """

    guild       : _model.objects.Guild
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :attr:`~.voice.client.Client.guild_id`
          - :attr:`~.model.objects.User.id`
    """
    user : _model.objects.GuildMember
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`user_id`
          - :attr:`~.model.objects.GuildMember.user`\'s :attr:`~.model.objects.User.id`
    """
    flags: _model.enums.SpeechFlags
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`speaking`
          -
    """
    ssrc : _model.types.Integer
    """
    .. list-table::
        :width: 450px
        :widths: 50 50
        :header-rows: 1

        * - Source
          - Target
        * - :code:`ssrc`
          -
    """
