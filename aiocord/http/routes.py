

from . import client as _client


__all__ = (
    'Route',
    'get_global_application_commands', 'create_global_application_command', 
    'get_global_application_command', 'update_global_application_command', 
    'delete_global_application_command', 
    'update_all_global_application_commands', 'get_guild_application_commands', 
    'create_guild_application_command', 'get_guild_application_command', 
    'update_guild_application_command', 'delete_guild_application_command', 
    'update_all_guild_application_commands', 
    'get_guild_application_command_permissions', 
    'get_application_command_permissions', 
    'update_application_command_permissions', 
    # 'update_all_application_command_permissions', 
    'create_interaction_response', 'get_interaction_response', 
    'update_interaction_response', 
    'delete_interaction_response', 'create_followup_message', 
    'get_followup_message', 'update_followup_message', 
    'delete_followup_message', 
    'get_application_role_connection_metadata', 
    'update_application_role_connection_metadata', 
    'get_guild_audit_log', 'get_guild_auto_moderation_rules', 
    'get_auto_moderation_rule', 'create_auto_moderation_rule', 
    'update_auto_moderation_rule', 'delete_auto_moderation_rule', 
    'get_channel', 'update_channel', 'delete_channel', 'get_messages', 
    'get_message', 'create_message', 'create_message_crosspost', 
    'create_reaction', 'delete_own_reaction', 'delete_user_reaction', 
    'get_reactions', 'delete_all_reactions', 'delete_all_emoji_reactions', 
    'update_message', 'delete_message', 'delete_messages', 
    'update_channel_permissions', 'get_channel_invites', 
    'create_channel_invite', 'delete_channel_permission', 
    'create_channel_follow', 'create_typing_indicator', 'get_channel_pins', 
    'create_channel_pin', 'delete_channel_pin', 'create_channel_recipient', 
    'delete_channel_recipient', 'create_message_thread', 'create_thread', 
    'create_self_thread_member', 'create_thread_member', 
    'delete_self_thread_member', 'delete_thread_member', 'get_thread_member', 
    'get_thread_members', 'get_public_archived_threads', 
    'get_private_archived_threads', 'get_self_private_archived_threads', 
    'get_guild_emojis', 'get_guild_emoji', 'create_guild_emoji', 
    'update_guild_emoji', 'delete_guild_emoji', 'create_guild', 'get_guild', 
    'get_guild_preview', 'update_guild', 'delete_guild', 'get_guild_channels', 
    'create_guild_channel', 'update_guild_channel_positions', 
    'get_active_guild_threads', 'get_guild_member', 'get_guild_members', 
    'search_guild_members', 'create_guild_member', 'update_guild_member', 
    'update_self_guild_member', 'create_guild_member_role', 
    'delete_guild_member_role', 'delete_guild_member', 'get_guild_bans', 
    'get_guild_ban', 'create_guild_ban', 'delete_guild_ban', 'get_guild_roles', 
    'create_guild_role', 'update_guild_role_positions', 'update_guild_role', 
    'update_guild_mfa_level', 'delete_guild_role', 'get_guild_prune_count', 
    'start_guild_prune', 'get_guild_voice_regions', 'get_guild_invites', 
    'get_guild_integrations', 'delete_guild_integration', 
    'get_guild_widget_settings', 'update_guild_widget', 'get_guild_widget', 
    'get_guild_vanity_url', 'get_guild_widget_image', 
    'get_guild_welcome_screen', 'update_guild_welcome_screen', 
    'get_guild_onboarding', 'update_self_voice_state', 'update_voice_state', 
    'get_guild_scheduled_events', 'create_guild_scheduled_event', 
    'get_guild_scheduled_event', 'update_guild_scheduled_event', 
    'delete_guild_scheduled_event', 'get_guild_scheduled_event_users', 
    'get_guild_template', 'create_guild_via_guild_template', 
    'get_guild_templates', 'create_guild_template', 'sync_guild_template', 
    'update_guild_template', 'delete_guild_template', 'get_invite',
    'delete_invite', 'create_stage_instance', 'get_stage_instance', 
    'update_stage_instance', 'delete_stage_instance', 'get_sticker', 
    'get_sticker_packs', 'get_guild_stickers', 'get_guild_sticker', 
    'create_guild_sticker', 'update_guild_sticker', 'delete_guild_sticker', 
    'get_self_user', 'get_user', 'update_self_user', 'get_self_guilds', 
    'get_self_guild_member', 'delete_self_guild_member', 'create_self_channel', 
    # 'create_group_channel', 
    'get_self_connections', 'get_self_application_role_connection', 
    'update_self_application_role_connection', 'get_voice_regions', 
    'create_webhook', 'get_channel_webhooks', 'get_guild_webhooks', 
    'get_webhook', 'get_webhook_via_token', 'update_webhook', 
    'update_webhook_via_token', 'delete_webhook', 'delete_webhook_via_token', 
    'create_webhook_message', 'create_webhook_message_slack_compatible', 
    'create_webhook_message_github_compatible', 'get_webhook_message', 
    'update_webhook_message', 'delete_webhook_message', 'get_gateway', 
    'get_gateway_bot', 'get_self_application_information',  
    'get_self_authorization_information', 'get_skus', 'get_entitlements', 
    'create_entitlement', 'delete_entitlement'
)


