import typing

from . import types as _types
from . import enums as _enums


__all__ = (
    'ApplicationCommand', 'ApplicationCommandOption', 
    'ApplicationCommandOptionChoice', 'GuildApplicationCommandPermissions',
    'ApplicationCommandPermission', 'MessageActionRowComponent',
    'MessageButtonComponent', 'MessageSelectMenuComponent', 
    'MessageSelectMenuComponentDefaultValue', 
    'MessageSelectMenuComponentOption', 'MessageTextInputComponent', 
    'Interaction', 'ApplicationCommandInteractionData', 
    'ApplicationCommandInteractionDataOption', 
    'MessageComponentInteractionData', 'ModalSubmitInteractionData', 
    'ResolvedInteractionData', 'MessageInteraction', 'InteractionResponse', 
    'MessageInteractionResponse', 'AutocompleteInteractionResponse',
    'ModalInteractionResponse', 'Application', 
    'ApplicationIntegrationTypeConfiguration','ApplicationInstallParams', 
    'ApplicationRoleConnectionMetadata', 'AuditLog', 'AuditLogEntry', 
    'OptionalAuditLogEntryInfo', 'AuditLogChange', 'AutoModerationRule', 
    'AutoModerationTriggerMetadata', 'AutoModerationAction', 
    'AutoModerationActionMetadata', 'Channel', 'Message', 'MessageActivity', 
    'MessageInteractionMetadata', 'MessageReference', 'Reaction', 
    'FollowedChannel', 'Overwrite', 'ThreadMetadata', 'ThreadMember', 
    'DefaultReaction', 'ForumTag', 'Embed', 'EmbedThumbnail', 'EmbedVideo', 
    'EmbedImage', 'EmbedProvider', 'EmbedAuthor', 'EmbedFooter', 'EmbedField', 
    'Attachment', 'AllowedMentions', 'RoleSubscriptionData', 'Emoji', 'Guild', 
    'GuildWidgetSettings', 'GuildWidget', 'GuildMember', 'Integration', 
    'IntegrationAccount', 'IntegrationApplication', 'Ban', 'WelcomeScreen', 
    'WelcomeScreenChannel', 'GuildOnboarding', 'GuildOnboardingPrompt', 
    'GuildOnboardingPromptOption', 'GuildScheduledEvent', 
    'GuildScheduledEventEntityMetadata', 'GuildScheduledEventUser', 
    'GuildTemplate', 'Invite', 'InviteStageInstance', 'StageInstance', 
    'Sticker', 'StickerPack', 'User', 'Connection', 
    'ApplicationRoleConnection', 'VoiceState', 'VoiceRegion', 
    'Webhook', 'Presence', 'ClientStatus', 'Activity', 'ActivityTimestamps', 
    'ActivityParty', 'ActivityAssets', 'ActivitySecrets', 'ActivityButton', 
    'Role', 'RoleTags', 'Team', 'TeamMember', 'SKU', 'Entitlement'
)


class ApplicationCommand(typing.TypedDict):
    
    id                        : _types.Snowflake
    type                      : _enums.ApplicationCommandType
    application_id            : _types.Snowflake
    guild_id                  : _types.Snowflake
    name                      : _types.String
    name_localizations        : dict[_enums.Locale, _types.String]
    description               : _types.String
    description_localizations : dict[_enums.Locale, _types.String]
    options                   : list['ApplicationCommandOption']
    default_member_permissions: _enums.Permissions
    # dm_permission             : _types.Boolean
    default_permission        : _types.Boolean
    nsfw                      : _types.Boolean
    version                   : _types.Snowflake
    integration_types         : list[_enums.ApplicationIntegrationType]
    contexts                  : list[_enums.InteractionContextType]


class ApplicationCommandOption(typing.TypedDict):
    
    type                     : _enums.ApplicationCommandOptionType
    name                     : _types.String
    name_localizations       : dict[_enums.Locale, _types.String]
    description              : _types.String
    description_localizations: dict[_enums.Locale, _types.String]
    required                 : _types.Boolean
    choices                  : list['ApplicationCommandOptionChoice']
    options                  : list['ApplicationCommandOption']
    channel_types            : list[_enums.ChannelType]
    min_value                : typing.Union[_types.Integer, _types.Decimal]
    max_value                : typing.Union[_types.Integer, _types.Decimal]
    min_length               : _types.Integer
    max_length               : _types.Integer
    autocomplete             : _types.Boolean


class ApplicationCommandOptionChoice(typing.TypedDict):
    
    name              : _types.String
    name_localizations: dict[_enums.Locale, _types.String]
    value             : typing.Union[_types.String, _types.Integer, _types.Decimal]


