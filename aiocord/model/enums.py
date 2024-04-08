import enum


__all__ = (
    'ApplicationCommandType', 'StatusType', 'Locale',
    'Permissions', 'ApplicationCommandOptionType', 'ChannelType', 
    'MessageComponentType', 'MessageButtonComponentStyle', 
    'MessageTextInputComponentStyle', 'InteractionType', 
    'InteractionContextType', 'InteractionResponseType', 
    'ApplicationIntegrationType', 'ApplicationFlags', 
    'ApplicationRoleConnectionMetadataType', 'AuditLogEvent', 
    'OptionalAuditLogEntryInfoOverwrittenEntityType', 
    'AutoModerationTriggerType', 'AutoModerationRuleKeywordPresetType', 
    'AutoModerationRuleEventType', 'AutoModerationActionType', 
    'ChannelVideoQualityMode', 'ChannelFlags', 'ChannelSortOrderType', 
    'ForumLayoutType', 'MessageType', 'MessageActivityType', 'MessageFlags', 
    'OverwriteType', 'EmbedType', 'AllowedMentionsType', 
    'GuildVerificationLevel', 'GuildDefaultMessageNotificationLevel', 
    'GuildExplicitContentFilterLevel', 'GuildFeature', 'GuildMFALevel', 
    'GuildNSFWLevel', 'GuildSystemChannelFlags', 'GuildPremiumTier', 
    'GuildMemberFlags', 'IntegrationExpireBehaviorType', 
    'GuildOnboardingPromptType', 'GuildScheduledEventPrivacyLevel', 
    'GuildScheduledEventEntityType', 'GuildScheduledEventStatus', 
    'InviteTargetType', 'StageInstancePrivacyLevel', 'StickerType', 
    'StickerFormatType', 'UserFlags', 'UserPremiumType', 
    'ConnectionVisibilityType', 'WebhookType', 'ActivityType', 
    'ActivityFlags', 'TeamMemberMembershipState', 'WidgetStyleOption',
    'SpeechFlags', 'TimestampStyle', 'SKUType', 'SKUFlags', 'EntitlementType',
    'EntitlementOwnerType'
)


class EnumMeta(enum.EnumType):

    def __call__(self, data, *args, **kwargs):
        try:
            value = super().__call__(data, *args, **kwargs)
        except ValueError:
            value = data
        return value
    

class ApplicationCommandType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Application Command Option Types </interactions/application-commands#application-command-object-application-command-option-type>`
    """

    chat_input = 1
    user       = 2
    message    = 3


class StatusType(enum.StrEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Update Presence Status Types </topics/gateway-events#update-presence-status-types>`
    """

    online    = 'online'
    dnd       = 'dnd'
    idle      = 'idle'
    invisible = 'invisible'
    offline   = 'offline'