class Route:
    
    """
    Contains all necessary data to perform a targeted request.

    :param verb:
        The HTTP method.
    :param path_template:
        The formattable path portion for the url.

    .. code-block:: python

        route = Route('GET', '/path/{0}/to/{1}/resource')
        value = await route(client, 'step0', 'step1', json = ..., params = ..., headers = ...)
    """

    __slots__ = ('_verb', '_path_template')

    def __init__(self, 
                 verb         : str,
                 path_template: str):

        self._verb = verb
        self._path_template = path_template

    @property
    def _identity(self):

        return (self._verb, self._path_template)

    def __call__(self, 
                 client: _client.Client, 
                 /,
                 *path_sections, 
                 **kwargs):

        path = self._path_template.format(*path_sections)

        return client.request(self._verb, path, **kwargs, identity = self._identity)
    
    def __repr__(self):

        return f'<{self.__class__.__name__}({self._verb} {self._path_template})>'
    

get_global_application_commands = Route('GET', '/applications/{0}/commands')
"""
|dsrc|
:ddoc:`Get Global Application Commands </interactions/application-commands#get-global-application-commands>`
"""

create_global_application_command = Route('POST', '/applications/{0}/commands')
"""
|dsrc|
:ddoc:`Create Global Application Command </interactions/application-commands#create-global-application-command>`
"""

get_global_application_command = Route('GET', '/applications/{0}/commands/{1}')
"""
|dsrc|
:ddoc:`Get Global Application Command </interactions/application-commands#get-global-application-command>`
"""

update_global_application_command = Route('PATCH', '/applications/{0}/commands/{1}')
"""
|dsrc|
:ddoc:`Edit Global Application Command </interactions/application-commands#edit-global-application-command>`
"""

delete_global_application_command = Route('DELETE', '/applications/{0}/commands/{1}')
"""
|dsrc|
:ddoc:`Delete Global Application Command </interactions/application-commands#delete-global-application-command>`
"""

update_all_global_application_commands = Route('PUT', '/applications/{0}/commands')
"""
|dsrc|
:ddoc:`Bulk Overwrite Global Application Commands </interactions/application-commands#bulk-overwrite-global-application-commands>`
"""

get_guild_application_commands = Route('GET', '/applications/{0}/guilds/{1}/commands')
"""
|dsrc|
:ddoc:`Get Guild Application Commands </interactions/application-commands#get-guild-application-commands>`
"""

create_guild_application_command = Route('POST', '/applications/{0}/guilds/{1}/commands')
"""
|dsrc|
:ddoc:`Create Guild Application Command </interactions/application-commands#create-guild-application-command>`
"""

get_guild_application_command = Route('GET', '/applications/{0}/guilds/{1}/commands/{2}')
"""
|dsrc|
:ddoc:`Get Guild Application Command </interactions/application-commands#get-guild-application-command>`
"""

update_guild_application_command = Route('PATCH', '/applications/{0}/guilds/{1}/commands/{2}')
"""
|dsrc|
:ddoc:`Edit Guild Application Command </interactions/application-commands#edit-guild-application-command>`
"""

delete_guild_application_command = Route('DELETE', '/applications/{0}/guilds/{1}/commands/{2}')
"""
|dsrc|
:ddoc:`Delete Guild Application Command </interactions/application-commands#delete-guild-application-command>`
"""

update_all_guild_application_commands = Route('PUT', '/applications/{0}/guilds/{1}/commands')
"""
|dsrc|
:ddoc:`Bulk Overwrite Guild Application Commands </interactions/application-commands#bulk-overwrite-guild-application-commands>`
"""

get_guild_application_command_permissions = Route('GET', '/applications/{0}/guilds/{1}/commands/permissions')
"""
|dsrc|
:ddoc:`Get Guild Application Command Permissions </interactions/application-commands#get-guild-application-command-permissions>`
"""

get_application_command_permissions = Route('GET', '/applications/{0}/guilds/{1}/commands/{2}/permissions')
"""
|dsrc|
:ddoc:`Get Application Command Permissions </interactions/application-commands#get-application-command-permissions>`
"""

update_application_command_permissions = Route('PUT', '/applications/{0}/guilds/{1}/commands/{2}/permissions')
"""
|dsrc|
:ddoc:`Edit Application Command Permissions </interactions/application-commands#edit-application-command-permissions>`
"""

# update_all_application_command_permissions = Route('PUT', '/applications/{0}/guilds/{1}/commands/permissions')
# """
# |dsrc|
# :ddoc:`Batch Edit Application Command Permissions </interactions/application-commands#batch-edit-application-command-permissions>`
# """

create_interaction_response = Route('POST', '/interactions/{0}/{1}/callback')
"""
|dsrc|
:ddoc:`Create Interaction Response </interactions/receiving-and-responding#create-interaction-response>`
"""

get_interaction_response = Route('GET', '/webhooks/{0}/{1}/messages/@original')
"""
|dsrc|
:ddoc:`Get Original Interaction Response </interactions/receiving-and-responding#get-original-interaction-response>`
"""

update_interaction_response = Route('PATCH', '/webhooks/{0}/{1}/messages/@original')
"""
|dsrc|
:ddoc:`Edit Original Interaction Response </interactions/receiving-and-responding#edit-original-interaction-response>`
"""