class GuildApplicationCommandPermissions(typing.TypedDict):

    id            : _types.Snowflake
    application_id: _types.Snowflake
    guild_id      : _types.Snowflake
    permissions   : _types.Collection['ApplicationCommandPermission']


class ApplicationCommandPermission(typing.TypedDict):

    id        : _types.Snowflake
    type      : _enums.ApplicationCommandPermissionType
    permission: _types.Boolean


class MessageActionRowComponent(typing.TypedDict):
    
    type      : _enums.MessageComponentType
    components: list[typing.Union['MessageButtonComponent', 'MessageSelectMenuComponent', 'MessageTextInputComponent']]


class MessageButtonComponent(typing.TypedDict):
    
    type     : _types.Integer
    style    : _types.Integer
    label    : _types.String
    emoji    : 'Emoji'
    custom_id: _types.String
    url      : _types.String
    disabled : _types.Boolean


class MessageSelectMenuComponent(typing.TypedDict):
    
    type          : _enums.MessageComponentType
    custom_id     : _types.String
    options       : list['MessageSelectMenuComponentOption']
    channel_types : list[_enums.ChannelType]
    placeholder   : _types.String
    default_values: list['MessageSelectMenuComponentDefaultValue']
    min_values    : _types.Integer
    max_values    : _types.Integer
    disabled      : _types.Boolean


class MessageSelectMenuComponentOption(typing.TypedDict):
    
    label      : _types.String
    value      : _types.String
    description: _types.String
    emoji      : 'Emoji'
    default    : _types.Boolean


class MessageSelectMenuComponentDefaultValue(typing.TypedDict):

    id: _types.Snowflake
    type: _enums.MessageSelectMenuComponentDefaultValueType


class MessageTextInputComponent(typing.TypedDict):
    
    type       : _types.Integer
    custom_id  : _types.String
    style      : _enums.MessageTextInputComponentStyle
    label      : _types.String
    min_length : _types.Integer
    max_length : _types.Integer
    required   : _types.Boolean
    value      : _types.String
    placeholder: _types.String


class Interaction(typing.TypedDict):
    
    id                            : _types.Snowflake
    application_id                : _types.Snowflake
    type                          : _enums.InteractionType
    data                          : typing.Union['ApplicationCommandInteractionData', 'MessageComponentInteractionData', 'ModalSubmitInteractionData', 'ResolvedInteractionData']
    guild_id                      : _types.Snowflake
    channel                       : 'Channel'
    channel_id                    : _types.Snowflake
    member                        : 'GuildMember'
    user                          : 'User'
    token                         : _types.String
    version                       : _types.Integer
    message                       : 'Message'
    app_permissions               : _types.String
    locale                        : _types.String
    guild_locale                  : _types.String
    entitlements                  : list['Entitlement']
    authorizing_integration_owners: dict[_enums.ApplicationIntegrationType, _types.Snowflake]
    context                       : _enums.InteractionContextType


class ApplicationCommandInteractionData(typing.TypedDict):
    
    id       : _types.Snowflake
    name     : _types.String
    type     : _types.Integer
    resolved : 'ResolvedInteractionData'
    options  : list['ApplicationCommandInteractionDataOption']
    guild_id : _types.Snowflake
    target_id: _types.Snowflake


class ApplicationCommandInteractionDataOption(typing.TypedDict):
    
    name   : _types.String
    type   : _types.Integer
    value  : typing.Union[_types.String, _types.Integer, _types.Decimal, _types.Boolean]
    options: list['ApplicationCommandInteractionDataOption']
    focused: _types.Boolean


class MessageComponentInteractionData(typing.TypedDict):
    
    custom_id     : _types.String
    component_type: _types.Integer
    values        : list['MessageSelectMenuComponent']


class ModalSubmitInteractionData(typing.TypedDict):
    
    custom_id : _types.String
    components: list[typing.Union['MessageActionRowComponent', 'MessageButtonComponent', 'MessageSelectMenuComponent', 'MessageTextInputComponent']]


class ResolvedInteractionData(typing.TypedDict):
    
    users        : list['User']
    guild_members: list['GuildMember']
    channels     : list['Channel']
    messages     : list['Message']
    attachments  : list['Attachment']


class MessageInteraction(typing.TypedDict):
    
    id          : _types.Snowflake
    type        : _enums.InteractionType
    name        : _types.String
    user        : 'User'
    guild_member: 'GuildMember'


class InteractionResponse(typing.TypedDict):
    
    type: _enums.InteractionResponseType
    data: typing.Union['MessageInteractionResponse', 'AutocompleteInteractionResponse', 'ModalInteractionResponse']


