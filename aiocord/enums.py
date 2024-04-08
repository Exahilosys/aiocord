import enum


__all__ = ('Intents', 'GatewayEvent', 'VoiceEvent')


class Intents(enum.IntFlag):

    """
    Available :ddoc:`Gateway Intents </topics/gateway#gateway-intents>`.
    """
  
    guilds                           = 1 << 0
    guild_members                    = 1 << 1
    guild_moderation                 = 1 << 2
    guild_emojis_and_stickers        = 1 << 3
    guild_integrations               = 1 << 4
    guild_webhooks                   = 1 << 5
    guild_invites                    = 1 << 6
    guild_voice_states               = 1 << 7
    guild_presences                  = 1 << 8
    guild_messages                   = 1 << 9
    guild_message_reactions          = 1 << 10
    guild_message_typing             = 1 << 11
    direct_messages                  = 1 << 12
    direct_message_reactions         = 1 << 13
    direct_message_typing            = 1 << 14
    message_content                  = 1 << 15
    guild_scheduled_events           = 1 << 16
    auto_moderation_configuration    = 1 << 20
    auto_moderation_action_execution = 1 << 21

    @classmethod
    def default(cls):

        """
        Get all the non-privilaged intents.
        """

        return (
              cls.guilds
            | cls.guild_moderation
            | cls.guild_emojis_and_stickers
            | cls.guild_integrations
            | cls.guild_webhooks
            | cls.guild_invites
            | cls.guild_voice_states
            | cls.guild_messages
            | cls.guild_message_reactions
            | cls.guild_message_typing
            | cls.direct_messages
            | cls.direct_message_reactions
            | cls.direct_message_typing
            | cls.guild_scheduled_events
            | cls.auto_moderation_configuration
            | cls.auto_moderation_action_execution
        )