delete_interaction_response = Route('DELETE', '/webhooks/{0}/{1}/messages/@original')
"""
|dsrc|
:ddoc:`Delete Original Interaction Response </interactions/receiving-and-responding#delete-original-interaction-response>`
"""

create_followup_message = Route('POST', '/webhooks/{0}/{1}')
"""
|dsrc|
:ddoc:`Create Followup Message </interactions/receiving-and-responding#create-followup-message>`
"""

get_followup_message = Route('GET', '/webhooks/{0}/{1}/messages/{2}')
"""
|dsrc|
:ddoc:`Get Followup Message </interactions/receiving-and-responding#get-followup-message>`
"""

update_followup_message = Route('PATCH', '/webhooks/{0}/{1}/messages/{2}')
"""
|dsrc|
:ddoc:`Edit Followup Message </interactions/receiving-and-responding#edit-followup-message>`
"""

delete_followup_message = Route('DELETE', '/webhooks/{0}/{1}/messages/{2}')
"""
|dsrc|
:ddoc:`Delete Followup Message </interactions/receiving-and-responding#delete-followup-message>`
"""

get_application_role_connection_metadata = Route('GET', '/applications/{0}/role-connections/metadata')
"""
|dsrc|
:ddoc:`Get Application Role Connection Metadata Records </resources/application-role-connection-metadata#get-application-role-connection-metadata-records>`
"""

update_application_role_connection_metadata = Route('PUT', '/applications/{0}/role-connections/metadata')
"""
|dsrc|
:ddoc:`Update Application Role Connection Metadata Records </resources/application-role-connection-metadata#update-application-role-connection-metadata-records>`
"""

get_guild_audit_log = Route('GET', '/guilds/{0}/audit-logs')
"""
|dsrc|
:ddoc:`Get Guild Audit Log </resources/audit-log#get-guild-audit-log>`
"""

get_guild_auto_moderation_rules = Route('GET', '/guilds/{0}/auto-moderation/rules')
"""
|dsrc|
:ddoc:`List Auto Moderation Rules For Guild </resources/auto-moderation#list-auto-moderation-rules-for-guild>`
"""

get_auto_moderation_rule = Route('GET', '/guilds/{0}/auto-moderation/rules/{1}')
"""
|dsrc|
:ddoc:`Get Auto Moderation Rule </resources/auto-moderation#get-auto-moderation-rule>`
"""

create_auto_moderation_rule = Route('POST', '/guilds/{0}/auto-moderation/rules')
"""
|dsrc|
:ddoc:`Create Auto Moderation Rule </resources/auto-moderation#create-auto-moderation-rule>`
"""

update_auto_moderation_rule = Route('PATCH', '/guilds/{0}/auto-moderation/rules/{1}')
"""
|dsrc|
:ddoc:`Modify Auto Moderation Rule </resources/auto-moderation#modify-auto-moderation-rule>`
"""

delete_auto_moderation_rule = Route('DELETE', '/guilds/{0}/auto-moderation/rules/{1}')
"""
|dsrc|
:ddoc:`Delete Auto Moderation Rule </resources/auto-moderation#delete-auto-moderation-rule>`
"""

get_channel = Route('GET', '/channels/{0}')
"""
|dsrc|
:ddoc:`Get Channel </resources/channel#get-channel>`
"""

update_channel = Route('PATCH', '/channels/{0}')
"""
|dsrc|
:ddoc:`Modify Channel </resources/channel#modify-channel>`
"""

delete_channel = Route('DELETE', '/channels/{0}')
"""
|dsrc|
:ddoc:`Delete/Close Channel </resources/channel#delete/close-channel>`
"""

get_messages = Route('GET', '/channels/{0}/messages')
"""
|dsrc|
:ddoc:`Get Channel Messages </resources/channel#get-channel-messages>`
"""

get_message = Route('GET', '/channels/{0}/messages/{1}')
"""
|dsrc|
:ddoc:`Get Channel Message </resources/channel#get-channel-message>`
"""

create_message = Route('POST', '/channels/{0}/messages')
"""
|dsrc|
:ddoc:`Create Message </resources/channel#create-message>`
"""

create_message_crosspost = Route('POST', '/channels/{0}/messages/{1}/crosspost')
"""
|dsrc|
:ddoc:`Crosspost Message </resources/channel#crosspost-message>`
"""

create_reaction = Route('PUT', '/channels/{0}/messages/{1}/reactions/{2}/@me')
"""
|dsrc|
:ddoc:`Create Reaction </resources/channel#create-reaction>`
"""

delete_own_reaction = Route('DELETE', '/channels/{0}/messages/{1}/reactions/{2}/@me')
"""
|dsrc|
:ddoc:`Delete Own Reaction </resources/channel#delete-own-reaction>`
"""

delete_user_reaction = Route('DELETE', '/channels/{0}/messages/{1}/reactions/{2}/{3}')
"""
|dsrc|
:ddoc:`Delete User Reaction </resources/channel#delete-user-reaction>`
"""

get_reactions = Route('GET', '/channels/{0}/messages/{1}/reactions/{2}')
"""
|dsrc|
:ddoc:`Get Reactions </resources/channel#get-reactions>`
"""

delete_all_reactions = Route('DELETE', '/channels/{0}/messages/{1}/reactions')
"""
|dsrc|
:ddoc:`Delete All Reactions </resources/channel#delete-all-reactions>`
"""