class MessageInteractionResponse(typing.TypedDict):

    tts             : typing.Optional[_types.Boolean]
    content         : typing.Optional[_types.String]
    embeds          : typing.Optional[list['Embed']]
    allowed_mentions: typing.Optional['AllowedMentions']
    flags           : typing.Optional[_enums.MessageFlags]
    components      : typing.Optional[list[typing.Union['MessageButtonComponent', 'MessageSelectMenuComponent', 'MessageTextInputComponent']]]
    attachments     : typing.Optional[list['Attachment']]


class AutocompleteInteractionResponse(typing.TypedDict):

    choices: list['ApplicationCommandOptionChoice']


class ModalInteractionResponse(typing.TypedDict):

    custom_id : _types.String
    title     : _types.String
    components: list[typing.Union['MessageButtonComponent', 'MessageSelectMenuComponent', 'MessageTextInputComponent']]


class Application(typing.TypedDict):
    
    id                               : _types.Snowflake
    name                             : _types.String
    icon                             : typing.Optional[_types.String]
    description                      : _types.String
    rpc_origins                      : list[_types.String]
    bot_public                       : _types.Boolean
    bot_require_code_grant           : _types.Boolean
    terms_of_service_url             : _types.String
    privacy_policy_url               : _types.String
    owner                            : 'User'
    verify_key                       : _types.String
    team                             : typing.Optional['Team']
    guild_id                         : _types.Snowflake
    primary_sku_id                   : _types.Snowflake
    slug                             : _types.String
    cover_image                      : _types.String
    flags                            : _types.Integer
    tags                             : list[_types.String]
    install_params                   : 'ApplicationInstallParams'
    custom_install_url               : _types.String
    role_connections_verification_url: _types.String
    integration_types_config         : dict[_enums.ApplicationIntegrationType, 'ApplicationIntegrationTypeConfiguration']


class ApplicationIntegrationTypeConfiguration(typing.TypedDict):

    oauth2_install_params: 'ApplicationInstallParams'


class ApplicationInstallParams(typing.TypedDict):
    
    scopes     : list[_types.String]
    permissions: _enums.Permissions


class ApplicationRoleConnectionMetadata(typing.TypedDict):
    
    type                     : _enums.ApplicationRoleConnectionMetadataType
    key                      : _types.String
    name                     : _types.String
    name_localizations       : dict[_enums.Locale, _types.String]
    description              : _types.String
    description_localizations: dict[_enums.Locale, _types.String]


class AuditLog(typing.TypedDict):
    
    application_commands  : list['ApplicationCommand']
    audit_log_entries     : list['AuditLogEntry']
    auto_moderation_rules : list['AutoModerationRule']
    guild_scheduled_events: list['GuildScheduledEvent']
    integrations          : list['Integration']
    threads               : list['Channel']
    users                 : list['User']
    webhooks              : list['Webhook']


class AuditLogEntry(typing.TypedDict):
    
    target_id  : typing.Optional[_types.String]
    changes    : list['AuditLogChange']
    user_id    : typing.Optional[_types.Snowflake]
    id         : _types.Snowflake
    action_type: _enums.AuditLogEvent
    options    : 'OptionalAuditLogEntryInfo'
    reason     : _types.String


class OptionalAuditLogEntryInfo(typing.TypedDict):
    
    application_id                   : _types.Snowflake
    auto_moderation_rule_name        : _types.String
    auto_moderation_rule_trigger_type: _types.String
    channel_id                       : _types.Snowflake
    count                            : _types.String
    delete_member_days               : _types.String
    id                               : _types.Snowflake
    members_removed                  : _types.String
    message_id                       : _types.Snowflake
    role_name                        : _types.String
    type                             : _enums.OptionalAuditLogEntryInfoOverwrittenEntityType


class AuditLogChange(typing.TypedDict):
    
    new_value: typing.Any
    old_value: typing.Any
    key      : _types.String


class AutoModerationRule(typing.TypedDict):
    
    id              : _types.Snowflake
    guild_id        : _types.Snowflake
    name            : _types.String
    creator_id      : _types.Snowflake
    event_type      : _enums.AutoModerationRuleEventType
    trigger_type    : _enums.AutoModerationTriggerType
    trigger_metadata: 'AutoModerationTriggerMetadata'
    actions         : list['AutoModerationAction']
    enabled         : _types.Boolean
    exempt_roles    : list[_types.Snowflake]
    exempt_channels : list[_types.Snowflake]


class AutoModerationTriggerMetadata(typing.TypedDict):
    
    keyword_filter                 : list[_types.String]
    regex_patterns                 : list[_types.String]
    presets                        : list[_enums.AutoModerationRuleKeywordPresetType]
    allow_list                     : list[_types.String]
    mention_total_limit            : _types.Integer
    mention_raid_protection_enabled: _types.Boolean


class AutoModerationAction(typing.TypedDict):
    
    type    : _enums.AutoModerationActionType
    metadata: 'AutoModerationActionMetadata'