class GatewayEvent(enum.StrEnum):

    """
    Available `Events </topics/gateway-events#receive-events>` received through :attr:`.gateway.enums.OpCode.dispatch`.
    """

    ready                                  = 'READY'
    """
    |dsrc| 
    :ddoc:`Ready </topics/gateway-events#ready>`
    """
    update_application_command_permissions = 'APPLICATION_COMMAND_PERMISSIONS_UPDATE'
    """
    |dsrc| 
    :ddoc:`Application Command Permissions Update <topics/gateway-events#application-command-permissions-update>`
    """
    create_auto_moderation_rule            = 'AUTO_MODERATION_RULE_CREATE'
    """
    |dsrc| 
    :ddoc:`Auto Moderation Rule Create </topics/gateway-events#auto-moderation-rule-create>`
    """
    update_auto_moderation_rule            = 'AUTO_MODERATION_RULE_UPDATE'
    """
    |dsrc| 
    :ddoc:`Auto Moderation Rule Update </topics/gateway-events#auto-moderation-rule-update>`
    """
    delete_auto_moderation_rule            = 'AUTO_MODERATION_RULE_DELETE'
    """
    |dsrc| 
    :ddoc:`Auto Moderation Rule Delete </topics/gateway-events#auto-moderation-rule-delete>` 
    """
    execute_auto_moderation_action         = 'AUTO_MODERATION_ACTION_EXECUTION'
    """
    |dsrc| 
    :ddoc:`Auto Moderation Action Execution </topics/gateway-events#auto-moderation-action-execution>` 
    """
    create_channel                         = 'CHANNEL_CREATE'
    """
    |dsrc| 
    :ddoc:`Channel Create </topics/gateway-events#channel-create>` 
    """
    update_channel                         = 'CHANNEL_UPDATE'
    """
    |dsrc| 
    :ddoc:`Channel Update </topics/gateway-events#channel-update>` 
    """
    delete_channel                         = 'CHANNEL_DELETE'
    """
    |dsrc| 
    :ddoc:`Channel Delete </topics/gateway-events#channel-delete>` 
    """
    update_channel_pins                    = 'CHANNEL_PINS_UPDATE'
    """
    |dsrc| 
    :ddoc:`Channel Pins Update </topics/gateway-events#channel-pins-update>` 
    """
    create_thread                          = 'THREAD_CREATE'
    """
    |dsrc| 
    :ddoc:`Thread Create </topics/gateway-events#thread-create>` 
    """
    update_thread                          = 'THREAD_UPDATE'
    """
    |dsrc| 
    :ddoc:`Thread Update </topics/gateway-events#thread-update>` 
    """
    delete_thread                          = 'THREAD_DELETE'
    """
    |dsrc| 
    :ddoc:`Thread Delete </topics/gateway-events#thread-delete>` 
    """
    sync_threads                           = 'THREAD_LIST_SYNC'
    """
    |dsrc| 
    :ddoc:`Thread List Sync </topics/gateway-events#thread-list-sync>` 
    """
    update_thread_member                   = 'THREAD_MEMBER_UPDATE'
    """
    |dsrc| 
    :ddoc:`Thread Member Update </topics/gateway-events#thread-member-update>` 
    """
    update_thread_members                  = 'THREAD_MEMBERS_UPDATE'
    """
    |dsrc| 
    :ddoc:`Thread Members Update </topics/gateway-events#thread-members-update>` 
    """
    create_guild                           = 'GUILD_CREATE'
    """
    |dsrc| 
    :ddoc:`Guild Create </topics/gateway-events#guild-create>` 
    """
    update_guild                           = 'GUILD_UPDATE'
    """
    |dsrc| 
    :ddoc:`Guild Update </topics/gateway-events#guild-update>` 
    """
    delete_guild                           = 'GUILD_DELETE'
    """
    |dsrc| 
    :ddoc:`Guild Delete </topics/gateway-events#guild-delete>` 
    """
    create_guild_audit_log_entry           = 'GUILD_AUDIT_LOG_ENTRY_CREATE'
    """
    |dsrc| 
    :ddoc:`Guild Audit Log Entry Create </topics/gateway-events#guild-audit-log-entry-create>` 
    """
    create_guild_ban                       = 'GUILD_BAN_ADD'
    """
    |dsrc| 
    :ddoc:`Guild Ban Add </topics/gateway-events#guild-ban-add>` 
    """
    delete_guild_ban                       = 'GUILD_BAN_REMOVE'
    """
    |dsrc| 
    :ddoc:`Guild Ban Remove </topics/gateway-events#guild-ban-remove>` 
    """
    update_guild_emojis                    = 'GUILD_EMOJIS_UPDATE'
    """
    |dsrc| 
    :ddoc:`Guild Emojis Update </topics/gateway-events#guild-emojis-update>` 
    """
    update_guild_stickers                  = 'GUILD_STICKERS_UPDATE'
    """
    |dsrc| 
    :ddoc:`Guild Stickers Update </topics/gateway-events#guild-stickers-update>` 
    """
    update_guild_integrations              = 'GUILD_INTEGRATIONS_UPDATE'
    """
    |dsrc| 
    :ddoc:`Guild Integrations Update </topics/gateway-events#guild-integrations-update>` 
    """
    create_guild_member                    = 'GUILD_MEMBER_ADD'
    """
    |dsrc| 
    :ddoc:`Guild Member Add </topics/gateway-events#guild-member-add>` 
    """
    delete_guild_member                    = 'GUILD_MEMBER_REMOVE'
    """
    |dsrc| 
    :ddoc:`Guild Member Remove </topics/gateway-events#guild-member-remove>` 
    """
    update_guild_member                    = 'GUILD_MEMBER_UPDATE'
    """
    |dsrc| 
    :ddoc:`Guild Member Update </topics/gateway-events#guild-member-update>` 
    """
    receive_guild_members                  = 'GUILD_MEMBERS_CHUNK'
    """
    |dsrc| 
    :ddoc:`Guild Members Chunk </topics/gateway-events#guild-members-chunk>` 
    """
    create_guild_role                      = 'GUILD_ROLE_CREATE'
    """
    |dsrc| 
    :ddoc:`Guild Role Create </topics/gateway-events#guild-role-create>` 
    """
    update_guild_role                      = 'GUILD_ROLE_UPDATE'
    """
    |dsrc| 
    :ddoc:`Guild Role Update </topics/gateway-events#guild-role-update>` 
    """
    delete_guild_role                      = 'GUILD_ROLE_DELETE'
    """
    |dsrc| 
    :ddoc:`Guild Role Delete </topics/gateway-events#guild-role-delete>` 
    """
    create_guild_scheduled_event           = 'GUILD_SCHEDULED_EVENT_CREATE'
    """
    |dsrc| 
    :ddoc:`Guild Scheduled Event Create </topics/gateway-events#guild-scheduled-event-create>` 
    """
    update_guild_scheduled_event           = 'GUILD_SCHEDULED_EVENT_UPDATE'
    """
    |dsrc| 
    :ddoc:`Guild Scheduled Event Update </topics/gateway-events#guild-scheduled-event-update>` 
    """
    delete_guild_scheduled_event           = 'GUILD_SCHEDULED_EVENT_DELETE'
    """
    |dsrc| 
    :ddoc:`Guild Scheduled Event Delete </topics/gateway-events#guild-scheduled-event-delete>` 
    """
    create_guild_scheduled_event_user      = 'GUILD_SCHEDULED_EVENT_USER_ADD'
    """
    |dsrc| 
    :ddoc:`Guild Scheduled Event User Add </topics/gateway-events#guild-scheduled-event-user-add>` 
    """
    delete_guild_scheduled_event_user      = 'GUILD_SCHEDULED_EVENT_USER_REMOVE'
    """
    |dsrc| 
    :ddoc:`Guild Scheduled Event User Remove </topics/gateway-events#guild-scheduled-event-user-remove>` 
    """
    create_integration                     = 'INTEGRATION_CREATE'
    """
    |dsrc| 
    :ddoc:`Integration Create </topics/gateway-events#integration-create>` 
    """
    update_integration                     = 'INTEGRATION_UPDATE'
    """
    |dsrc| 
    :ddoc:`Integration Update </topics/gateway-events#integration-update>` 
    """
    delete_integration                     = 'INTEGRATION_DELETE'
    """
    |dsrc| 
    :ddoc:`Integration Delete </topics/gateway-events#integration-delete>` 
    """
    create_interaction                     = 'INTERACTION_CREATE'
    """
    |dsrc| 
    :ddoc:`Interaction Create </topics/gateway-events#interaction-create>` 
    """
    create_invite                          = 'INVITE_CREATE'
    """
    |dsrc| 
    :ddoc:`Invite Create </topics/gateway-events#invite-create>` 
    """
    delete_invite                          = 'INVITE_DELETE'
    """
    |dsrc| 
    :ddoc:`Invite Delete </topics/gateway-events#invite-delete>` 
    """
    create_message                         = 'MESSAGE_CREATE'
    """
    |dsrc| 
    :ddoc:`Message Create </topics/gateway-events#message-create>` 
    """
    update_message                         = 'MESSAGE_UPDATE'
    """
    |dsrc| 
    :ddoc:`Message Update </topics/gateway-events#message-update>` 
    """
    delete_message                         = 'MESSAGE_DELETE'
    """
    |dsrc| 
    :ddoc:`Message Delete </topics/gateway-events#message-delete>` 
    """
    delete_messages                        = 'MESSAGE_DELETE_BULK'
    """
    |dsrc| 
    :ddoc:`Message Delete Bulk </topics/gateway-events#message-delete-bulk>` 
    """
    create_message_reaction                = 'MESSAGE_REACTION_ADD'
    """
    |dsrc| 
    :ddoc:`Message Reaction Add </topics/gateway-events#message-reaction-add>` 
    """
    delete_message_reaction                = 'MESSAGE_REACTION_REMOVE'
    """
    |dsrc| 
    :ddoc:`Message Reaction Remove </topics/gateway-events#message-reaction-remove>` 
    """
    delete_all_message_reactions           = 'MESSAGE_REACTION_REMOVE_ALL'
    """
    |dsrc| 
    :ddoc:`Message Reaction Remove All </topics/gateway-events#message-reaction-remove-all>` 
    """
    delete_all_message_emoji_reactions     = 'MESSAGE_REACTION_REMOVE_EMOJI'
    """
    |dsrc| 
    :ddoc:`Message Reaction Remove Emoji </topics/gateway-events#message-reaction-remove-emoji>` 
    """
    update_presence                        = 'PRESENCE_UPDATE'
    """
    |dsrc| 
    :ddoc:`Presence Update </topics/gateway-events#presence-update>` 
    """
    create_stage_instance                  = 'STAGE_INSTANCE_CREATE'
    """
    |dsrc| 
    :ddoc:`Stage Instance Create </topics/gateway-events#stage-instance-create>` 
    """
    update_stage_instance                  = 'STAGE_INSTANCE_UPDATE'
    """
    |dsrc| 
    :ddoc:`Stage Instance Update </topics/gateway-events#stage-instance-update>` 
    """
    delete_stage_instance                  = 'STAGE_INSTANCE_DELETE'
    """
    |dsrc| 
    :ddoc:`Stage Instance Delete </topics/gateway-events#stage-instance-delete>` 
    """
    create_typing_indicator                = 'TYPING_START'
    """
    |dsrc| 
    :ddoc:`Typing Start </topics/gateway-events#typing-start>` 
    """
    update_self_user                       = 'USER_UPDATE'
    """
    |dsrc| 
    :ddoc:`User Update </topics/gateway-events#user-update>` 
    """
    update_voice_state                     = 'VOICE_STATE_UPDATE'
    """
    |dsrc| 
    :ddoc:`Voice State Update </topics/gateway-events#voice-state-update>` 
    """
    update_voice_server                    = 'VOICE_SERVER_UPDATE'
    """
    |dsrc| 
    :ddoc:`Voice Server Update </topics/gateway-events#voice-server-update>` 
    """
    update_webhooks                        = 'WEBHOOKS_UPDATE'
    """
    |dsrc| 
    :ddoc:`Webhooks Update </topics/gateway-events#webhooks-update>` 
    """
    create_entitlement                     = 'ENTITLEMENT_CREATE'
    """
    |dsrc|
    :ddoc:`Entitlement Create` </monetization/entitlements#new-entitlement>
    """
    update_entitlement                     = 'ENTITLEMENT_UPDATE'
    """
    |dsrc|
    :ddoc:`Entitlement Update` </monetization/entitlements#updated-entitlement>
    """
    delete_entitlement                     = 'ENTITLEMENT_DELETE'
    """
    |dsrc|
    :ddoc:`Entitlement Delete` </monetization/entitlements#deleted-entitlement>
    """


class VoiceEvent(enum.StrEnum):

    speak = 'SPEAK'
    """
    A user has spoken.
    """
    enter = 'ENTER'
    """
    A user has joined the channel.
    """
    leave = 'LEAVE'
    """
    A user has left the channel.
    """