delete_all_emoji_reactions = Route('DELETE', '/channels/{0}/messages/{1}/reactions/{2}')
"""
|dsrc|
:ddoc:`Delete All Reactions For Emoji </resources/channel#delete-all-reactions-for-emoji>`
"""

update_message = Route('PATCH', '/channels/{0}/messages/{1}')
"""
|dsrc|
:ddoc:`Edit Message </resources/channel#edit-message>`
"""

delete_message = Route('DELETE', '/channels/{0}/messages/{1}')
"""
|dsrc|
:ddoc:`Delete Message </resources/channel#delete-message>`
"""

delete_messages = Route('POST', '/channels/{0}/messages/bulk-delete')
"""
|dsrc|
:ddoc:`Bulk Delete Messages </resources/channel#bulk-delete-messages>`
"""

update_channel_permissions = Route('PUT', '/channels/{0}/permissions/{1}')
"""
|dsrc|
:ddoc:`Edit Channel Permissions </resources/channel#edit-channel-permissions>`
"""

get_channel_invites = Route('GET', '/channels/{0}/invites')
"""
|dsrc|
:ddoc:`Get Channel Invites </resources/channel#get-channel-invites>`
"""

create_channel_invite = Route('POST', '/channels/{0}/invites')
"""
|dsrc|
:ddoc:`Create Channel Invite </resources/channel#create-channel-invite>`
"""

delete_channel_permission = Route('DELETE', '/channels/{0}/permissions/{1}')
"""
|dsrc|
:ddoc:`Delete Channel Permission </resources/channel#delete-channel-permission>`
"""

create_channel_follow = Route('POST', '/channels/{0}/followers')
"""
|dsrc|
:ddoc:`Follow Announcement Channel </resources/channel#follow-announcement-channel>`
"""

create_typing_indicator = Route('POST', '/channels/{0}/typing')
"""
|dsrc|
:ddoc:`Trigger Typing Indicator </resources/channel#trigger-typing-indicator>`
"""

get_channel_pins = Route('GET', '/channels/{0}/pins')
"""
|dsrc|
:ddoc:`Get Pinned Messages </resources/channel#get-pinned-messages>`
"""

create_channel_pin = Route('PUT', '/channels/{0}/pins/{1}')
"""
|dsrc|
:ddoc:`Pin Message </resources/channel#pin-message>`
"""

delete_channel_pin = Route('DELETE', '/channels/{0}/pins/{1}')
"""
|dsrc|
:ddoc:`Unpin Message </resources/channel#unpin-message>`
"""

create_channel_recipient = Route('PUT', '/channels/{0}/recipients/{1}')
"""
|dsrc|
:ddoc:`Group Dm Add Recipient </resources/channel#group-dm-add-recipient>`
"""

delete_channel_recipient = Route('DELETE', '/channels/{0}/recipients/{1}')
"""
|dsrc|
:ddoc:`Group Dm Remove Recipient </resources/channel#group-dm-remove-recipient>`
"""

create_message_thread = Route('POST', '/channels/{0}/messages/{1}/threads')
"""
|dsrc|
:ddoc:`Start Thread From Message </resources/channel#start-thread-from-message>`
"""

create_thread = Route('POST', '/channels/{0}/threads')
"""
|dsrc|
:ddoc:`Start Thread Without Message </resources/channel#start-thread-without-message>`
"""

create_self_thread_member = Route('PUT', '/channels/{0}/thread-members/@me')
"""
|dsrc|
:ddoc:`Join Thread </resources/channel#join-thread>`
"""

create_thread_member = Route('PUT', '/channels/{0}/thread-members/{1}')
"""
|dsrc|
:ddoc:`Add Thread Member </resources/channel#add-thread-member>`
"""

delete_self_thread_member = Route('DELETE', '/channels/{0}/thread-members/@me')
"""
|dsrc|
:ddoc:`Leave Thread </resources/channel#leave-thread>`
"""

delete_thread_member = Route('DELETE', '/channels/{0}/thread-members/{1}')
"""
|dsrc|
:ddoc:`Remove Thread Member </resources/channel#remove-thread-member>`
"""

get_thread_member = Route('GET', '/channels/{0}/thread-members/{1}')
"""
|dsrc|
:ddoc:`Get Thread Member </resources/channel#get-thread-member>`
"""

get_thread_members = Route('GET', '/channels/{0}/thread-members')
"""
|dsrc|
:ddoc:`List Thread Members </resources/channel#list-thread-members>`
"""

get_public_archived_threads = Route('GET', '/channels/{0}/threads/archived/public')
"""
|dsrc|
:ddoc:`List Public Archived Threads </resources/channel#list-public-archived-threads>`
"""

get_private_archived_threads = Route('GET', '/channels/{0}/threads/archived/private')
"""
|dsrc|
:ddoc:`List Private Archived Threads </resources/channel#list-private-archived-threads>`
"""

get_self_private_archived_threads = Route('GET', '/channels/{0}/users/@me/threads/archived/private')
"""
|dsrc|
:ddoc:`List Joined Private Archived Threads </resources/channel#list-joined-private-archived-threads>`
"""

get_guild_emojis = Route('GET', '/guilds/{0}/emojis')
"""
|dsrc|
:ddoc:`List Guild Emojis </resources/emoji#list-guild-emojis>`
"""