class AutoModerationActionMetadata(typing.TypedDict):
    
    channel_id      : _types.Snowflake
    duration_seconds: _types.Integer
    custom_message  : _types.String


class Channel(typing.TypedDict):
    
    id                                : _types.Snowflake
    type                              : _enums.ChannelType
    guild_id                          : _types.Snowflake
    position                          : _types.Integer
    permission_overwrites             : list['Overwrite']
    name                              : typing.Optional[_types.String]
    topic                             : typing.Optional[_types.String]
    nsfw                              : _types.Boolean
    last_message_id                   : typing.Optional[_types.Snowflake]
    bitrate                           : _types.Integer
    user_limit                        : _types.Integer
    rate_limit_per_user               : _types.Integer
    recipients                        : list['User']
    icon                              : typing.Optional[_types.String]
    owner_id                          : _types.Snowflake
    application_id                    : _types.Snowflake
    managed                           : _types.Boolean
    parent_id                         : typing.Optional[_types.Snowflake]
    last_pin_timestamp                : typing.Optional[_types.ISO8601Timestamp]
    rtc_region                        : typing.Optional[_types.String]
    video_quality_mode                : _enums.ChannelVideoQualityMode
    message_count                     : _types.Integer
    member_count                      : _types.Integer
    thread_metadata                   : 'ThreadMetadata'
    member                            : 'ThreadMember'
    default_auto_archive_duration     : _types.Integer
    permissions                       : _enums.Permissions
    flags                             : _enums.ChannelFlags
    total_message_sent                : _types.Integer
    available_tags                    : list['ForumTag']
    applied_tags                      : list[_types.Snowflake]
    default_reaction_emoji            : typing.Optional['DefaultReaction']
    default_thread_rate_limit_per_user: _types.Integer
    default_sort_order                : typing.Optional[_enums.ChannelSortOrderType]
    default_forum_layout              : _enums.ForumLayoutType


class Message(typing.TypedDict):
    
    id                    : _types.Snowflake
    channel_id            : _types.Snowflake
    author                : 'User'
    content               : _types.String
    timestamp             : _types.ISO8601Timestamp
    edited_timestamp      : typing.Optional[_types.ISO8601Timestamp]
    tts                   : _types.Boolean
    mention_everyone      : _types.Boolean
    mentions              : list['User']
    mention_roles         : list[_types.Snowflake]
    mention_channels      : list['Channel']
    attachments           : list['Attachment']
    embeds                : list['Embed']
    reactions             : list['Reaction']
    nonce                 : _types.String | _types.Integer
    pinned                : _types.Boolean
    webhook_id            : _types.Snowflake
    type                  : _enums.MessageType
    activity              : 'MessageActivity'
    application           : 'Application'
    application_id        : _types.Snowflake
    message_reference     : 'MessageReference'
    flags                 : _enums.MessageFlags
    referenced_message    : typing.Optional['Message']
    interaction           : 'MessageInteraction'
    thread                : 'Channel'
    components            : list['MessageActionRowComponent']
    stickers              : list['Sticker']
    position              : _types.Integer
    role_subscription_data: 'RoleSubscriptionData'
    interaction_metadata  : 'MessageInteractionMetadata'


class MessageActivity(typing.TypedDict):
    
    type    : _enums.MessageActivityType
    party_id: _types.String


class MessageInteractionMetadata(typing.TypedDict):

    id                             : _types.Snowflake
    type                           : _enums.InteractionType
    user_id                        : _types.Snowflake
    authorizing_integration_owners : dict[_enums.ApplicationIntegrationType, typing.Any]
    original_response_message_id   : _types.Snowflake
    interacted_message_id          : _types.Snowflake
    triggering_interaction_metadata: 'MessageInteractionMetadata'


class MessageReference(typing.TypedDict):
    
    message_id        : _types.Snowflake
    channel_id        : _types.Snowflake
    guild_id          : _types.Snowflake
    fail_if_not_exists: _types.Boolean


class Reaction(typing.TypedDict):
    
    count: _types.Integer
    me   : _types.Boolean
    emoji: 'Emoji'


class FollowedChannel(typing.TypedDict):
    
    channel_id: _types.Snowflake
    webhook_id: _enums.OverwriteType


class Overwrite(typing.TypedDict):
    
    id   : _types.Snowflake
    type : _enums.OverwriteType
    allow: _enums.Permissions
    deny : _enums.Permissions


class ThreadMetadata(typing.TypedDict):
    
    archived             : _types.Boolean
    auto_archive_duration: _types.Integer
    archive_timestamp    : _types.ISO8601Timestamp
    locked               : _types.Boolean
    invitable            : _types.Boolean
    create_timestamp     : typing.Optional[_types.ISO8601Timestamp]