class Locale(enum.StrEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Locales </reference#locales>`
    """

    indonesian    = 'id'
    danish        = 'da'
    german        = 'de'
    english_uk    = 'en-GB'
    english_us    = 'en-US'
    spanish_es    = 'es-ES'
    french        = 'fr'
    croatian      = 'hr'
    italian       = 'it'
    lithuanian    = 'lt'
    hungarian     = 'hu'
    dutch         = 'nl'
    norwegian     = 'no'
    polish        = 'pl'
    portuguese_br = 'pt-BR'
    romanian      = 'ro'
    finnish       = 'fi'
    swedish_se    = 'sv-SE'
    vietnamese    = 'vi'
    turkish       = 'tr'
    czech         = 'cs'
    greek         = 'el'
    bulgarian     = 'bg'
    russian       = 'ru'
    ukrainian     = 'uk'
    hindi         = 'hi'
    thai          = 'th'
    chinese_cn    = 'zh-CN'
    japanese      = 'ja'
    chinese_tw    = 'zh-TW'
    korean        = 'ko'


class PermissionsMeta(enum.IntFlag, metaclass = EnumMeta.__class__):

    def __call__(self, data, *args, **kwargs):
        data = int(data)
        return super().__call__(data, *args, **kwargs)


class Permissions(enum.IntFlag, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Permission Flags </topics/permissions#permissions-bitwise-permission-flags>`
    """
    
    create_instant_invite               = 1 << 0
    kick_members                        = 1 << 1
    ban_members                         = 1 << 2
    administrator                       = 1 << 3
    manage_channels                     = 1 << 4
    manage_guild                        = 1 << 5
    add_reactions                       = 1 << 6
    view_audit_log                      = 1 << 7
    priority_speaker                    = 1 << 8
    stream                              = 1 << 9
    view_channel                        = 1 << 10
    send_messages                       = 1 << 11
    send_tts_messages                   = 1 << 12
    manage_messages                     = 1 << 13
    embed_links                         = 1 << 14
    attach_files                        = 1 << 15
    read_message_history                = 1 << 16
    mention_everyone                    = 1 << 17
    use_external_emojis                 = 1 << 18
    view_guild_insights                 = 1 << 19
    connect                             = 1 << 20
    speak                               = 1 << 21
    mute_members                        = 1 << 22
    deafen_members                      = 1 << 23
    move_members                        = 1 << 24
    use_vad                             = 1 << 25
    change_nickname                     = 1 << 26
    manage_nicknames                    = 1 << 27
    manage_roles                        = 1 << 28
    manage_webhooks                     = 1 << 29
    manage_guild_expressions            = 1 << 30
    use_application_commands            = 1 << 31
    request_to_speak                    = 1 << 32
    manage_events                       = 1 << 33
    manage_threads                      = 1 << 34
    create_public_threads               = 1 << 35
    create_private_threads              = 1 << 36
    use_external_stickers               = 1 << 37
    send_messages_in_threads            = 1 << 38
    use_embedded_activities             = 1 << 39
    moderate_members                    = 1 << 40
    view_creator_monetization_analytics = 1 << 41
    use_soundboard                      = 1 << 42
    create_guild_expressions            = 1 << 43
    create_events                       = 1 << 44
    send_voice_messages                 = 1 << 46


class ApplicationCommandOptionType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Application Command Option Types </interactions/application-commands#application-command-object-application-command-option-type>`
    """

    sub_command       = 1
    sub_command_group = 2
    string            = 3
    integer           = 4
    boolean           = 5
    user              = 6
    channel           = 7
    role              = 8
    mentionable       = 9
    number            = 10
    attachment        = 11


class ChannelType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Channel Types </resources/channel#channel-object-channel-types>`
    """

    guild_text          = 0
    dm                  = 1
    guild_voice         = 2
    group_dm            = 3
    guild_category      = 4
    guild_announcement  = 5
    announcement_thread = 10
    public_thread       = 11
    private_thread      = 12
    guild_stage_voice   = 13
    guild_directory     = 14
    guild_forum         = 15
    guild_media         = 16



class ApplicationCommandPermissionType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Application Command Permission Types </interactions/application-commands#application-command-permissions-object-application-command-permission-type>`
    """

    role    = 1
    user    = 2
    channel = 3


class MessageComponentType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Component Types </interactions/message-components#component-object-component-types>`
    """

    action_row         = 1
    button             = 2
    string_select      = 3
    text_input         = 4
    user_select        = 5
    role_select        = 6
    mentionable_select = 7
    channel_select     = 8


class MessageButtonComponentStyle(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Button Styles </interactions/message-components#button-object-button-styles>`
    """

    primary   = 1
    secondary = 2
    success   = 3
    danger    = 4
    link      = 5

class MessageSelectMenuComponentDefaultValueType(enum.StrEnum, metaclass = EnumMeta):


    """
    |dsrc| 
    :ddoc:`Select Meny Default Value Types </interactions/message-components#select-menu-object-select-default-value-structure>`
    """

    user = 'user'
    role = 'role'
    channel = 'channel'

class MessageTextInputComponentStyle(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Text Input Styles </interactions/message-components#text-inputs-text-input-styles>`
    """

    short = 1
    paragraph = 2


class InteractionType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Interaction Types </interactions/receiving-and-responding#interaction-object-interaction-type>`
    """

    ping                             = 1
    application_command              = 2
    message_component                = 3
    application_command_autocomplete = 4
    modal_submit                     = 5


class InteractionContextType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Interaction Context Types </interactions/receiving-and-responding#interaction-object-interaction-context-types>`
    """

    guild           = 0
    bot_dm          = 1
    private_channel = 2
    

class InteractionResponseType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Interaction Callback Types </interactions/receiving-and-responding#interaction-response-object-interaction-callback-type>`
    """

    pong                                    = 1
    channel_message_with_source             = 4
    deferred_channel_message_with_source    = 5
    deferred_update_message                 = 6
    update_message                          = 7
    application_command_autocomplete_result = 8
    modal                                   = 9
    premium_required                        = 10


class ApplicationIntegrationType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Application Integration Types </resources/application#application-object-application-integration-types>`
    """

    guild_install = 0
    user_install  = 1


class ApplicationFlags(enum.IntFlag, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Application Flags </resources/application#application-object-application-flags>`
    """

    application_auto_moderation_rule_create_badge = 1 << 6
    gateway_presence                              = 1 << 12
    gateway_presence_limited                      = 1 << 13
    gateway_guild_members                         = 1 << 14
    gateway_guild_members_limited                 = 1 << 15
    verification_pending_guild_limit              = 1 << 16
    embedded                                      = 1 << 17
    gateway_message_content                       = 1 << 18
    gateway_message_content_limited               = 1 << 19
    application_command_badge                     = 1 << 23


class ApplicationRoleConnectionMetadataType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Application Role Connection Metadata Types </resources/application-role-connection-metadata#application-role-connection-metadata-object-application-role-connection-metadata-type>`
    """

    integer_less_than_or_equal     = 1
    integer_greater_than_or_equal  = 2
    integer_equal                  = 3
    integer_not_equal              = 4
    datetime_less_than_or_equal    = 5
    datetime_greater_than_or_equal = 6
    boolean_equal                  = 7
    boolean_not_equal              = 8


class AuditLogEvent(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Audit Log Events </resources/audit-log#audit-log-entry-object-audit-log-events>`
    """

    guild_update                                = 1
    channel_create                              = 10
    channel_update                              = 11
    channel_delete                              = 12
    channel_overwrite_create                    = 13
    channel_overwrite_update                    = 14
    channel_overwrite_delete                    = 15
    member_kick                                 = 20
    member_prune                                = 21
    member_ban_add                              = 22
    member_ban_remove                           = 23
    member_update                               = 24
    member_role_update                          = 25
    member_move                                 = 26
    member_disconnect                           = 27
    bot_add                                     = 28
    role_create                                 = 30
    role_update                                 = 31
    role_delete                                 = 32
    invite_create                               = 40
    invite_update                               = 41
    invite_delete                               = 42
    webhook_create                              = 50
    webhook_update                              = 51
    webhook_delete                              = 52
    emoji_create                                = 60
    emoji_update                                = 61
    emoji_delete                                = 62
    message_delete                              = 72
    message_bulk_delete                         = 73
    message_pin                                 = 74
    message_unpin                               = 75
    integration_create                          = 80
    integration_update                          = 81
    integration_delete                          = 82
    stage_instance_create                       = 83
    stage_instance_update                       = 84
    stage_instance_delete                       = 85
    sticker_create                              = 90
    sticker_update                              = 91
    sticker_delete                              = 92
    guild_scheduled_event_create                = 100
    guild_scheduled_event_update                = 101
    guild_scheduled_event_delete                = 102
    thread_create                               = 110
    thread_update                               = 111
    thread_delete                               = 112
    application_command_permission_update       = 121
    auto_moderation_rule_create                 = 140
    auto_moderation_rule_update                 = 141
    auto_moderation_rule_delete                 = 142
    auto_moderation_block_message               = 143
    auto_moderation_flag_to_channel             = 144
    auto_moderation_user_communication_disabled = 145


class OptionalAuditLogEntryInfoOverwrittenEntityType(enum.StrEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Optional Audit Entry Info </resources/audit-log#audit-log-entry-object-optional-audit-entry-info>`
    """

    role   = '0'
    member = '1'


class AutoModerationTriggerType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Trigger Types </resources/auto-moderation#auto-moderation-rule-object-trigger-types>`
    """

    keyword        = 1
    spam           = 3
    keyword_preset = 4
    mention_spam   = 5


class AutoModerationRuleKeywordPresetType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Keyword Preset Types </resources/auto-moderation#auto-moderation-rule-object-keyword-preset-types>`
    """

    profanity      = 1
    sexual_content = 2
    slurs          = 3


class AutoModerationRuleEventType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Event Types </auto-moderation#auto-moderation-rule-object-event-types>`
    """

    message_send = 1


class AutoModerationActionType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Action Types </resources/auto-moderation#auto-moderation-action-object-action-types>`
    """

    block_message      = 1
    send_alert_message = 2
    timeout            = 3


class ChannelVideoQualityMode(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Video Quality Modes </resources/channel#channel-object-video-quality-modes>`
    """

    auto = 1
    full = 2


class ChannelFlags(enum.IntFlag, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Channel Flags </resources/channel#channel-object-channel-flags>`
    """

    pinned      = 1 << 1
    require_tag = 1 << 4


class ChannelSortOrderType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Sort Order Types </channel#channel-object-sort-order-types>`
    """

    latest_activity = 0
    creation_date   = 1


class ForumLayoutType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Forum Layout Types </resources/channel#channel-object-forum-layout-types>`
    """

    not_set      = 0
    list_view    = 1
    gallery_view = 2


class MessageType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Message Types </resources/channel#message-object-message-types>`
    """

    default                                      = 0
    recipient_add                                = 1
    recipient_remove                             = 2
    call                                         = 3
    channel_name_change                          = 4
    channel_icon_change                          = 5
    channel_pinned_message                       = 6
    user_join                                    = 7
    guild_boost                                  = 8
    guild_boost_tier_1                           = 9
    guild_boost_tier_2                           = 10
    guild_boost_tier_3                           = 11
    channel_follow_add                           = 12
    guild_discovery_disqualified                 = 14
    guild_discovery_requalified                  = 15
    guild_discovery_grace_period_initial_warning = 16
    guild_discovery_grace_period_final_warning   = 17
    thread_created                               = 18
    reply                                        = 19
    chat_input_command                           = 20
    thread_starter_message                       = 21
    guild_invite_reminder                        = 22
    context_menu_command                         = 23
    auto_moderation_action                       = 24
    role_subscription_purchase                   = 25
    interaction_premium_upsell                   = 26
    stage_start                                  = 27
    stage_end                                    = 28
    stage_speaker                                = 29
    stage_topic                                  = 31
    guild_application_premium_subscription       = 32


class MessageActivityType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Message Activity Types </resources/channel#message-object-message-activity-types>`
    """

    join         = 1
    spectate     = 2
    listen       = 3
    join_request = 5


class MessageFlags(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Message Flags </resources/channel#message-object-message-flags>`
    """

    crossposted                            = 1 << 0
    is_crosspost                           = 1 << 1
    suppress_embeds                        = 1 << 2
    source_message_deleted                 = 1 << 3
    urgent                                 = 1 << 4
    has_thread                             = 1 << 5
    ephemeral                              = 1 << 6
    loading                                = 1 << 7
    failed_to_mention_some_roles_in_thread = 1 << 8
    suppress_notifications                 = 1 << 12
    is_voice_message                       = 1 << 13



class OverwriteType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Overwrite Structure </resources/channel#overwrite-object-overwrite-structure>`
    """

    role   = 0
    member = 1


class EmbedType(enum.StrEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Embed Types </resources/channel#embed-object-embed-types>`
    """

    rich    = 'rich'
    image   = 'image'
    video   = 'video'
    gifv    = 'gifv'
    article = 'article'
    link    = 'link'


class AllowedMentionsType(enum.StrEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Allowed Mention Types </resources/channel#allowed-mentions-object-allowed-mention-types>`
    """

    roles    = 'roles'
    users    = 'users'
    everyone = 'everyone'


class GuildVerificationLevel(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Verification Level </resources/guild#guild-object-verification-level>`
    """

    none      = 0
    low       = 1
    medium    = 2
    high      = 3
    very_high = 4


class GuildDefaultMessageNotificationLevel(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Default Message Notification Level </resources/guild#guild-object-default-message-notification-level>`
    """

    all_messages  = 0
    only_mentions = 1
    

class GuildExplicitContentFilterLevel(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Explicit Content Filter Level </resources/guild#guild-object-explicit-content-filter-level>`
    """

    disabled              = 0
    members_without_roles = 1
    all_members           = 2


class GuildFeature(enum.StrEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Guild Features </resources/guild#guild-object-guild-features>`
    """

    animated_banner                           = 'ANIMATED_BANNER'
    animated_icon                             = 'ANIMATED_ICON'
    application_command_permissions_v2        = 'APPLICATION_COMMAND_PERMISSIONS_V2'
    auto_moderation                           = 'AUTO_MODERATION'
    banner                                    = 'BANNER'
    community                                 = 'COMMUNITY'
    creator_monetizable_provisional           = 'CREATOR_MONETIZABLE_PROVISIONAL'
    creator_store_page                        = 'CREATOR_STORE_PAGE'
    developer_support_server                  = 'DEVELOPER_SUPPORT_SERVER'
    discoverable                              = 'DISCOVERABLE'
    featurable                                = 'FEATURABLE'
    invites_disabled                          = 'INVITES_DISABLED'
    invite_splash                             = 'INVITE_SPLASH'
    member_verification_gate_enabled          = 'MEMBER_VERIFICATION_GATE_ENABLED'
    more_stickers                             = 'MORE_STICKERS'
    news                                      = 'NEWS'
    partnered                                 = 'PARTNERED'
    preview_enabled                           = 'PREVIEW_ENABLED'
    role_icons                                = 'ROLE_ICONS'
    role_subscriptions_available_for_purchase = 'ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE'
    role_subscriptions_enabled                = 'ROLE_SUBSCRIPTIONS_ENABLED'
    ticketed_events_enabled                   = 'TICKETED_EVENTS_ENABLED'
    vanity_url                                = 'VANITY_URL'
    verified                                  = 'VERIFIED'
    vip_regions                               = 'VIP_REGIONS'
    welcome_screen_enabled                    = 'WELCOME_SCREEN_ENABLED'
    raid_alerts_disabled                      = 'RAID_ALERTS_DISABLED'
    # undocumented
    text_in_voice_enabled                     = 'TEXT_IN_VOICE_ENABLED'


class GuildMFALevel(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Mfa Level </resources/guild#guild-object-mfa-level>`
    """

    none     = 0
    elevated = 1


class GuildNSFWLevel(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Guild Nsfw Level </resources/guild#guild-object-guild-nsfw-level>`
    """

    default        = 0
    explicit       = 1
    safe           = 2
    age_restricted = 3


class GuildSystemChannelFlags(enum.IntFlag, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`System Channel Flags </resources/guild#guild-object-system-channel-flags>`
    """

    suppress_join_notifications                              = 1 << 0
    suppress_premium_subscriptions                           = 1 << 1
    suppress_guild_reminder_notifications                    = 1 << 2
    suppress_join_notification_replies                       = 1 << 3
    suppress_role_subscription_purchase_notifications        = 1 << 4
    suppress_role_subscription_purchase_notification_replies = 1 << 5


class GuildPremiumTier(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Premium Tier </resources/guild#guild-object-premium-tier>`
    """

    none   = 0
    tier_1 = 1
    tier_2 = 2
    tier_3 = 3


class GuildMemberFlags(enum.IntFlag, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Guild Member Flags </resources/guild#guild-member-object-guild-member-flags>`
    """

    did_rejoin            = 1 << 0
    completed_onboarding  = 1 << 1
    bypasses_verification = 1 << 2
    started_onboarding    = 1 << 3


class IntegrationExpireBehaviorType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Integration Expire Behaviors </resources/guild#integration-object-integration-expire-behaviors>`
    """

    remove_role = 0
    kick        = 1


class GuildOnboardingPromptType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Prompt Types </resources/guild#guild-onboarding-object-prompt-types>`
    """

    multiple_choice = 0
    dropdown        = 1


class GuildScheduledEventPrivacyLevel(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Guild Scheduled Event Privacy Level </resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-privacy-level>`
    """

    guild_only = 2


class GuildScheduledEventEntityType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Guild Scheduled Event Entity Types </resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-types>`
    """

    stage_instance = 1
    voice          = 2
    external       = 3


class GuildScheduledEventStatus(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Guild Scheduled Event Status </resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-status>`
    """

    scheduled = 1
    active    = 2
    completed = 3
    canceled  = 4


class InviteTargetType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Invite Target Types </resources/invite#invite-object-invite-target-types>`
    """

    stream               = 1
    embedded_application = 2


class StageInstancePrivacyLevel(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Privacy Level </resources/stage-instance#stage-instance-object-privacy-level>`
    """

    public     = 1
    guild_only = 2


class StickerType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Sticker Types </resources/sticker#sticker-object-sticker-types>`
    """

    standard = 1
    guild    = 2


class StickerFormatType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Sticker Format Types </resources/sticker#sticker-object-sticker-format-types>`
    """

    png    = 1
    apng   = 2
    lottie = 3
    gif    = 4


class UserFlags(enum.IntFlag, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`User Flags </resources/user#user-object-user-flags>`
    """

    staff                    = 1 << 0
    partner                  = 1 << 1
    hypesquad                = 1 << 2
    bug_hunter_level_1       = 1 << 3
    hypesquad_online_house_1 = 1 << 6
    hypesquad_online_house_2 = 1 << 7
    hypesquad_online_house_3 = 1 << 8
    premium_early_supporter  = 1 << 9
    team_pseudo_user         = 1 << 10
    bug_hunter_level_2       = 1 << 14
    verified_bot             = 1 << 16
    verified_developer       = 1 << 17
    certified_moderator      = 1 << 18
    bot_http_interactions    = 1 << 19
    active_developer         = 1 << 22


class UserPremiumType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Premium Types </resources/user#user-object-premium-types>`
    """

    none          = 0
    nitro_classic = 1
    nitro         = 2
    nitro_basic   = 3


class ConnectionVisibilityType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Visibility Types </resources/user#connection-object-visibility-types>`
    """

    none     = 0
    everyone = 1


class WebhookType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Webhook Types </resources/webhook#webhook-object-webhook-types>`
    """

    incoming         = 1
    channel_follower = 2
    application      = 3


class ActivityType(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Activity Types </topics/gateway-events#activity-object-activity-types>`
    """

    game      = 0
    streaming = 1
    listening = 2
    watching  = 3
    custom    = 4
    competing = 5


class ActivityFlags(enum.IntFlag, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Activity Types </topics/gateway-events#activity-object-activity-types>`
    """

    instance                    = 1 << 0
    join                        = 1 << 1
    spectate                    = 1 << 2
    join_request                = 1 << 3
    sync                        = 1 << 4
    play                        = 1 << 5
    party_privacy_friends       = 1 << 6
    party_privacy_voice_channel = 1 << 7
    embedded                    = 1 << 8


class TeamMemberMembershipState(enum.IntEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Data Models Membership State Enum </topics/teams#data-models-membership-state-enum>`
    """

    invited  = 1
    accepted = 2


class WidgetStyleOption(enum.StrEnum, metaclass = EnumMeta):

    """
    |dsrc| 
    :ddoc:`Widget Style Options </resources/guild#get-guild-widget-image-widget-style-options>`
    """

    shield	= 'shield' 
    banner1	= 'banner1' 
    banner2	= 'banner2' 
    banner3	= 'banner3' 
    banner4	= 'banner4' 


class SpeechFlags(enum.IntFlag):

    """
    |dsrc|
    :ddoc:`Speaking Flags </topics/voice-connections#speaking>`
    """

    microphone = 1
    soundshare = 2
    priority   = 4


class TimestampStyle(enum.StrEnum):

    """
    |dsrc|
    :ddoc:`Message Formatting Timestamp Styles </reference#message-formatting-timestamp-styles>`
    """

    short_time      = 't'
    long_time       = 'T'
    short_date      = 'd'
    long_date       = 'D'
    short_date_time = 'f'
    long_date_time  = 'F'
    relative_time   = 'R'


class SKUType(enum.IntEnum):

    """
    |dsrc|
    :ddoc:`SKU Types </monetization/skus#sku-object-sku-types>`
    """

    subscription       = 5
    subscription_group = 6


class SKUFlags(enum.IntFlag):

    """
    |dsrc|
    :ddoc:`SKU Flags </monetization/skus#sku-object-sku-flags>`
    """

    available          = 1 << 2
    guild_subscription = 1 << 7
    user_subscription  = 1 << 8


class EntitlementType(enum.IntEnum):

    """
    |dsrc|
    :ddoc:`Entitlement Types </monetization/entitlements#entitlement-object-entitlement-types>`
    """

    application_subscription = 8


class EntitlementOwnerType(enum.IntEnum):

    """
    |dsrc|
    :ddoc:`Entitlement Owner Type </monetization/entitlements#create-test-entitlement>`
    """

    guild_subscription = 1
    user_subscription  = 2