get_guild_emoji = Route('GET', '/guilds/{0}/emojis/{1}')
"""
|dsrc|
:ddoc:`Get Guild Emoji </resources/emoji#get-guild-emoji>`
"""

create_guild_emoji = Route('POST', '/guilds/{0}/emojis')
"""
|dsrc|
:ddoc:`Create Guild Emoji </resources/emoji#create-guild-emoji>`
"""

update_guild_emoji = Route('PATCH', '/guilds/{0}/emojis/{1}')
"""
|dsrc|
:ddoc:`Modify Guild Emoji </resources/emoji#modify-guild-emoji>`
"""

delete_guild_emoji = Route('DELETE', '/guilds/{0}/emojis/{1}')
"""
|dsrc|
:ddoc:`Delete Guild Emoji </resources/emoji#delete-guild-emoji>`
"""

create_guild = Route('POST', '/guilds')
"""
|dsrc|
:ddoc:`Create Guild </resources/guild#create-guild>`
"""

get_guild = Route('GET', '/guilds/{0}')
"""
|dsrc|
:ddoc:`Get Guild </resources/guild#get-guild>`
"""

get_guild_preview = Route('GET', '/guilds/{0}/preview')
"""
|dsrc|
:ddoc:`Get Guild Preview </resources/guild#get-guild-preview>`
"""

update_guild = Route('PATCH', '/guilds/{0}')
"""
|dsrc|
:ddoc:`Modify Guild </resources/guild#modify-guild>`
"""

delete_guild = Route('DELETE', '/guilds/{0}')
"""
|dsrc|
:ddoc:`Delete Guild </resources/guild#delete-guild>`
"""

get_guild_channels = Route('GET', '/guilds/{0}/channels')
"""
|dsrc|
:ddoc:`Get Guild Channels </resources/guild#get-guild-channels>`
"""

create_guild_channel = Route('POST', '/guilds/{0}/channels')
"""
|dsrc|
:ddoc:`Create Guild Channel </resources/guild#create-guild-channel>`
"""

update_guild_channel_positions = Route('PATCH', '/guilds/{0}/channels')
"""
|dsrc|
:ddoc:`Modify Guild Channel Positions </resources/guild#modify-guild-channel-positions>`
"""

get_active_guild_threads = Route('GET', '/guilds/{0}/threads/active')
"""
|dsrc|
:ddoc:`List Active Guild Threads </resources/guild#list-active-guild-threads>`
"""

get_guild_member = Route('GET', '/guilds/{0}/members/{1}')
"""
|dsrc|
:ddoc:`Get Guild Member </resources/guild#get-guild-member>`
"""

get_guild_members = Route('GET', '/guilds/{0}/members')
"""
|dsrc|
:ddoc:`List Guild Members </resources/guild#list-guild-members>`
"""

search_guild_members = Route('GET', '/guilds/{0}/members/search')
"""
|dsrc|
:ddoc:`Search Guild Members </resources/guild#search-guild-members>`
"""

create_guild_member = Route('PUT', '/guilds/{0}/members/{1}')
"""
|dsrc|
:ddoc:`Add Guild Member </resources/guild#add-guild-member>`
"""

update_guild_member = Route('PATCH', '/guilds/{0}/members/{1}')
"""
|dsrc|
:ddoc:`Modify Guild Member </resources/guild#modify-guild-member>`
"""

update_self_guild_member = Route('PATCH', '/guilds/{0}/members/@me')
"""
|dsrc|
:ddoc:`Modify Current Member </resources/guild#modify-current-member>`
"""

create_guild_member_role = Route('PUT', '/guilds/{0}/members/{1}/roles/{2}')
"""
|dsrc|
:ddoc:`Add Guild Member Role </resources/guild#add-guild-member-role>`
"""

delete_guild_member_role = Route('DELETE', '/guilds/{0}/members/{1}/roles/{2}')
"""
|dsrc|
:ddoc:`Remove Guild Member Role </resources/guild#remove-guild-member-role>`
"""

delete_guild_member = Route('DELETE', '/guilds/{0}/members/{1}')
"""
|dsrc|
:ddoc:`Remove Guild Member </resources/guild#remove-guild-member>`
"""

get_guild_bans = Route('GET', '/guilds/{0}/bans')
"""
|dsrc|
:ddoc:`Get Guild Bans </resources/guild#get-guild-bans>`
"""

get_guild_ban = Route('GET', '/guilds/{0}/bans/{1}')
"""
|dsrc|
:ddoc:`Get Guild Ban </resources/guild#get-guild-ban>`
"""

create_guild_ban = Route('PUT', '/guilds/{0}/bans/{1}')
"""
|dsrc|
:ddoc:`Create Guild Ban </resources/guild#create-guild-ban>`
"""

delete_guild_ban = Route('DELETE', '/guilds/{0}/bans/{1}')
"""
|dsrc|
:ddoc:`Remove Guild Ban </resources/guild#remove-guild-ban>`
"""

get_guild_roles = Route('GET', '/guilds/{0}/roles')
"""
|dsrc|
:ddoc:`Get Guild Roles </resources/guild#get-guild-roles>`
"""

create_guild_role = Route('POST', '/guilds/{0}/roles')
"""
|dsrc|
:ddoc:`Create Guild Role </resources/guild#create-guild-role>`
"""