class ThreadMember(typing.TypedDict):
    
    thread_id     : _types.Snowflake
    user_id       : _types.Snowflake
    join_timestamp: _types.ISO8601Timestamp
    flags         : _types.Integer
    member        : 'GuildMember'


class DefaultReaction(typing.TypedDict):
    
    emoji_id  : typing.Optional[_types.Snowflake]
    emoji_name: typing.Optional[_types.String]


class ForumTag(typing.TypedDict):
    
    id        : _types.Snowflake
    name      : _types.String
    moderated : _types.Boolean
    emoji_id  : typing.Optional[_types.Snowflake]
    emoji_name: typing.Optional[_types.String]


class Embed(typing.TypedDict):
    
    title      : _types.String
    type       : _enums.EmbedType
    description: _types.String
    url        : _types.String
    timestamp  : _types.ISO8601Timestamp
    color      : _types.Integer
    footer     : 'EmbedFooter'
    image      : 'EmbedImage'
    thumbnail  : 'EmbedThumbnail'
    video      : 'EmbedVideo'
    provider   : 'EmbedProvider'
    author     : 'EmbedAuthor'
    fields     : list['EmbedField']


class EmbedThumbnail(typing.TypedDict):
    
    url      : _types.String
    proxy_url: _types.String
    height   : _types.Integer
    width    : _types.Integer


class EmbedVideo(typing.TypedDict):
    
    url      : _types.String
    proxy_url: _types.String
    height   : _types.Integer
    width    : _types.Integer


class EmbedImage(typing.TypedDict):
    
    url      : _types.String
    proxy_url: _types.String
    height   : _types.Integer
    width    : _types.Integer


class EmbedProvider(typing.TypedDict):
    
    name: _types.String
    url : _types.String


class EmbedAuthor(typing.TypedDict):
    
    name          : _types.String
    url           : _types.String
    icon_url      : _types.String
    proxy_icon_url: _types.String


class EmbedFooter(typing.TypedDict):
    
    text          : _types.String
    icon_url      : _types.String
    proxy_icon_url: _types.String


class EmbedField(typing.TypedDict):
    
    name  : _types.String
    value : _types.String
    inline: _types.Boolean


class Attachment(typing.TypedDict):
    
    id           : _types.Snowflake
    filename     : _types.String
    description  : _types.String
    content_type : _types.String
    size         : _types.Integer
    url          : _types.String
    proxy_url    : _types.String
    height       : typing.Optional[_types.Integer]
    width        : typing.Optional[_types.Integer]
    ephemeral    : _types.Boolean
    duration_secs: _types.Decimal
    waveform     : _types.String


class AllowedMentions(typing.TypedDict):
    
    parse       : list[_enums.AllowedMentionsType]
    roles       : list[_types.Snowflake]
    users       : list[_types.Snowflake]
    replied_user: _types.Boolean


class RoleSubscriptionData(typing.TypedDict):
    
    role_subscription_listing_id: _types.Snowflake
    tier_name                   : _types.String
    total_months_subscribed     : _types.Integer
    is_renewal                  : _types.Boolean


class Emoji(typing.TypedDict):
    
    id            : typing.Optional[_types.Snowflake]
    name          : typing.Optional[_types.String]
    roles         : list[_types.Snowflake]
    user          : 'User'
    require_colons: _types.Boolean
    managed       : _types.Boolean
    animated      : _types.Boolean
    available     : _types.Boolean


