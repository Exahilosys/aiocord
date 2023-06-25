import typing
import yarl
import vessel

from . import types as _types


__all__ = (
    'emoji', 'guild_icon', 'guild_splash', 'guild_discovery_splash', 
    'guild_banner', 'user_banner', 'default_user_avatar', 'user_avatar', 
    'guild_member_avatar', 'application_icon', 'application_cover', 
    'application_asset', 'achievement_icon', 'store_page_asset', 
    'sticker_pack_banner', 'team_icon', 'sticker', 'role_icon', 
    'guild_scheduled_event_cover', 'guild_member_banner'
)


_base_uri = yarl.URL('https://cdn.discordapp.com')


def _make(template, parts, extension = '.png', size = None):

    if any(part is vessel.missing for part in parts):
        return vessel.missing
    
    path = template.format(*parts)

    query = {}

    if not size is None:
        query['size'] = size

    return _base_uri.with_path(path + extension).with_query(query)


class _make_hint(typing.TypedDict):

    extension: typing.Optional[_types.String]
    size     : typing.Optional[_types.Integer]


def emoji(emoji_id: _types.Snowflake, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/emojis/{0}'

    parts = [emoji_id]

    return _make(template, parts, **kwargs)


def guild_icon(guild_id: _types.Snowflake, guild_icon: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/icons/{0}/{1}'

    parts = [guild_id, guild_icon]

    return _make(template, parts, **kwargs)


def guild_splash(guild_id: _types.Snowflake, guild_splash: _types.String, /, **kwargs: typing.Unpack[_make_hint]):

    template = '/splashes/{0}/{1}'

    parts = [guild_id, guild_splash]

    return _make(template, parts, **kwargs)


def guild_discovery_splash(guild_id: _types.Snowflake, guild_discovery_splash: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/discovery-splashes/{0}/{1}'

    parts = [guild_id, guild_discovery_splash]
    
    return _make(template, parts, **kwargs)


def guild_banner(guild_id: _types.Snowflake, guild_banner: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/banners/{0}/{1}'

    parts = [guild_id, guild_banner]
    
    return _make(template, parts, **kwargs)


def user_banner(user_id: _types.Snowflake, user_banner: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/banners/{0}/{1}'

    parts = [user_id, user_banner]
    
    return _make(template, parts, **kwargs)


def default_user_avatar(user_discriminator: _types.Snowflake, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/embed/avatars/{0}'

    parts = [user_discriminator % 5]
    
    return _make(template, parts, **kwargs)


def user_avatar(user_id: _types.Snowflake, user_avatar: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/avatars/{0}/{1}'

    parts = [user_id, user_avatar]
    
    return _make(template, parts, **kwargs)


def guild_member_avatar(guild_id: _types.Snowflake, user_id: _types.Snowflake, guild_member_avatar: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/guilds/{0}/users/{1}/avatars/{2}'

    parts = [guild_id, user_id, guild_member_avatar]
    
    return _make(template, parts, **kwargs)


def application_icon(application_id: _types.Snowflake, icon: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/app-icons/{0}/{1}'

    parts = [application_id, icon]
    
    return _make(template, parts, **kwargs)


def application_cover(application_id: _types.Snowflake, cover_image: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/app-icons/{0}/{1}'

    parts = [application_id, cover_image]
    
    return _make(template, parts, **kwargs)


def application_asset(application_id: _types.Snowflake, asset_id: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/app-assets/{0}/{1}'

    parts = [application_id, asset_id]
    
    return _make(template, parts, **kwargs)


def achievement_icon(application_id: _types.Snowflake, achievement_id: _types.Snowflake, icon_hash: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/app-assets/{0}/achievements/{1}/icons/{2}'

    parts = [application_id, achievement_id, icon_hash]
    
    return _make(template, parts, **kwargs)


def store_page_asset(application_id: _types.Snowflake, asset_id: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    # NOTE: spec does not link "asset_id"
    template = '/app-assets/{0}/store/{1}'

    parts = [application_id, asset_id]

    return _make(template, parts, **kwargs)


def sticker_pack_banner(sticker_pack_banner_asset_id: _types.Snowflake, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/app-assets/710982414301790216/store/{0}'

    parts = [sticker_pack_banner_asset_id]
    
    return _make(template, parts, **kwargs)


def team_icon(team_id: _types.Snowflake, team_icon: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/team-icons/{0}/{1}'

    parts = [team_id, team_icon]
    
    return _make(template, parts, **kwargs)


def sticker(sticker_id: _types.Snowflake, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/stickers/{0}'

    parts = [sticker_id]
    
    return _make(template, parts, **kwargs)


def role_icon(role_id: _types.Snowflake, role_icon: _types.String, /, **kwargs: typing.Unpack[_make_hint]):
    
    template = '/role-icons/{0}/{1}'

    parts = [role_id, role_icon]
    
    return _make(template, parts, **kwargs)


def guild_scheduled_event_cover(scheduled_event_id: _types.Snowflake, scheduled_event_cover: _types.String, /, **kwargs: typing.Unpack[_make_hint]):

    template = '/guild-events/{0}/{1}'

    parts = [scheduled_event_id, scheduled_event_cover]

    return _make(template, parts, **kwargs)


def guild_member_banner(guild_id: _types.Snowflake, user_id: _types.Snowflake, member_banner: _types.String, /, **kwargs: typing.Unpack[_make_hint]):

    template = '/guilds/{0}/users/{1}/banners/{2}'

    parts = [guild_id, user_id, member_banner]

    return _make(template, parts, **kwargs)