update_guild_role_positions = Route('PATCH', '/guilds/{0}/roles')
"""
|dsrc|
:ddoc:`Modify Guild Role Positions </resources/guild#modify-guild-role-positions>`
"""

update_guild_role = Route('PATCH', '/guilds/{0}/roles/{1}')
"""
|dsrc|
:ddoc:`Modify Guild Role </resources/guild#modify-guild-role>`
"""

update_guild_mfa_level = Route('POST', '/guilds/{0}/mfa')
"""
|dsrc|
:ddoc:`Modify Guild Mfa Level </resources/guild#modify-guild-mfa-level>`
"""

delete_guild_role = Route('DELETE', '/guilds/{0}/roles/{1}')
"""
|dsrc|
:ddoc:`Delete Guild Role </resources/guild#delete-guild-role>`
"""

get_guild_prune_count = Route('GET', '/guilds/{0}/prune')
"""
|dsrc|
:ddoc:`Get Guild Prune Count </resources/guild#get-guild-prune-count>`
"""

start_guild_prune = Route('POST', '/guilds/{0}/prune')
"""
|dsrc|
:ddoc:`Begin Guild Prune </resources/guild#begin-guild-prune>`
"""

get_guild_voice_regions = Route('GET', '/guilds/{0}/regions')
"""
|dsrc|
:ddoc:`Get Guild Voice Regions </resources/guild#get-guild-voice-regions>`
"""

get_guild_invites = Route('GET', '/guilds/{0}/invites')
"""
|dsrc|
:ddoc:`Get Guild Invites </resources/guild#get-guild-invites>`
"""

get_guild_integrations = Route('GET', '/guilds/{0}/integrations')
"""
|dsrc|
:ddoc:`Get Guild Integrations </resources/guild#get-guild-integrations>`
"""

delete_guild_integration = Route('DELETE', '/guilds/{0}/integrations/{1}')
"""
|dsrc|
:ddoc:`Delete Guild Integration </resources/guild#delete-guild-integration>`
"""

get_guild_widget_settings = Route('GET', '/guilds/{0}/widget')
"""
|dsrc|
:ddoc:`Get Guild Widget Settings </resources/guild#get-guild-widget-settings>`
"""

update_guild_widget = Route('PATCH', '/guilds/{0}/widget')
"""
|dsrc|
:ddoc:`Modify Guild Widget </resources/guild#modify-guild-widget>`
"""

get_guild_widget = Route('GET', '/guilds/{0}/widget.json')
"""
|dsrc|
:ddoc:`Get Guild Widget </resources/guild#get-guild-widget>`
"""

get_guild_vanity_url = Route('GET', '/guilds/{0}/vanity-url')
"""
|dsrc|
:ddoc:`Get Guild Vanity Url </resources/guild#get-guild-vanity-url>`
"""

get_guild_widget_image = Route('GET', '/guilds/{0}/widget.png')
"""
|dsrc|
:ddoc:`Get Guild Widget Image </resources/guild#get-guild-widget-image>`
"""

get_guild_welcome_screen = Route('GET', '/guilds/{0}/welcome-screen')
"""
|dsrc|
:ddoc:`Get Guild Welcome Screen </resources/guild#get-guild-welcome-screen>`
"""

update_guild_welcome_screen = Route('PATCH', '/guilds/{0}/welcome-screen')
"""
|dsrc|
:ddoc:`Modify Guild Welcome Screen </resources/guild#modify-guild-welcome-screen>`
"""

get_guild_onboarding = Route('GET', '/guilds/{0}/onboarding')
"""
|dsrc|
:ddoc:`Get Guild Onboarding </resources/guild#get-guild-onboarding>`
"""

update_self_voice_state = Route('PATCH', '/guilds/{0}/voice-states/@me')
"""
|dsrc|
:ddoc:`Modify Current User Voice State </resources/guild#modify-current-user-voice-state>`
"""

update_voice_state = Route('PATCH', '/guilds/{0}/voice-states/{1}')
"""
|dsrc|
:ddoc:`Modify User Voice State </resources/guild#modify-user-voice-state>`
"""

get_guild_scheduled_events = Route('GET', '/guilds/{0}/scheduled-events')
"""
|dsrc|
:ddoc:`List Scheduled Events For Guild </resources/guild-scheduled-event#list-scheduled-events-for-guild>`
"""

create_guild_scheduled_event = Route('POST', '/guilds/{0}/scheduled-events')
"""
|dsrc|
:ddoc:`Create Guild Scheduled Event </resources/guild-scheduled-event#create-guild-scheduled-event>`
"""

get_guild_scheduled_event = Route('GET', '/guilds/{0}/scheduled-events/{1}')
"""
|dsrc|
:ddoc:`Get Guild Scheduled Event </resources/guild-scheduled-event#get-guild-scheduled-event>`
"""

update_guild_scheduled_event = Route('PATCH', '/guilds/{0}/scheduled-events/{1}')
"""
|dsrc|
:ddoc:`Modify Guild Scheduled Event </resources/guild-scheduled-event#modify-guild-scheduled-event>`
"""

delete_guild_scheduled_event = Route('DELETE', '/guilds/{0}/scheduled-events/{1}')
"""
|dsrc|
:ddoc:`Delete Guild Scheduled Event </resources/guild-scheduled-event#delete-guild-scheduled-event>`
"""