class Guild(typing.TypedDict):
    
    id                           : _types.Snowflake
    name                         : _types.String
    icon                         : typing.Optional[_types.String]
    icon_hash                    : typing.Optional[_types.String]
    splash                       : typing.Optional[_types.String]
    discovery_splash             : typing.Optional[_types.String]
    owner                        : _types.Boolean
    owner_id                     : _types.Snowflake
    permissions                  : _enums.Permissions
    afk_channel_id               : typing.Optional[_types.Snowflake]
    afk_timeout                  : _types.Integer
    widget_enabled               : _types.Boolean
    widget_channel_id            : typing.Optional[_types.Snowflake]
    verification_level           : _enums.GuildVerificationLevel
    default_message_notifications: _enums.GuildDefaultMessageNotificationLevel
    explicit_content_filter      : _enums.GuildExplicitContentFilterLevel
    roles                        : list['Role']
    emojis                       : list['Emoji']
    features                     : list[_enums.GuildFeature]
    mfa_level                    : _types.Integer
    application_id               : typing.Optional[_types.Snowflake]
    system_channel_id            : typing.Optional[_types.Snowflake]
    system_channel_flags         : _enums.GuildSystemChannelFlags
    rules_channel_id             : typing.Optional[_types.Snowflake]
    max_presences                : typing.Optional[_types.Integer]
    max_members                  : _types.Integer
    vanity_url_code              : typing.Optional[_types.String]
    description                  : typing.Optional[_types.String]
    banner                       : typing.Optional[_types.String]
    premium_tier                 : _enums.GuildPremiumTier
    premium_subscription_count   : _types.Integer
    preferred_locale             : _types.String
    public_updates_channel_id    : typing.Optional[_types.Snowflake]
    max_video_channel_users      : _types.Integer
    max_stage_video_channel_users: _types.Integer
    approximate_member_count     : _types.Integer
    approximate_presence_count   : _types.Integer
    welcome_screen               : 'WelcomeScreen'
    nsfw_level                   : _enums.GuildNSFWLevel
    stickers                     : list['Sticker']
    premium_progress_bar_enabled : _types.Boolean
    joined_at                    : _types.ISO8601Timestamp
    large                        : _types.Boolean
    unavailable                  : _types.Boolean
    member_count                 : _types.Integer
    voice_states                 : list['VoiceState']
    members                      : list['GuildMember']
    channels                     : list['Channel']
    threads                      : list['Channel']
    presences                    : list['Presence']
    stage_instances              : list['StageInstance']
    scheduled_events             : list['GuildScheduledEvent']
    safety_alerts_channel_id     : _types.Snowflake


class GuildWidgetSettings(typing.TypedDict):
    
    enabled   : _types.Boolean
    channel_id: typing.Optional[_types.Snowflake]


class GuildWidget(typing.TypedDict):
    
    id            : _types.Snowflake
    name          : _types.String
    instant_invite: typing.Optional[_types.String]
    channels      : list['Channel']
    members       : list['User']
    presence_count: _types.Integer


class GuildMember(typing.TypedDict):
    
    user                        : 'User'
    nick                        : typing.Optional[_types.String]
    avatar                      : typing.Optional[_types.String]
    roles                       : list[_types.Snowflake]
    joined_at                   : _types.ISO8601Timestamp
    premium_since               : typing.Optional[_types.ISO8601Timestamp]
    deaf                        : _types.Boolean
    mute                        : _types.Boolean
    flags                       : _enums.GuildMemberFlags
    pending                     : _types.Boolean
    permissions                 : _enums.Permissions
    communication_disabled_until: typing.Optional[_types.ISO8601Timestamp]


class Integration(typing.TypedDict):
    
    id                 : _types.Snowflake
    name               : _types.String
    type               : _types.String
    enabled            : _types.Boolean
    syncing            : _types.Boolean
    role_id            : _types.Snowflake
    enable_emoticons   : _types.Boolean
    expire_behavior    : _enums.IntegrationExpireBehaviorType
    expire_grace_period: _types.Integer
    user               : 'User'
    account            : 'IntegrationAccount'
    synced_at          : _types.ISO8601Timestamp
    subscriber_count   : _types.Integer
    revoked            : _types.Boolean
    application        : 'Application'
    scopes             : list[_types.String]


class IntegrationAccount(typing.TypedDict):
    
    id  : _types.String
    name: _types.String


class IntegrationApplication(typing.TypedDict):
    
    id         : _types.Snowflake
    name       : _types.String
    icon       : typing.Optional[_types.String]
    description: _types.String
    bot        : 'User'


class Ban(typing.TypedDict):
    
    reason: typing.Optional[_types.String]
    user  : 'User'


class WelcomeScreen(typing.TypedDict):
    
    description     : typing.Optional[_types.String]
    welcome_channels: list['WelcomeScreenChannel']


class WelcomeScreenChannel(typing.TypedDict):
    
    channel_id : _types.Snowflake
    description: _types.String
    emoji_id   : typing.Optional[_types.Snowflake]
    emoji_name : typing.Optional[_types.String]


class GuildOnboarding(typing.TypedDict):
    
    guild_id           : _types.Snowflake
    prompts            : list['GuildOnboardingPrompt']
    default_channel_ids: list[_types.Snowflake]
    enabled            : _types.Boolean


class GuildOnboardingPrompt(typing.TypedDict):
    
    id           : _types.Snowflake
    type         : _enums.GuildOnboardingPromptType
    options      : list['GuildOnboardingPromptOption']
    title        : _types.String
    single_select: _types.Boolean
    required     : _types.Boolean
    in_onboarding: _types.Boolean


class GuildOnboardingPromptOption(typing.TypedDict):
    
    id         : _types.Snowflake
    channel_ids: list[_types.Snowflake]
    role_ids   : list[_types.Snowflake]
    emoji      : 'Emoji'
    title      : _types.String
    description: typing.Optional[_types.String]