get_guild_scheduled_event_users = Route('GET', '/guilds/{0}/scheduled-events/{1}/users')
"""
|dsrc|
:ddoc:`Get Guild Scheduled Event Users </resources/guild-scheduled-event#get-guild-scheduled-event-users>`
"""

get_guild_template = Route('GET', '/guilds/templates/{0}')
"""
|dsrc|
:ddoc:`Get Guild Template </resources/guild-template#get-guild-template>`
"""

create_guild_via_guild_template = Route('POST', '/guilds/templates/{0}')
"""
|dsrc|
:ddoc:`Create Guild From Guild Template </resources/guild-template#create-guild-from-guild-template>`
"""

get_guild_templates = Route('GET', '/guilds/{0}/templates')
"""
|dsrc|
:ddoc:`Get Guild Templates </resources/guild-template#get-guild-templates>`
"""

create_guild_template = Route('POST', '/guilds/{0}/templates')
"""
|dsrc|
:ddoc:`Create Guild Template </resources/guild-template#create-guild-template>`
"""

sync_guild_template = Route('PUT', '/guilds/{0}/templates/{1}')
"""
|dsrc|
:ddoc:`Sync Guild Template </resources/guild-template#sync-guild-template>`
"""

update_guild_template = Route('PATCH', '/guilds/{0}/templates/{1}')
"""
|dsrc|
:ddoc:`Modify Guild Template </resources/guild-template#modify-guild-template>`
"""

delete_guild_template = Route('DELETE', '/guilds/{0}/templates/{1}')
"""
|dsrc|
:ddoc:`Delete Guild Template </resources/guild-template#delete-guild-template>`
"""

get_invite = Route('GET', '/invites/{0}')
"""
|dsrc|
:ddoc:`Get Invite </resources/invite#get-invite>`
"""

delete_invite = Route('DELETE', '/invites/{0}')
"""
|dsrc|
:ddoc:`Delete Invite </resources/invite#delete-invite>`
"""

create_stage_instance = Route('POST', '/stage-instances')
"""
|dsrc|
:ddoc:`Create Stage Instance </resources/stage-instance#create-stage-instance>`
"""

get_stage_instance = Route('GET', '/stage-instances/{0}')
"""
|dsrc|
:ddoc:`Get Stage Instance </resources/stage-instance#get-stage-instance>`
"""

update_stage_instance = Route('PATCH', '/stage-instances/{0}')
"""
|dsrc|
:ddoc:`Modify Stage Instance </resources/stage-instance#modify-stage-instance>`
"""

delete_stage_instance = Route('DELETE', '/stage-instances/{0}')
"""
|dsrc|
:ddoc:`Delete Stage Instance </resources/stage-instance#delete-stage-instance>`
"""

get_sticker = Route('GET', '/stickers/{0}')
"""
|dsrc|
:ddoc:`Get Sticker </resources/sticker#get-sticker>`
"""

get_sticker_packs = Route('GET', '/sticker-packs')
"""
|dsrc|
:ddoc:`List Nitro Sticker Packs </resources/sticker#list-nitro-sticker-packs>`
"""

get_guild_stickers = Route('GET', '/guilds/{0}/stickers')
"""
|dsrc|
:ddoc:`List Guild Stickers </resources/sticker#list-guild-stickers>`
"""

get_guild_sticker = Route('GET', '/guilds/{0}/stickers/{1}')
"""
|dsrc|
:ddoc:`Get Guild Sticker </resources/sticker#get-guild-sticker>`
"""

create_guild_sticker = Route('POST', '/guilds/{0}/stickers')
"""
|dsrc|
:ddoc:`Create Guild Sticker </resources/sticker#create-guild-sticker>`
"""

update_guild_sticker = Route('PATCH', '/guilds/{0}/stickers/{1}')
"""
|dsrc|
:ddoc:`Modify Guild Sticker </resources/sticker#modify-guild-sticker>`
"""

delete_guild_sticker = Route('DELETE', '/guilds/{0}/stickers/{1}')
"""
|dsrc|
:ddoc:`Delete Guild Sticker </resources/sticker#delete-guild-sticker>`
"""

get_self_user = Route('GET', '/users/@me')
"""
|dsrc|
:ddoc:`Get Current User </resources/user#get-current-user>`
"""

get_user = Route('GET', '/users/{0}')
"""
|dsrc|
:ddoc:`Get User </resources/user#get-user>`
"""

update_self_user = Route('PATCH', '/users/@me')
"""
|dsrc|
:ddoc:`Modify Current User </resources/user#modify-current-user>`
"""

get_self_guilds = Route('GET', '/users/@me/guilds')
"""
|dsrc|
:ddoc:`Get Current User Guilds </resources/user#get-current-user-guilds>`
"""

get_self_guild_member = Route('GET', '/users/@me/guilds/{0}/member')
"""
|dsrc|
:ddoc:`Get Current User Guild Member </resources/user#get-current-user-guild-member>`
"""

delete_self_guild_member = Route('DELETE', '/users/@me/guilds/{0}')
"""
|dsrc|
:ddoc:`Leave Guild </resources/user#leave-guild>`
"""

create_self_channel = Route('POST', '/users/@me/channels')
"""
|dsrc|
:ddoc:`Create Dm </resources/user#create-dm>`
"""

# create_group_channel = Route('POST', '/users/@me/channels')
# """
# |dsrc|
# :ddoc:`Create Group Dm </resources/user#create-group-dm>`
# """