class GuildScheduledEvent(typing.TypedDict):
    
    id                  : _types.Snowflake
    guild_id            : _types.Snowflake
    channel_id          : typing.Optional[_types.Snowflake]
    creator_id          : typing.Optional[_types.Snowflake]
    name                : _types.String
    description         : typing.Optional[_types.String]
    scheduled_start_time: _types.ISO8601Timestamp
    scheduled_end_time  : typing.Optional[_types.ISO8601Timestamp]
    privacy_level       : _enums.GuildScheduledEventPrivacyLevel
    status              : _enums.GuildScheduledEventStatus
    entity_type         : _enums.GuildScheduledEventEntityType
    entity_id           : typing.Optional[_types.Snowflake]
    entity_metadata     : typing.Optional['GuildScheduledEventEntityMetadata']
    creator             : 'User'
    user_count          : _types.Integer
    image               : typing.Optional[_types.String]


class GuildScheduledEventEntityMetadata(typing.TypedDict):
    
    location: _types.String


class GuildScheduledEventUser(typing.TypedDict):
    
    guild_scheduled_event_id: _types.Snowflake
    user                    : 'User'
    member                  : 'GuildMember'


class GuildTemplate(typing.TypedDict):
    
    code                   : _types.String
    name                   : _types.String
    description            : typing.Optional[_types.String]
    usage_count            : _types.Integer
    creator_id             : _types.Snowflake
    creator                : 'User'
    created_at             : _types.ISO8601Timestamp
    updated_at             : _types.ISO8601Timestamp
    source_guild_id        : _types.Snowflake
    serialized_source_guild: 'Guild'
    is_dirty               : typing.Optional[_types.Boolean]


class Invite(typing.TypedDict):
    
    code                      : _types.String
    guild                     : 'Guild'
    channel                   : typing.Optional['Channel']
    inviter                   : 'User'
    target_type               : _enums.InviteTargetType
    target_user               : 'User'
    target_application        : 'Application'
    approximate_presence_count: _types.Integer
    approximate_member_count  : _types.Integer
    expires_at                : typing.Optional[_types.ISO8601Timestamp]
    stage_instance            : 'InviteStageInstance'
    guild_scheduled_event     : 'GuildScheduledEvent'
    uses                      : _types.Integer
    max_uses                  : _types.Integer
    max_age                   : _types.Integer
    temporary                 : _types.Boolean
    created_at                : _types.ISO8601Timestamp


class InviteStageInstance(typing.TypedDict):
    
    members          : list['GuildMember']
    participant_count: _types.Integer
    speaker_count    : _types.Integer
    topic            : _types.String


class StageInstance(typing.TypedDict):
    
    id                      : _types.Snowflake
    guild_id                : _types.Snowflake
    channel_id              : _types.Snowflake
    topic                   : _types.String
    privacy_level           : _enums.StageInstancePrivacyLevel
    discoverable_disabled   : _types.Boolean
    guild_scheduled_event_id: typing.Optional[_types.Snowflake]


class Sticker(typing.TypedDict):
    
    id         : _types.Snowflake
    pack_id    : _types.Snowflake
    name       : _types.String
    description: typing.Optional[_types.String]
    tags       : _types.String
    asset      : _types.String
    type       : _enums.StickerType
    format_type: _enums.StickerFormatType
    available  : _types.Boolean
    guild_id   : _types.Snowflake
    user       : 'User'
    sort_value : _types.Integer


class StickerPack(typing.TypedDict):
    
    id              : _types.Snowflake
    stickers        : list['Sticker']
    name            : _types.String
    sku_id          : _types.Snowflake
    cover_sticker_id: _types.Snowflake
    description     : _types.String
    banner_asset_id : _types.Snowflake


class User(typing.TypedDict):
    
    id           : _types.Snowflake
    username     : _types.String
    discriminator: _types.String
    avatar       : typing.Optional[_types.String]
    bot          : _types.Boolean
    system       : _types.Boolean
    mfa_enabled  : _types.Boolean
    banner       : typing.Optional[_types.String]
    accent_color : typing.Optional[_types.Integer]
    locale       : _enums.Locale
    verified     : _types.Boolean
    email        : typing.Optional[_types.String]
    flags        : _enums.UserFlags
    premium_type : _enums.UserPremiumType
    public_flags : _enums.UserFlags


class Connection(typing.TypedDict):
    
    id           : _types.String
    name         : _types.String
    type         : _types.String
    revoked      : _types.Boolean
    integrations : list['Integration']
    verified     : _types.Boolean
    friend_sync  : _types.Boolean
    show_activity: _types.Boolean
    two_way_link : _types.Boolean
    visibility   : _enums.ConnectionVisibilityType


class ApplicationRoleConnection(typing.TypedDict):
    
    platform_name    : typing.Optional[_types.String]
    platform_username: typing.Optional[_types.String]
    metadata         : dict[_types.String, 'ApplicationRoleConnectionMetadata']