get_self_connections = Route('GET', '/users/@me/connections')
"""
|dsrc|
:ddoc:`Get User Connections </resources/user#get-user-connections>`
"""

get_self_application_role_connection = Route('GET', '/users/@me/applications/{0}/role-connection')
"""
|dsrc|
:ddoc:`Get User Application Role Connection </resources/user#get-user-application-role-connection>`
"""

update_self_application_role_connection = Route('PUT', '/users/@me/applications/{0}/role-connection')
"""
|dsrc|
:ddoc:`Update User Application Role Connection </resources/user#update-user-application-role-connection>`
"""

get_voice_regions = Route('GET', '/voice/regions')
"""
|dsrc|
:ddoc:`List Voice Regions </resources/voice#list-voice-regions>`
"""

create_webhook = Route('POST', '/channels/{0}/webhooks')
"""
|dsrc|
:ddoc:`Create Webhook </resources/webhook#create-webhook>`
"""

get_channel_webhooks = Route('GET', '/channels/{0}/webhooks')
"""
|dsrc|
:ddoc:`Get Channel Webhooks </resources/webhook#get-channel-webhooks>`
"""

get_guild_webhooks = Route('GET', '/guilds/{0}/webhooks')
"""
|dsrc|
:ddoc:`Get Guild Webhooks </resources/webhook#get-guild-webhooks>`
"""

get_webhook = Route('GET', '/webhooks/{0}')
"""
|dsrc|
:ddoc:`Get Webhook </resources/webhook#get-webhook>`
"""

get_webhook_via_token = Route('GET', '/webhooks/{0}/{1}')
"""
|dsrc|
:ddoc:`Get Webhook With Token </resources/webhook#get-webhook-with-token>`
"""

update_webhook = Route('PATCH', '/webhooks/{0}')
"""
|dsrc|
:ddoc:`Modify Webhook </resources/webhook#modify-webhook>`
"""

update_webhook_via_token = Route('PATCH', '/webhooks/{0}/{1}')
"""
|dsrc|
:ddoc:`Modify Webhook With Token </resources/webhook#modify-webhook-with-token>`
"""

delete_webhook = Route('DELETE', '/webhooks/{0}')
"""
|dsrc|
:ddoc:`Delete Webhook </resources/webhook#delete-webhook>`
"""

delete_webhook_via_token = Route('DELETE', '/webhooks/{0}/{1}')
"""
|dsrc|
:ddoc:`Delete Webhook With Token </resources/webhook#delete-webhook-with-token>`
"""

create_webhook_message = Route('POST', '/webhooks/{0}/{1}')
"""
|dsrc|
:ddoc:`Execute Webhook </resources/webhook#execute-webhook>`
"""

create_webhook_message_slack_compatible = Route('POST', '/webhooks/{0}/{1}/slack')
"""
|dsrc|
:ddoc:`Execute Slack Compatible Webhook </resources/webhook#execute-slack-compatible-webhook>`
"""

create_webhook_message_github_compatible = Route('POST', '/webhooks/{0}/{1}/github')
"""
|dsrc|
:ddoc:`Execute Github Compatible Webhook </resources/webhook#execute-github-compatible-webhook>`
"""

get_webhook_message = Route('GET', '/webhooks/{0}/{1}/messages/{2}')
"""
|dsrc|
:ddoc:`Get Webhook Message </resources/webhook#get-webhook-message>`
"""

update_webhook_message = Route('PATCH', '/webhooks/{0}/{1}/messages/{2}')
"""
|dsrc|
:ddoc:`Edit Webhook Message </resources/webhook#edit-webhook-message>`
"""

delete_webhook_message = Route('DELETE', '/webhooks/{0}/{1}/messages/{2}')
"""
|dsrc|
:ddoc:`Delete Webhook Message </resources/webhook#delete-webhook-message>`
"""

get_gateway = Route('GET', '/gateway')
"""
|dsrc|
:ddoc:`Get Gateway </topics/gateway#get-gateway>`
"""

get_gateway_bot = Route('GET', '/gateway/bot')
"""
|dsrc|
:ddoc:`Get Gateway Bot </topics/gateway#get-gateway-bot>`
"""

get_self_application_information = Route('GET', '/oauth2/applications/@me')
"""
|dsrc|
:ddoc:`Get Current Bot Application Information </topics/oauth2#get-current-bot-application-information>`
"""

get_self_authorization_information = Route('GET', '/oauth2/@me')
"""
|dsrc|
:ddoc:`Get Current Authorization Information </topics/oauth2#get-current-authorization-information>`
"""

get_skus = Route('GET', '/applications/{0}/skus')
"""
|dsrc|
:ddoc:`List SKUs </monetization/skus#list-skus>`
"""

get_entitlements = Route('GET', '/applications/{0}/entitlements')
"""
|dsrc|
:ddoc:`List Entitlements <//monetization/entitlements#create-test-entitlement>`
"""

create_entitlement = Route('POST', '/applications/{0}/entitlements')
"""
|dsrc|
:ddoc:`Create Test Entitlement </monetization/entitlements#create-test-entitlement>`
"""

delete_entitlement = Route('DELETE', '/applications/{0}/entitlements/{1}')
"""
|dsrc|
:ddoc:`Delete Test Entitlement </monetization/entitlements#delete-test-entitlement>`
"""