class VoiceState(typing.TypedDict):
    
    guild_id                  : _types.Snowflake
    channel_id                : typing.Optional[_types.Snowflake]
    user_id                   : _types.Snowflake
    member                    : 'GuildMember'
    session_id                : _types.String
    deaf                      : _types.Boolean
    mute                      : _types.Boolean
    self_deaf                 : _types.Boolean
    self_mute                 : _types.Boolean
    self_stream               : _types.Boolean
    self_video                : _types.Boolean
    suppress                  : _types.Boolean
    request_to_speak_timestamp: typing.Optional[_types.ISO8601Timestamp]


class VoiceRegion(typing.TypedDict):
    
    id        : _types.String
    name      : _types.String
    optimal   : _types.Boolean
    deprecated: _types.Boolean
    custom    : _types.Boolean


class Webhook(typing.TypedDict):
    
    id            : _types.Snowflake
    type          : _enums.WebhookType
    guild_id      : typing.Optional[_types.Snowflake]
    channel_id    : typing.Optional[_types.Snowflake]
    user          : 'User'
    name          : typing.Optional[_types.String]
    avatar        : typing.Optional[_types.String]
    token         : _types.String
    application_id: typing.Optional[_types.Snowflake]
    source_guild  : 'Guild'
    source_channel: 'Channel'
    url           : _types.String


class Presence(typing.TypedDict):
    
    user         : 'User'
    guild_id     : _types.Snowflake
    status       : _enums.StatusType
    activities   : list['Activity']
    client_status: 'ClientStatus'


class ClientStatus(typing.TypedDict):
    
    desktop: _types.String
    mobile : _types.String
    web    : _types.String


class Activity(typing.TypedDict):
    
    name          : _types.String
    type          : _enums.ActivityType
    url           : typing.Optional[_types.String]
    created_at    : _types.Timestamp
    timestamps    : 'ActivityTimestamps'
    application_id: _types.Snowflake
    details       : typing.Optional[_types.String]
    state         : typing.Optional[_types.String]
    emoji         : typing.Optional['Emoji']
    party         : 'ActivityParty'
    assets        : 'ActivityAssets'
    secrets       : 'ActivitySecrets'
    instance      : _types.Boolean
    flags         : _enums.ActivityFlags
    buttons       : list['ActivityButton']


class ActivityTimestamps(typing.TypedDict):
    
    start: _types.Timestamp
    end  : _types.Timestamp


class ActivityParty(typing.TypedDict):
    
    id  : _types.String
    size: list[_types.Integer]


class ActivityAssets(typing.TypedDict):
    
    large_image: _types.String
    large_text : _types.String
    small_image: _types.String
    small_text : _types.String


class ActivitySecrets(typing.TypedDict):
    
    join    : _types.String
    spectate: _types.String
    match   : _types.String


class ActivityButton(typing.TypedDict):
    
    label: _types.String
    url  : _types.String


class Role(typing.TypedDict):
    
    id           : _types.Snowflake
    name         : _types.String
    color        : _types.Integer
    hoist        : _types.Boolean
    icon         : typing.Optional[_types.String]
    unicode_emoji: typing.Optional[_types.String]
    position     : _types.Integer
    permissions  : _types.String
    managed      : _types.Boolean
    mentionable  : _types.Boolean
    tags         : 'RoleTags'


class RoleTags(typing.TypedDict):
    
    bot_id                 : _types.Snowflake
    integration_id         : _types.Snowflake
    premium_subscriber     : _types.Boolean
    subscription_listing_id: _types.Snowflake
    available_for_purchase : _types.Boolean
    guild_connections      : _types.Boolean


class Team(typing.TypedDict):
    
    icon         : typing.Optional[_types.String]
    id           : _types.Snowflake
    members      : list['TeamMember']
    name         : _types.String
    owner_user_id: _types.Snowflake


class TeamMember(typing.TypedDict):
    
    membership_state: _enums.TeamMemberMembershipState
    permissions     : list[_types.String]
    team_id         : _types.Snowflake
    user            : 'User'


class SKU(typing.TypedDict):

    id            : _types.Snowflake
    type          : _enums.SKUType
    application_id: _types.Snowflake
    name          : _types.String
    slug          : _types.String
    flags         : _enums.SKUFlags


class Entitlement(typing.TypedDict):

    id            : _types.Snowflake
    sku_id        : _types.Snowflake
    application_id: _types.Snowflake
    user_id       : _types.Snowflake
    type          : _enums.EntitlementType
    deleted       : _types.Boolean
    starts_at     : _types.ISO8601Timestamp
    ends_at       : _types.ISO8601Timestamp
    guild_id      : _types.Snowflake