
import typing
import vessel

from . import types     as _types
from . import enums     as _enums
from . import protocols as _protocols
from . import mentions  as _mentions
from . import images    as _images


__all__ = _protocols.__all__


_ApplicationCommand_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.ApplicationCommandType(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'name_localizations': vessel.SetField(
        create = lambda path, data: {
            _enums.Locale(data_key): _types.String(data_val) for data_key, data_val in data.items()
        }
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description_localizations': vessel.SetField(
        create = lambda path, data: {
            _enums.Locale(data_key): _types.String(data_val) for data_key, data_val in data.items()
        }
    ),
    'options': vessel.SetField(
        create = lambda path, data: _types.Collection(ApplicationCommandOption, data)
    ),
    'default_member_permissions': vessel.SetField(
        create = lambda path, data: _enums.Permissions(data)
    ),
    # 'dm_permission': vessel.SetField(
    #     create = lambda path, data: _types.Boolean(data)
    # ),
    'default_permission': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'nsfw': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'version': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'integration_types': vessel.SetField(
        create = lambda path, data: _types.Collection(_enums.ApplicationIntegrationType, data)
    ),
    'contexts': vessel.SetField(
        create = lambda path, data: _types.Collection(_enums.InteractionContextType, data)
    )
}


class ApplicationCommand(_types.Object[_protocols.ApplicationCommand], fields = _ApplicationCommand_fields):

    """
    |dsrc| :ddoc:`Application Command Structure </interactions/application-commands#application-command-object-application-command-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    type: _enums.ApplicationCommandType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['application_id']
    )
    """
    |dsrc| **application_id**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    name_localizations: dict[_enums.Locale, _types.String] = vessel.GetField(
        select = lambda root: root['name_localizations']
    )
    """
    |dsrc| **name_localizations**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    description_localizations: dict[_enums.Locale, _types.String] = vessel.GetField(
        select = lambda root: root['description_localizations']
    )
    """
    |dsrc| **description_localizations**
    """
    options: _types.Collection['ApplicationCommandOption'] = vessel.GetField(
        select = lambda root: root['options']
    )
    """
    |dsrc| **options**
    """
    default_member_permissions: _enums.Permissions = vessel.GetField(
        select = lambda root: root['default_member_permissions']
    )
    """
    |dsrc| **default_member_permissions**
    """
    dm_permission: _types.Boolean = vessel.GetField(
        select = lambda root: root['dm_permission']
    )
    """
    |dsrc| **dm_permission** (deprecated)
    """
    default_permission: _types.Boolean = vessel.GetField(
        select = lambda root: root['default_permission']
    )
    """
    |dsrc| **default_permission**
    """
    nsfw: _types.Boolean = vessel.GetField(
        select = lambda root: root['nsfw']
    )
    """
    |dsrc| **nsfw**
    """
    version: _types.Snowflake = vessel.GetField(
        select = lambda root: root['version']
    )
    """
    |dsrc| **version**
    """
    integration_types: _types.Collection[_enums.ApplicationIntegrationType] = vessel.GetField(
        select = lambda root: root['integration_types']
    )
    """
    |dsrc| **integration_types**
    """
    context_types: _types.Collection[_enums.InteractionContextType] = vessel.GetField(
        select = lambda root: root['contexts']
    )
    """
    |dsrc| **contexts**
    """

    def mention(self):

        """
        Get the mention.
        """

        return _mentions.command(self.name, self.id)


def _ApplicationCommandOption_fields_get_min_value_type(data):

    type = data['type']

    if type in {_enums.ApplicationCommandOptionType.integer}:
        return _types.Integer
    
    if type in {_enums.ApplicationCommandOptionType.number}:
        return _types.Decimal
    
    raise ValueError(f'unhandleable type: {type}')


def _ApplicationCommandOption_fields_get_max_value_type(data):

    type = data['type']

    if type in {_enums.ApplicationCommandOptionType.integer}:
        return _types.Integer
    
    if type in {_enums.ApplicationCommandOptionType.number}:
        return _types.Decimal
    
    raise ValueError(f'unhandleable type: {type}')


_ApplicationCommandOption_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.ApplicationCommandOptionType(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data),
        unique = True
    ),
    'name_localizations': vessel.SetField(
        create = lambda path, data: {
            _enums.Locale(data_key): _types.String(data_val) for data_key, data_val in data.items()
        }
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description_localizations': vessel.SetField(
        create = lambda path, data: {
            _enums.Locale(data_key): _types.String(data_val) for data_key, data_val in data.items()
        }
    ),
    'required': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'choices': vessel.SetField(
        create = lambda path, data: _types.Collection(ApplicationCommandOptionChoice, data)
    ),
    'options': vessel.SetField(
        create = lambda path, data: _types.Collection(ApplicationCommandOption, data)
    ),
    'channel_types': vessel.SetField(
        create = lambda path, data: _types.Collection(_enums.ChannelType, data)
    ),
    'min_value': vessel.SetField(
        create = lambda path, data: _ApplicationCommandOption_fields_get_min_value_type(data)(data)
    ),
    'max_value': vessel.SetField(
        create = lambda path, data: _ApplicationCommandOption_fields_get_max_value_type(data)(data)
    ),
    'min_length': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'max_length': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'autocomplete': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class ApplicationCommandOption(_types.Object[_protocols.ApplicationCommandOption], fields = _ApplicationCommandOption_fields):

    """
    |dsrc| :ddoc:`Application Command Option Structure </interactions/application-commands#application-command-object-application-command-option-structure>`
    """

    type: _enums.ApplicationCommandOptionType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    name_localizations: dict[_enums.Locale, _types.String] = vessel.GetField(
        select = lambda root: root['name_localizations']
    )
    """
    |dsrc| **name_localizations**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    description_localizations: dict[_enums.Locale, _types.String] = vessel.GetField(
        select = lambda root: root['description_localizations']
    )
    """
    |dsrc| **description_localizations**
    """
    required: _types.Boolean = vessel.GetField(
        select = lambda root: root['required']
    )
    """
    |dsrc| **required**
    """
    choices: _types.Collection['ApplicationCommandOptionChoice'] = vessel.GetField(
        select = lambda root: root['choices']
    )
    """
    |dsrc| **choices**
    """
    options: _types.Collection['ApplicationCommandOption'] = vessel.GetField(
        select = lambda root: root['options']
    )
    """
    |dsrc| **options**
    """
    channel_types: _types.Collection[_enums.ChannelType] = vessel.GetField(
        select = lambda root: root['channel_types']
    )
    """
    |dsrc| **channel_types**
    """
    min_value: typing.Union[_types.Integer, _types.Decimal] = vessel.GetField(
        select = lambda root: root['min_value']
    )
    """
    |dsrc| **min_value**
    """
    max_value: typing.Union[_types.Integer, _types.Decimal] = vessel.GetField(
        select = lambda root: root['max_value']
    )
    """
    |dsrc| **max_value**
    """
    min_length: _types.Integer = vessel.GetField(
        select = lambda root: root['min_length']
    )
    """
    |dsrc| **min_length**
    """
    max_length: _types.Integer = vessel.GetField(
        select = lambda root: root['max_length']
    )
    """
    |dsrc| **max_length**
    """
    autocomplete: _types.Boolean = vessel.GetField(
        select = lambda root: root['autocomplete']
    )
    """
    |dsrc| **autocomplete**
    """


def _ApplicationCommandOptionChoice_fields_get_value_type(data):

    type = data['type']
    
    if type in {_enums.ApplicationCommandOptionType.string}:
        return _types.String

    if type in {_enums.ApplicationCommandOptionType.integer}:
        return _types.Integer
    
    if type in {_enums.ApplicationCommandOptionType.number}:
        return _types.Decimal
    
    raise ValueError(f'unhandleable type: {type}')


_ApplicationCommandOptionChoice_fields = {
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'name_localizations': vessel.SetField(
        create = lambda path, data: {
            _enums.Locale(data_key): _types.String(data_val) for data_key, data_val in data.items()
        }
    ),
    'value': vessel.SetField(
        create = lambda path, data: _ApplicationCommandOptionChoice_fields_get_value_type(data)(data)
    )
}


class ApplicationCommandOptionChoice(_types.Object[_protocols.ApplicationCommandOptionChoice], fields = _ApplicationCommandOptionChoice_fields):

    """
    |dsrc| :ddoc:`Application Command Option Choice Structure </interactions/application-commands#application-command-object-application-command-option-choice-structure>`
    """

    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    name_localizations: dict[_enums.Locale, _types.String] = vessel.GetField(
        select = lambda root: root['name_localizations']
    )
    """
    |dsrc| **name_localizations**
    """
    value: typing.Union[_types.String, _types.Integer, _types.Decimal] = vessel.GetField(
        select = lambda root: root['value']
    )
    """
    |dsrc| **value**
    """


_GuildApplicationCommandPermissions_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'permissions': vessel.SetField(
        create = lambda path, data: _types.Collection(ApplicationCommandPermission, data)
    )
}


class GuildApplicationCommandPermissions(_types.Object[_protocols.GuildApplicationCommandPermissions], fields = _GuildApplicationCommandPermissions_fields):

    """
    DocumenGuild Application Command Permissions Structure </interactions/application-commands#application-command-permissions-object-guild-application-command-permissions-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['application_id']
    )
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    permissions: _types.Collection['ApplicationCommandPermission'] = vessel.GetField(
        select = lambda root: root['permissions']
    )


_ApplicationCommandPermission_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.ApplicationCommandPermissionType(data)
    ),
    'permission': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class ApplicationCommandPermission(_types.Object[_protocols.ApplicationCommandPermission], fields = _ApplicationCommandPermission_fields):

    """
    DocumenApplication Command Permissions Structure </interactions/application-commands#application-command-permissions-object-application-command-permissions-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    type: _enums.ApplicationCommandPermissionType = vessel.GetField(
        select = lambda root: root['type']
    )
    permission: _types.Boolean = vessel.GetField(
        select = lambda root: root['permission']
    )


def _MessageActionRowComponent_fields_get_components_subtype(data):

    type = data['type']
    
    if type in {_enums.MessageComponentType.button}:
        return MessageButtonComponent
    
    if type in {_enums.MessageComponentType.text_input}:
        return MessageTextInputComponent
    
    if type in {_enums.MessageComponentType.string_select, _enums.MessageComponentType.user_select, _enums.MessageComponentType.role_select, _enums.MessageComponentType.mentionable_select, _enums.MessageComponentType.channel_select}:
        return MessageSelectMenuComponent
    
    raise ValueError(f'unhandleable type: {type}')


_MessageActionRowComponent_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.MessageComponentType(data)
    ),
    'components': vessel.SetField(
        create = lambda path, data: _types.Collection(lambda data: _MessageActionRowComponent_fields_get_components_subtype(data)(data), data)
    )
}


class MessageActionRowComponent(_types.Object[_protocols.MessageActionRowComponent], fields = _MessageActionRowComponent_fields):

    """
    |dsrc| :ddoc:`Action Rows </interactions/message-components#action-rows>`
    """

    type: _enums.MessageComponentType = vessel.SetField(
        create = lambda root: root['type']
    )
    components: _types.Collection[typing.Union['MessageButtonComponent', 'MessageSelectMenuComponent', 'MessageTextInputComponent']] = vessel.GetField(
        select = lambda root: root['components']
    )
    """
    |dsrc| **components**
    """


_MessageButtonComponent_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.MessageComponentType(data)
    ),
    'style': vessel.SetField(
        create = lambda path, data: _enums.MessageButtonComponentStyle(data)
    ),
    'label': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'emoji': vessel.SetField(
        create = lambda path, data: Emoji(data)
    ),
    'custom_id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'disabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class MessageButtonComponent(_types.Object[_protocols.MessageButtonComponent], fields = _MessageButtonComponent_fields):

    """
    |dsrc| :ddoc:`Button Structure </interactions/message-components#button-object-button-structure>`
    """

    type: _types.Integer = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    style: _types.Integer = vessel.GetField(
        select = lambda root: root['style']
    )
    """
    |dsrc| **style**
    """
    label: _types.String = vessel.GetField(
        select = lambda root: root['label']
    )
    """
    |dsrc| **label**
    """
    emoji: 'Emoji' = vessel.GetField(
        select = lambda root: root['emoji']
    )
    """
    |dsrc| **emoji**
    """
    custom_id: _types.String = vessel.GetField(
        select = lambda root: root['custom_id']
    )
    """
    |dsrc| **custom_id**
    """
    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """
    disabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['disabled']
    )
    """
    |dsrc| **disabled**
    """


_MessageSelectMenuComponent_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.MessageComponentType(data)
    ),
    'custom_id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'options': vessel.SetField(
        create = lambda path, data: _types.Collection(MessageSelectMenuComponentOption, data)
    ),
    'channel_types': vessel.SetField(
        create = lambda path, data: _types.Collection(_enums.ChannelType, data)
    ),
    'placeholder': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'default_values': vessel.SetField(
        create = lambda path, data: _types.Collection(MessageSelectMenuComponentDefaultValue, data)
    ),
    'min_values': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'max_values': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'disabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class MessageSelectMenuComponent(_types.Object[_protocols.MessageSelectMenuComponent], fields = _MessageSelectMenuComponent_fields):

    """
    |dsrc| :ddoc:`Select Menu Structure </interactions/message-components#select-menu-object-select-menu-structure>`
    """

    type: _enums.MessageComponentType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    custom_id: _types.String = vessel.GetField(
        select = lambda root: root['custom_id']
    )
    """
    |dsrc| **custom_id**
    """
    options: _types.Collection['MessageSelectMenuComponentOption'] = vessel.GetField(
        select = lambda root: root['options']
    )
    """
    |dsrc| **options**
    """
    channel_types: _types.Collection[_enums.ChannelType] = vessel.GetField(
        select = lambda root: root['channel_types']
    )
    """
    |dsrc| **channel_types**
    """
    placeholder: _types.String = vessel.GetField(
        select = lambda root: root['placeholder']
    )
    """
    |dsrc| **placeholder**
    """
    default_values: _types.Collection['MessageSelectMenuComponentDefaultValue'] = vessel.GetField(
        select = lambda root: root['default_values']
    )
    """
    |dsrc| **default_values**
    """
    min_values: _types.Integer = vessel.GetField(
        select = lambda root: root['min_values']
    )
    """
    |dsrc| **min_values**
    """
    max_values: _types.Integer = vessel.GetField(
        select = lambda root: root['max_values']
    )
    """
    |dsrc| **max_values**
    """
    disabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['disabled']
    )
    """
    |dsrc| **disabled**
    """


_MessageSelectMenuComponentOption_fields = {
    'label': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'value': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'emoji': vessel.SetField(
        create = lambda path, data: Emoji(data)
    ),
    'default': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class MessageSelectMenuComponentOption(_types.Object[_protocols.MessageSelectMenuComponentOption], fields = _MessageSelectMenuComponentOption_fields):

    """
    |dsrc| :ddoc:`Select Option Structure </interactions/message-components#select-menu-object-select-option-structure>`
    """

    label: _types.String = vessel.GetField(
        select = lambda root: root['label']
    )
    """
    |dsrc| **label**
    """
    value: _types.String = vessel.GetField(
        select = lambda root: root['value']
    )
    """
    |dsrc| **value**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    emoji: 'Emoji' = vessel.GetField(
        select = lambda root: root['emoji']
    )
    """
    |dsrc| **emoji**
    """
    default: _types.Boolean = vessel.GetField(
        select = lambda root: root['default']
    )
    """
    |dsrc| **default**
    """

_MessageSelectMenuComponentDefaultValue_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.MessageSelectMenuComponentDefaultValueType(data)
    )
}

class MessageSelectMenuComponentDefaultValue(_types.Object[_protocols.MessageSelectMenuComponentDefaultValue], fields = _MessageSelectMenuComponentDefaultValue_fields):

    """
    |dsrc| :ddoc:`Select Default Value Structure </interactions/message-components#select-menu-object-select-default-value-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    type: _enums.MessageSelectMenuComponentDefaultValueType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """

_MessageTextInputComponent_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.MessageComponentType(data)
    ),
    'custom_id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'style': vessel.SetField(
        create = lambda path, data: _enums.MessageTextInputComponentStyle(data)
    ),
    'label': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'min_length': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'max_length': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'required': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'value': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'placeholder': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class MessageTextInputComponent(_types.Object[_protocols.MessageTextInputComponent], fields = _MessageTextInputComponent_fields):

    """
    |dsrc| :ddoc:`Text Inputs Text Input Structure </interactions/message-components#text-inputs-text-input-structure>`
    """

    type: _types.Integer = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    custom_id: _types.String = vessel.GetField(
        select = lambda root: root['custom_id']
    )
    """
    |dsrc| **custom_id**
    """
    style: _enums.MessageTextInputComponentStyle = vessel.GetField(
        select = lambda root: root['style']
    )
    """
    |dsrc| **style**
    """
    label: _types.String = vessel.GetField(
        select = lambda root: root['label']
    )
    """
    |dsrc| **label**
    """
    min_length: _types.Integer = vessel.GetField(
        select = lambda root: root['min_length']
    )
    """
    |dsrc| **min_length**
    """
    max_length: _types.Integer = vessel.GetField(
        select = lambda root: root['max_length']
    )
    """
    |dsrc| **max_length**
    """
    required: _types.Boolean = vessel.GetField(
        select = lambda root: root['required']
    )
    """
    |dsrc| **required**
    """
    value: _types.String = vessel.GetField(
        select = lambda root: root['value']
    )
    """
    |dsrc| **value**
    """
    placeholder: _types.String = vessel.GetField(
        select = lambda root: root['placeholder']
    )
    """
    |dsrc| **placeholder**
    """


def _Interaction_fields_get_data_type(type):

    if type in {_enums.InteractionType.application_command, _enums.InteractionType.application_command_autocomplete}:
        return ApplicationCommandInteractionData
    
    if type in {_enums.InteractionType.message_component}:
        return MessageComponentInteractionData
    
    if type in {_enums.InteractionType.modal_submit}:
        return ModalSubmitInteractionData
    
    raise ValueError(f'unhandleable type: {type}')


_Interaction_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.InteractionType(data)
    ),
    'data': vessel.SetField(
        create = lambda path, data: _Interaction_fields_get_data_type(path[-1]['type'])(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'channel': vessel.SetField(
        create = lambda path, data: Channel(data)
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'member': vessel.SetField(
        create = lambda path, data: GuildMember(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'token': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'version': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'message': vessel.SetField(
        create = lambda path, data: Message(data)
    ),
    'app_permissions': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'locale': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'guild_locale': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'entitlements': vessel.SetField(
        create = lambda path, data: _types.Collection(Entitlement, data)
    ),
    'authorizing_integration_owners': vessel.SetField(
        create = lambda path, data: dict(
            map(
                lambda item: (
                    _enums.ApplicationIntegrationType(item[0]),
                    _types.Snowflake(item[1])
                ),
                data.items()
            )
        )
    ),
    'context': vessel.SetField(
        create = lambda path, data: _enums.InteractionContextType(data)
    )
}


class Interaction(_types.Object[_protocols.Interaction], fields = _Interaction_fields):

    """
    |dsrc| :ddoc:`Interaction Structure </interactions/receiving-and-responding#interaction-object-interaction-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['application_id']
    )
    """
    |dsrc| **application_id**
    """
    type: _enums.InteractionType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    data: typing.Union['ApplicationCommandInteractionData', 'MessageComponentInteractionData', 'ModalSubmitInteractionData', 'ResolvedInteractionData'] = vessel.GetField(
        select = lambda root: root['data']
    )
    """
    |dsrc| **data**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    channel: 'Channel' = vessel.GetField(
        select = lambda root: root['channel']
    )
    """
    |dsrc| **channel**
    """
    channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    member: 'GuildMember' = vessel.GetField(
        select = lambda root: root['member']
    )
    """
    |dsrc| **member**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    token: _types.String = vessel.GetField(
        select = lambda root: root['token']
    )
    """
    |dsrc| **token**
    """
    version: _types.Integer = vessel.GetField(
        select = lambda root: root['version']
    )
    """
    |dsrc| **version**
    """
    message: 'Message' = vessel.GetField(
        select = lambda root: root['message']
    )
    """
    |dsrc| **message**
    """
    app_permissions: _types.String = vessel.GetField(
        select = lambda root: root['app_permissions']
    )
    """
    |dsrc| **app_permissions**
    """
    locale: _types.String = vessel.GetField(
        select = lambda root: root['locale']
    )
    """
    |dsrc| **locale**
    """
    guild_locale: _types.String = vessel.GetField(
        select = lambda root: root['guild_locale']
    )
    """
    |dsrc| **guild_locale**
    """
    entitlements: _types.Collection['Entitlement'] = vessel.GetField(
        select = lambda root: root['entitlements']
    )
    """
    |dsrc| **entitlements**
    """
    authorizing_integration_owners: dict[_enums.ApplicationIntegrationType, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['authorizing_integration_owners']
    )
    """
    |dsrc| **authorizing_integration_owners**
    """
    context: _enums.InteractionContextType = vessel.GetField(
        select = lambda root: root['context']
    )
    """
    |dsrc| **context**
    """


_ApplicationCommandInteractionData_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.ApplicationCommandType(data)
    ),
    'resolved': vessel.SetField(
        create = lambda path, data: ResolvedInteractionData(data)
    ),
    'options': vessel.SetField(
        create = lambda path, data: _types.Collection(ApplicationCommandInteractionDataOption, data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'target_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    )
}


def _ApplicationCommandInteractionData_keyify(path, data):

    data_id = data['id']
    core_id: _types.Snowflake(data_id)

    return core_id


class ApplicationCommandInteractionData(_types.Object[_protocols.ApplicationCommandInteractionData], fields = _ApplicationCommandInteractionData_fields, keyify = _ApplicationCommandInteractionData_keyify):

    """
    |dsrc| :ddoc:`Application Command Data Structure </interactions/receiving-and-responding#interaction-object-application-command-data-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    type: _types.Integer = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    resolved: 'ResolvedInteractionData' = vessel.GetField(
        select = lambda root: root['resolved']
    )
    """
    |dsrc| **resolved**
    """
    options: _types.Collection['ApplicationCommandInteractionDataOption'] = vessel.GetField(
        select = lambda root: root['options']
    )
    """
    |dsrc| **options**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    target_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['target_id']
    )
    """
    |dsrc| **target_id**
    """


_ApplicationCommandInteractionDataOption_fields = {
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.ApplicationCommandOptionType(data)
    ),
    'value': vessel.SetField(
        create = lambda path, data: data
    ),
    'options': vessel.SetField(
        create = lambda path, data: _types.Collection(ApplicationCommandInteractionDataOption, data)
    ),
    'focused': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class ApplicationCommandInteractionDataOption(_types.Object[_protocols.ApplicationCommandInteractionDataOption], fields = _ApplicationCommandInteractionDataOption_fields):

    """
    |dsrc| :ddoc:`Application Command Interaction Data Option Structure </interactions/receiving-and-responding#interaction-object-application-command-interaction-data-option-structure>`
    """

    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    type: _types.Integer = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    value: typing.Union[_types.String, _types.Integer, _types.Decimal, _types.Boolean] = vessel.GetField(
        select = lambda root: root['value']
    )
    """
    |dsrc| **value**
    """
    options: _types.Collection['ApplicationCommandInteractionDataOption'] = vessel.GetField(
        select = lambda root: root['options']
    )
    """
    |dsrc| **options**
    """
    focused: _types.Boolean = vessel.GetField(
        select = lambda root: root['focused']
    )
    """
    |dsrc| **focused**
    """


_MessageComponentInteractionData_fields = {
    'custom_id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'component_type': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'values': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    )
}


class MessageComponentInteractionData(_types.Object[_protocols.MessageComponentInteractionData], fields = _MessageComponentInteractionData_fields):

    """
    |dsrc| :ddoc:`Message Component Data Structure </interactions/receiving-and-responding#interaction-object-message-component-data-structure>`
    """

    custom_id: _types.String = vessel.GetField(
        select = lambda root: root['custom_id']
    )
    """
    |dsrc| **custom_id**
    """
    component_type: _types.Integer = vessel.GetField(
        select = lambda root: root['component_type']
    )
    """
    |dsrc| **component_type**
    """
    values: _types.Collection['MessageSelectMenuComponent'] = vessel.GetField(
        select = lambda root: root['values']
    )
    """
    |dsrc| **values**
    """


def _ModalSubmitInteractionData_fields_get_components_subtype(data):

    type = data['type']

    if type in {_enums.MessageComponentType.action_row}:
        return MessageActionRowComponent
    
    if type in {_enums.MessageComponentType.button}:
        return MessageButtonComponent
    
    if type in {_enums.MessageComponentType.text_input}:
        return MessageTextInputComponent
    
    if type in {_enums.MessageComponentType.string_select, _enums.MessageComponentType.user_select, _enums.MessageComponentType.role_select, _enums.MessageComponentType.mentionable_select, _enums.MessageComponentType.channel_select}:
        return MessageSelectMenuComponent
    
    raise ValueError(f'unhandleable type: {type}')


_ModalSubmitInteractionData_fields = {
    'custom_id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'components': vessel.SetField(
        create = lambda path, data: _types.Collection(lambda data: _ModalSubmitInteractionData_fields_get_components_subtype(data)(data), data)
    )
}


class ModalSubmitInteractionData(_types.Object[_protocols.ModalSubmitInteractionData], fields = _ModalSubmitInteractionData_fields):

    """
    |dsrc| :ddoc:`Modal Submit Data Structure </interactions/receiving-and-responding#interaction-object-modal-submit-data-structure>`
    """

    custom_id: _types.String = vessel.GetField(
        select = lambda root: root['custom_id']
    )
    """
    |dsrc| **custom_id**
    """
    components: _types.Collection[typing.Union['MessageActionRowComponent', 'MessageButtonComponent', 'MessageSelectMenuComponent', 'MessageTextInputComponent']] = vessel.GetField(
        select = lambda root: root['components']
    )
    """
    |dsrc| **components**
    """


def _ResolvedInteractionData_fields_fix_members(path, members):

    users = path[-1]['users']

    for user_id, member in members.items():
        member['user'] = vessel.strip(users[user_id])

    return members.values()


_ResolvedInteractionData_fields = {
    'users': vessel.SetField(
        create = lambda path, data: _types.Collection(User, data.values())
    ),
    'members': vessel.SetField(
        create = lambda path, data: _types.Collection(
            GuildMember,
            _ResolvedInteractionData_fields_fix_members(path, data)
        )
    ),
    'channels': vessel.SetField(
        create = lambda path, data: _types.Collection(Channel, data.values())
    ),
    'messages': vessel.SetField(
        create = lambda path, data: _types.Collection(Message, data.values())
    ),
    'attachments': vessel.SetField(
        create = lambda path, data: _types.Collection(Attachment, data.values())
    )
}


class ResolvedInteractionData(_types.Object[_protocols.ResolvedInteractionData], fields = _ResolvedInteractionData_fields):

    """
    |dsrc| :ddoc:`Resolved Data Structure </interactions/receiving-and-responding#interaction-object-resolved-data-structure>`
    """

    users: _types.Collection['User'] = vessel.GetField(
        select = lambda root: root['users']
    )
    """
    |dsrc| **users**
    """
    guild_members: _types.Collection['GuildMember'] = vessel.GetField(
        select = lambda root: root['members']
    )
    """
    |dsrc| **guild_members**
    """
    channels: _types.Collection['Channel'] = vessel.GetField(
        select = lambda root: root['channels']
    )
    """
    |dsrc| **channels**
    """
    messages: _types.Collection['Message'] = vessel.GetField(
        select = lambda root: root['messages']
    )
    """
    |dsrc| **messages**
    """
    attachments: _types.Collection['Attachment'] = vessel.GetField(
        select = lambda root: root['attachments']
    )
    """
    |dsrc| **attachments**
    """


_MessageInteraction_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.InteractionType(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'member': vessel.SetField(
        create = lambda path, data: GuildMember(data)
    )
}


class MessageInteraction(_types.Object[_protocols.MessageInteraction], fields = _MessageInteraction_fields):

    """
    |dsrc| :ddoc:`Message Interaction Structure </interactions/receiving-and-responding#message-interaction-object-message-interaction-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    type: _enums.InteractionType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    guild_member: 'GuildMember' = vessel.GetField(
        select = lambda root: root['member']
    )
    """
    |dsrc| **guild_member**
    """


_InteractionResponse_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.InteractionResponseType(data)
    ),
    'data': vessel.SetField(
        # NOTE: missing type matching specification
        # https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-data-structure
        create = lambda path, data: data
    )
}


class InteractionResponse(_types.Object[_protocols.InteractionResponse], fields = _InteractionResponse_fields):

    """
    |dsrc| :ddoc:`Interaction Response Structure </interactions/receiving-and-responding#interaction-response-object-interaction-response-structure>`
    """

    type: _enums.InteractionResponseType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    # data: 'InteractionResponseData' = vessel.GetField(
    #     select = lambda root: root['data']
    # )
    # """
    # |dsrc| **data**
    # """
    data: typing.Any = vessel.GetField(
        select = lambda root: root['data']
    )
    """
    |dsrc| **data**
    """


_Application_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'icon': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'rpc_origins': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    ),
    'bot_public': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'bot_require_code_grant': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'terms_of_service_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'privacy_policy_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'owner': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'verify_key': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'team': vessel.SetField(
        create = lambda path, data: Team(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'primary_sku_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'slug': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'cover_image': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'flags': vessel.SetField(
        create = lambda path, data: _enums.ApplicationFlags(data)
    ),
    'tags': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    ),
    'install_params': vessel.SetField(
        create = lambda path, data: ApplicationInstallParams(data)
    ),
    'custom_install_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'role_connections_verification_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'integration_types_config': vessel.SetField(
        create  = lambda path, data: dict(
            map(
                lambda item: (
                    _enums.ApplicationIntegrationType(item[0]),
                    ApplicationIntegrationTypeConfiguration(item[1])
                ),
                data.items()
            )
        )
    )
}


def _Application_identify(path, data):

    data_id = data['id']
    core_id: _types.Snowflake(data_id)

    return core_id


class Application(_types.Object[_protocols.Application], fields = _Application_fields):

    """
    |dsrc| :ddoc:`Application Structure </resources/application#application-object-application-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    icon: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['icon']
    )
    """
    |dsrc| **icon**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    rpc_origins: _types.Collection[_types.String] = vessel.GetField(
        select = lambda root: root['rpc_origins']
    )
    """
    |dsrc| **rpc_origins**
    """
    bot_public: _types.Boolean = vessel.GetField(
        select = lambda root: root['bot_public']
    )
    """
    |dsrc| **bot_public**
    """
    bot_require_code_grant: _types.Boolean = vessel.GetField(
        select = lambda root: root['bot_require_code_grant']
    )
    """
    |dsrc| **bot_require_code_grant**
    """
    terms_of_service_url: _types.String = vessel.GetField(
        select = lambda root: root['terms_of_service_url']
    )
    """
    |dsrc| **terms_of_service_url**
    """
    privacy_policy_url: _types.String = vessel.GetField(
        select = lambda root: root['privacy_policy_url']
    )
    """
    |dsrc| **privacy_policy_url**
    """
    owner: 'User' = vessel.GetField(
        select = lambda root: root['owner']
    )
    """
    |dsrc| **owner**
    """
    verify_key: _types.String = vessel.GetField(
        select = lambda root: root['verify_key']
    )
    """
    |dsrc| **verify_key**
    """
    team: typing.Union[None, 'Team'] = vessel.GetField(
        select = lambda root: root['team']
    )
    """
    |dsrc| **team**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    primary_sku_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['primary_sku_id']
    )
    """
    |dsrc| **primary_sku_id**
    """
    slug: _types.String = vessel.GetField(
        select = lambda root: root['slug']
    )
    """
    |dsrc| **slug**
    """
    cover: _types.String = vessel.GetField(
        select = lambda root: root['cover_image']
    )
    """
    |dsrc| **cover_image**
    """
    flags: _types.Integer = vessel.GetField(
        select = lambda root: root['flags']
    )
    """
    |dsrc| **flags**
    """
    tags: _types.Collection[_types.String] = vessel.GetField(
        select = lambda root: root['tags']
    )
    """
    |dsrc| **tags**
    """
    install_params: 'ApplicationInstallParams' = vessel.GetField(
        select = lambda root: root['install_params']
    )
    """
    |dsrc| **install_params**
    """
    custom_install_url: _types.String = vessel.GetField(
        select = lambda root: root['custom_install_url']
    )
    """
    |dsrc| **custom_install_url**
    """
    role_connections_verification_url: _types.String = vessel.GetField(
        select = lambda root: root['role_connections_verification_url']
    )
    """
    |dsrc| **role_connections_verification_url**
    """
    integration_type_configs: dict[_enums.ApplicationIntegrationType, 'ApplicationIntegrationTypeConfiguration'] = vessel.GetField(
        select = lambda root: root['role_connections_verification_url']
    )
    """
    |dsrc| **integration_types_config**
    """

    def icon_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the icon url.
        """

        return _images.application_icon(self.id, self.icon, **kwargs)

    def cover_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the cover url.
        """

        return _images.application_cover(self.id, self.cover, **kwargs)

    def asset_url(self, asset_id: _types.Snowflake, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the asset url.
        """

        return _images.application_asset(self.id, asset_id, **kwargs)


_ApplicationIntegrationTypeConfiguration_fields = {
    'oauth2_install_params': vessel.SetField(
        create = lambda path, data: ApplicationInstallParams(data)
    )
}


class ApplicationIntegrationTypeConfiguration(_types.Object[_protocols.ApplicationIntegrationTypeConfiguration], fields = _ApplicationIntegrationTypeConfiguration_fields):

    """
    |dsrc| :ddoc:`Application Integration Type Configuration Object </resources/application#application-object-application-integration-type-configuration-object>`
    """

    oauth2_install_params: 'ApplicationInstallParams' = vessel.GetField(
        select = lambda root: root['oauth2_install_params']
    )
    """
    |dsrc| **oauth2_install_params**
    """


_ApplicationInstallParams_fields = {
    'scopes': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    ),
    'permissions': vessel.SetField(
        create = lambda path, data: _enums.Permissions(data)
    )
}


class ApplicationInstallParams(_types.Object[_protocols.ApplicationInstallParams], fields = _ApplicationInstallParams_fields):

    """
    |dsrc| :ddoc:`Install Params Structure </resources/application#install-params-object-install-params-structure>`
    """

    scopes: _types.Collection[_types.String] = vessel.GetField(
        select = lambda root: root['scopes']
    )
    """
    |dsrc| **scopes**
    """
    permissions: _enums.Permissions = vessel.GetField(
        select = lambda root: root['permissions']
    )
    """
    |dsrc| **permissions**
    """


_ApplicationRoleConnectionMetadata_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.ApplicationRoleConnectionMetadataType(data)
    ),
    'key': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'name_localizations': vessel.SetField(
        create = lambda path, data: {
            _enums.Locale(data_key): _types.String(data_val) for data_key, data_val in data.items()
        }
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description_localizations': vessel.SetField(
        create = lambda path, data: {
            _enums.Locale(data_key): _types.String(data_val) for data_key, data_val in data.items()
        }
    )
}


class ApplicationRoleConnectionMetadata(_types.Object[_protocols.ApplicationRoleConnectionMetadata], fields = _ApplicationRoleConnectionMetadata_fields):

    """
    |dsrc| :ddoc:`Application Role Connection Metadata Structure </resources/application-role-connection-metadata#application-role-connection-metadata-object-application-role-connection-metadata-structure>`
    """

    type: _enums.ApplicationRoleConnectionMetadataType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    key: _types.String = vessel.GetField(
        select = lambda root: root['key']
    )
    """
    |dsrc| **key**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    name_localizations: dict[_enums.Locale, _types.String] = vessel.GetField(
        select = lambda root: root['name_localizations']
    )
    """
    |dsrc| **name_localizations**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    description_localizations: dict[_enums.Locale, _types.String] = vessel.GetField(
        select = lambda root: root['description_localizations']
    )
    """
    |dsrc| **description_localizations**
    """


_AuditLog_fields = {
    'application_commands': vessel.SetField(
        create = lambda path, data: _types.Collection(ApplicationCommand, data)
    ),
    'audit_log_entries': vessel.SetField(
        create = lambda path, data: _types.Collection(AuditLogEntry, data)
    ),
    'auto_moderation_rules': vessel.SetField(
        create = lambda path, data: _types.Collection(AutoModerationRule, data)
    ),
    'guild_scheduled_events': vessel.SetField(
        create = lambda path, data: _types.Collection(GuildScheduledEvent, data)
    ),
    'integrations': vessel.SetField(
        create = lambda path, data: _types.Collection(Integration, data)
    ),
    'threads': vessel.SetField(
        create = lambda path, data: _types.Collection(Channel, data)
    ),
    'users': vessel.SetField(
        create = lambda path, data: _types.Collection(User, data)
    ),
    'webhooks': vessel.SetField(
        create = lambda path, data: _types.Collection(Webhook, data)
    )
}


class AuditLog(_types.Object[_protocols.AuditLog], fields = _AuditLog_fields):

    """
    |dsrc| :ddoc:`Audit Log Structure </resources/audit-log#audit-log-object-audit-log-structure>`
    """

    application_commands: _types.Collection['ApplicationCommand'] = vessel.GetField(
        select = lambda root: root['application_commands']
    )
    """
    |dsrc| **application_commands**
    """
    audit_log_entries: _types.Collection['AuditLogEntry'] = vessel.GetField(
        select = lambda root: root['audit_log_entries']
    )
    """
    |dsrc| **audit_log_entries**
    """
    auto_moderation_rules: _types.Collection['AutoModerationRule'] = vessel.GetField(
        select = lambda root: root['auto_moderation_rules']
    )
    """
    |dsrc| **auto_moderation_rules**
    """
    guild_scheduled_events: _types.Collection['GuildScheduledEvent'] = vessel.GetField(
        select = lambda root: root['guild_scheduled_events']
    )
    """
    |dsrc| **guild_scheduled_events**
    """
    integrations: _types.Collection['Integration'] = vessel.GetField(
        select = lambda root: root['integrations']
    )
    """
    |dsrc| **integrations**
    """
    threads: _types.Collection['Channel'] = vessel.GetField(
        select = lambda root: root['threads']
    )
    """
    |dsrc| **threads**
    """
    users: _types.Collection['User'] = vessel.GetField(
        select = lambda root: root['users']
    )
    """
    |dsrc| **users**
    """
    webhooks: _types.Collection['Webhook'] = vessel.GetField(
        select = lambda root: root['webhooks']
    )
    """
    |dsrc| **webhooks**
    """


_AuditLogEntry_fields = {
    'target_id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'changes': vessel.SetField(
        create = lambda path, data: _types.Collection(AuditLogChange, data)
    ),
    'user_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'action_type': vessel.SetField(
        create = lambda path, data: _enums.AuditLogEvent(data)
    ),
    'options': vessel.SetField(
        create = lambda path, data: OptionalAuditLogEntryInfo(data)
    ),
    'reason': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class AuditLogEntry(_types.Object[_protocols.AuditLogEntry], fields = _AuditLogEntry_fields):

    """
    |dsrc| :ddoc:`Audit Log Entry Structure </resources/audit-log#audit-log-entry-object-audit-log-entry-structure>`
    """

    target_id: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['target_id']
    )
    """
    |dsrc| **target_id**
    """
    changes: _types.Collection['AuditLogChange'] = vessel.GetField(
        select = lambda root: root['changes']
    )
    """
    |dsrc| **changes**
    """
    user_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['user_id']
    )
    """
    |dsrc| **user_id**
    """
    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    action_type: _enums.AuditLogEvent = vessel.GetField(
        select = lambda root: root['action_type']
    )
    """
    |dsrc| **action_type**
    """
    options: 'OptionalAuditLogEntryInfo' = vessel.GetField(
        select = lambda root: root['options']
    )
    """
    |dsrc| **options**
    """
    reason: _types.String = vessel.GetField(
        select = lambda root: root['reason']
    )
    """
    |dsrc| **reason**
    """
    

_OptionalAuditLogEntryInfo_fields = {
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'auto_moderation_rule_name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'auto_moderation_rule_trigger_type': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'count': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'delete_member_days': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'members_removed': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'message_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'role_name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.OptionalAuditLogEntryInfoOverwrittenEntityType(data)
    )
}


class OptionalAuditLogEntryInfo(_types.Object[_protocols.OptionalAuditLogEntryInfo], fields = _OptionalAuditLogEntryInfo_fields):

    """
    |dsrc| :ddoc:`Optional Audit Entry Info </resources/audit-log#audit-log-entry-object-optional-audit-entry-info>`
    """

    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['application_id']
    )
    """
    |dsrc| **application_id**
    """
    auto_moderation_rule_name: _types.String = vessel.GetField(
        select = lambda root: root['auto_moderation_rule_name']
    )
    """
    |dsrc| **auto_moderation_rule_name**
    """
    auto_moderation_rule_trigger_type: _types.String = vessel.GetField(
        select = lambda root: root['auto_moderation_rule_trigger_type']
    )
    """
    |dsrc| **auto_moderation_rule_trigger_type**
    """
    channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    count: _types.String = vessel.GetField(
        select = lambda root: root['count']
    )
    """
    |dsrc| **count**
    """
    delete_member_days: _types.String = vessel.GetField(
        select = lambda root: root['delete_member_days']
    )
    """
    |dsrc| **delete_member_days**
    """
    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    members_removed: _types.String = vessel.GetField(
        select = lambda root: root['members_removed']
    )
    """
    |dsrc| **members_removed**
    """
    message_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['message_id']
    )
    """
    |dsrc| **message_id**
    """
    role_name: _types.String = vessel.GetField(
        select = lambda root: root['role_name']
    )
    """
    |dsrc| **role_name**
    """
    type: _enums.OptionalAuditLogEntryInfoOverwrittenEntityType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """


def _AuditLogChange_fields_get_new_value_type(data):

    return lambda data: data


def _AuditLogChange_fields_get_old_value_type(data):

    return lambda data: data


_AuditLogChange_fields = {
    # TODO: implicit type matching specification
    # https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-optional-audit-entry-info
    'new_value': vessel.SetField(
        create = lambda path, data: _AuditLogChange_fields_get_new_value_type(data)(data)
    ),
    'old_value': vessel.SetField(
        create = lambda path, data: _AuditLogChange_fields_get_old_value_type(data)(data)
    ),
    'key': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class AuditLogChange(_types.Object[_protocols.AuditLogChange], fields = _AuditLogChange_fields):

    """
    |dsrc| :ddoc:`Audit Log Change Structure </resources/audit-log#audit-log-change-object-audit-log-change-structure>`
    """

    new_value: typing.Any = vessel.GetField(
        select = lambda root: root['new_value']
    )
    """
    |dsrc| **new_value**
    """
    old_value: typing.Any = vessel.GetField(
        select = lambda root: root['old_value']
    )
    """
    |dsrc| **old_value**
    """
    key: _types.String = vessel.GetField(
        select = lambda root: root['key']
    )
    """
    |dsrc| **key**
    """


_AutoModerationRule_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'creator_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'event_type': vessel.SetField(
        create = lambda path, data: _enums.AutoModerationRuleEventType(data)
    ),
    'trigger_type': vessel.SetField(
        create = lambda path, data: _enums.AutoModerationTriggerType(data)
    ),
    'trigger_metadata': vessel.SetField(
        create = lambda path, data: AutoModerationTriggerMetadata(data)
    ),
    'actions': vessel.SetField(
        create = lambda path, data: _types.Collection(AutoModerationAction, data)
    ),
    'enabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'exempt_roles': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'exempt_channels': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    )
}


def _AutoModerationRule_identify(path, data):

    data_id = data['id']
    core_id: _types.Snowflake(data_id)

    return core_id


class AutoModerationRule(_types.Object[_protocols.AutoModerationRule], fields = _AutoModerationRule_fields):

    """
    |dsrc| :ddoc:`Trigger Metadata </resources/auto-moderation#auto-moderation-rule-object-trigger-metadata>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    creator_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['creator_id']
    )
    """
    |dsrc| **creator_id**
    """
    event_type: _enums.AutoModerationRuleEventType = vessel.GetField(
        select = lambda root: root['event_type']
    )
    """
    |dsrc| **event_type**
    """
    trigger_type: _enums.AutoModerationTriggerType = vessel.GetField(
        select = lambda root: root['trigger_type']
    )
    """
    |dsrc| **trigger_type**
    """
    trigger_metadata: 'AutoModerationTriggerMetadata' = vessel.GetField(
        select = lambda root: root['trigger_metadata']
    )
    """
    |dsrc| **trigger_metadata**
    """
    actions: _types.Collection['AutoModerationAction'] = vessel.GetField(
        select = lambda root: root['actions']
    )
    """
    |dsrc| **actions**
    """
    enabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['enabled']
    )
    """
    |dsrc| **enabled**
    """
    exempt_roles: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['exempt_roles']
    )
    """
    |dsrc| **exempt_roles**
    """
    exempt_channels: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['exempt_channels']
    )
    """
    |dsrc| **exempt_channels**
    """


_AutoModerationTriggerMetadata_fields = {
    'keyword_filter': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    ),
    'regex_patterns': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    ),
    'presets': vessel.SetField(
        create = lambda path, data: _types.Collection(_enums.AutoModerationRuleKeywordPresetType, data)
    ),
    'allow_list': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    ),
    'mention_total_limit': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'mention_raid_protection_enabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class AutoModerationTriggerMetadata(_types.Object[_protocols.AutoModerationTriggerMetadata], fields = _AutoModerationTriggerMetadata_fields):

    """
    |dsrc| :ddoc:`Resources </resources/auto-moderation#auto-moderation-rule-object-trigger-metadata>`
    """

    keyword_filter: _types.Collection[_types.String] = vessel.GetField(
        select = lambda root: root['keyword_filter']
    )
    """
    |dsrc| **keyword_filter**
    """
    regex_patterns: _types.Collection[_types.String] = vessel.GetField(
        select = lambda root: root['regex_patterns']
    )
    """
    |dsrc| **regex_patterns**
    """
    presets: _types.Collection[_enums.AutoModerationRuleKeywordPresetType] = vessel.GetField(
        select = lambda root: root['presets']
    )
    """
    |dsrc| **presets**
    """
    allow_list: _types.Collection[_types.String] = vessel.GetField(
        select = lambda root: root['allow_list']
    )
    """
    |dsrc| **allow_list**
    """
    mention_total_limit: _types.Integer = vessel.GetField(
        select = lambda root: root['mention_total_limit']
    )
    """
    |dsrc| **mention_total_limit**
    """
    mention_raid_protection_enabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['mention_raid_protection_enabled']
    )
    """
    |dsrc| **mention_total_limit**
    """


_AutoModerationAction_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.AutoModerationActionType(data)
    ),
    'metadata': vessel.SetField(
        create = lambda path, data: AutoModerationActionMetadata(data)
    )
}


class AutoModerationAction(_types.Object[_protocols.AutoModerationAction], fields = _AutoModerationAction_fields):

    """
    |dsrc| :ddoc:`Auto Moderation Action Structure </resources/auto-moderation#auto-moderation-action-object-auto-moderation-action-structure>`
    """

    type: _enums.AutoModerationActionType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    metadata: 'AutoModerationActionMetadata' = vessel.GetField(
        select = lambda root: root['metadata']
    )
    """
    |dsrc| **metadata**
    """


_AutoModerationActionMetadata_fields = {
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'duration_seconds': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'custom_message': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class AutoModerationActionMetadata(_types.Object[_protocols.AutoModerationActionMetadata], fields = _AutoModerationActionMetadata_fields):

    """
    |dsrc| :ddoc:`Resources </resources/auto-moderation#auto-moderation-action-object-auto-moderation-action-structure>`
    """

    channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    duration_seconds: _types.Integer = vessel.GetField(
        select = lambda root: root['duration_seconds']
    )
    """
    |dsrc| **duration_seconds**
    """
    custom_message: _types.String = vessel.GetField(
        select = lambda root: root['custom_message']
    )
    """
    |dsrc| **custom_message**
    """


# SECTION: https://discord.com/developers/docs/resources/channel


_Channel_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.ChannelType(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'position': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'permission_overwrites': vessel.SetField(
        create = lambda path, data: _types.Collection(Overwrite, data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'topic': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'nsfw': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'last_message_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'bitrate': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'user_limit': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'rate_limit_per_user': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'recipients': vessel.SetField(
        create = lambda path, data: _types.Collection(User, data)
    ),
    'icon': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'owner_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'managed': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'parent_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'last_pin_timestamp': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'rtc_region': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'video_quality_mode': vessel.SetField(
        create = lambda path, data: _enums.ChannelVideoQualityMode(data)
    ),
    'message_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'member_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'thread_metadata': vessel.SetField(
        create = lambda path, data: ThreadMetadata(data)
    ),
    'member': vessel.SetField(
        create = lambda path, data: ThreadMember(data)
    ),
    'default_auto_archive_duration': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'permissions': vessel.SetField(
        create = lambda path, data: _enums.Permissions(data)
    ),
    'flags': vessel.SetField(
        create = lambda path, data: _enums.ChannelFlags(data)
    ),
    'total_message_sent': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'available_tags': vessel.SetField(
        create = lambda path, data: _types.Collection(ForumTag, data)
    ),
    'applied_tags': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'default_reaction_emoji': vessel.SetField(
        create = lambda path, data: DefaultReaction(data)
    ),
    'default_thread_rate_limit_per_user': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'default_sort_order': vessel.SetField(
        create = lambda path, data: _enums.ChannelSortOrderType(data)
    ),
    'default_forum_layout': vessel.SetField(
        create = lambda path, data: _enums.ForumLayoutType(data)
    )
}


def _Channel_identify(path, data):

    data_id = data['id']
    core_id: _types.Snowflake(data_id)

    return core_id


class Channel(_types.Object[_protocols.Channel], fields = _Channel_fields):

    """
    |dsrc| :ddoc:`Channel Structure </resources/channel#channel-object-channel-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    type: _enums.ChannelType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    position: _types.Integer = vessel.GetField(
        select = lambda root: root['position']
    )
    """
    |dsrc| **position**
    """
    permission_overwrites: _types.Collection['Overwrite'] = vessel.GetField(
        select = lambda root: root['permission_overwrites']
    )
    """
    |dsrc| **permission_overwrites**
    """
    name: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    topic: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['topic']
    )
    """
    |dsrc| **topic**
    """
    nsfw: _types.Boolean = vessel.GetField(
        select = lambda root: root['nsfw']
    )
    """
    |dsrc| **nsfw**
    """
    last_message_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['last_message_id']
    )
    """
    |dsrc| **last_message_id**
    """
    bitrate: _types.Integer = vessel.GetField(
        select = lambda root: root['bitrate']
    )
    """
    |dsrc| **bitrate**
    """
    user_limit: _types.Integer = vessel.GetField(
        select = lambda root: root['user_limit']
    )
    """
    |dsrc| **user_limit**
    """
    rate_limit_per_user: _types.Integer = vessel.GetField(
        select = lambda root: root['rate_limit_per_user']
    )
    """
    |dsrc| **rate_limit_per_user**
    """
    recipients: _types.Collection['User'] = vessel.GetField(
        select = lambda root: root['recipients']
    )
    """
    |dsrc| **recipients**
    """
    icon: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['icon']
    )
    """
    |dsrc| **icon**
    """
    owner_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['owner_id']
    )
    """
    |dsrc| **owner_id**
    """
    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['application_id']
    )
    """
    |dsrc| **application_id**
    """
    managed: _types.Boolean = vessel.GetField(
        select = lambda root: root['managed']
    )
    """
    |dsrc| **managed**
    """
    parent_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['parent_id']
    )
    """
    |dsrc| **parent_id**
    """
    last_pin_timestamp: typing.Union[None, _types.ISO8601Timestamp] = vessel.GetField(
        select = lambda root: root['last_pin_timestamp']
    )
    """
    |dsrc| **last_pin_timestamp**
    """
    rtc_region: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['rtc_region']
    )
    """
    |dsrc| **rtc_region**
    """
    video_quality_mode: _enums.ChannelVideoQualityMode = vessel.GetField(
        select = lambda root: root['video_quality_mode']
    )
    """
    |dsrc| **video_quality_mode**
    """
    message_count: _types.Integer = vessel.GetField(
        select = lambda root: root['message_count']
    )
    """
    |dsrc| **message_count**
    """
    member_count: _types.Integer = vessel.GetField(
        select = lambda root: root['member_count']
    )
    """
    |dsrc| **member_count**
    """
    thread_metadata: 'ThreadMetadata' = vessel.GetField(
        select = lambda root: root['thread_metadata']
    )
    """
    |dsrc| **thread_metadata**
    """
    member: 'ThreadMember' = vessel.GetField(
        select = lambda root: root['member']
    )
    """
    |dsrc| **member**
    """
    default_auto_archive_duration: _types.Integer = vessel.GetField(
        select = lambda root: root['default_auto_archive_duration']
    )
    """
    |dsrc| **default_auto_archive_duration**
    """
    permissions: _enums.Permissions = vessel.GetField(
        select = lambda root: root['permissions']
    )
    """
    |dsrc| **permissions**
    """
    flags: _enums.ChannelFlags = vessel.GetField(
        select = lambda root: root['flags']
    )
    """
    |dsrc| **flags**
    """
    total_message_sent: _types.Integer = vessel.GetField(
        select = lambda root: root['total_message_sent']
    )
    """
    |dsrc| **total_message_sent**
    """
    available_tags: _types.Collection['ForumTag'] = vessel.GetField(
        select = lambda root: root['available_tags']
    )
    """
    |dsrc| **available_tags**
    """
    applied_tags: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['applied_tags']
    )
    """
    |dsrc| **applied_tags**
    """
    default_reaction_emoji: typing.Union[None, 'DefaultReaction'] = vessel.GetField(
        select = lambda root: root['default_reaction_emoji']
    )
    """
    |dsrc| **default_reaction_emoji**
    """
    default_thread_rate_limit_per_user: _types.Integer = vessel.GetField(
        select = lambda root: root['default_thread_rate_limit_per_user']
    )
    """
    |dsrc| **default_thread_rate_limit_per_user**
    """
    default_sort_order: typing.Union[None, _enums.ChannelSortOrderType] = vessel.GetField(
        select = lambda root: root['default_sort_order']
    )
    """
    |dsrc| **default_sort_order**
    """
    default_forum_layout: _enums.ForumLayoutType = vessel.GetField(
        select = lambda root: root['default_forum_layout']
    )
    """
    |dsrc| **default_forum_layout**
    """

    def mention(self):

        """
        Get the mention.
        """

        return _mentions.channel(self.id)


def _Message_fields_get_components_subtype(data):

    type = data['type']

    if type in {_enums.MessageComponentType.action_row}:
        return MessageActionRowComponent
    
    raise ValueError(f'unhandleable type: {type}')


_Message_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'author': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'content': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'timestamp': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'edited_timestamp': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'tts': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'mention_everyone': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'mentions': vessel.SetField(
        create = lambda path, data: _types.Collection(User, data)
    ),
    'mention_roles': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'mention_channels': vessel.SetField(
        create = lambda path, data: _types.Collection(Channel, data)
    ),
    'attachments': vessel.SetField(
        create = lambda path, data: _types.Collection(Attachment, data)
    ),
    'embeds': vessel.SetField(
        create = lambda path, data: _types.Collection(Embed, data)
    ),
    'reactions': vessel.SetField(
        create = lambda path, data: _types.Collection(Reaction, data)
    ),
    'nonce': vessel.SetField(
        # NOTE: missing type matching specification
        create = lambda path, data: data
    ),
    'pinned': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'webhook_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.MessageType(data)
    ),
    'activity': vessel.SetField(
        create = lambda path, data: MessageActivity(data)
    ),
    'application': vessel.SetField(
        create = lambda path, data: Application(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'message_reference': vessel.SetField(
        create = lambda path, data: MessageReference(data)
    ),
    'flags': vessel.SetField(
        create = lambda path, data: _enums.MessageFlags(data)
    ),
    'referenced_message': vessel.SetField(
        create = lambda path, data: Message(data)
    ),
    # 'interaction': vessel.SetField(
    #     create = lambda path, data: MessageInteraction(data)
    # ),
    'thread': vessel.SetField(
        create = lambda path, data: Channel(data)
    ),
    'components': vessel.SetField(
        create = lambda path, data: _types.Collection(lambda data: _Message_fields_get_components_subtype(data)(data), data)
    ),
    'sticker_items': vessel.SetField(
        create = lambda path, data: _types.Collection(Sticker, data)
    ),
    # 'stickers': vessel.SetField(
    #     create = lambda path, data: _types.Collection(Sticker, data)
    # ),
    'position': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'role_subscription_data': vessel.SetField(
        create = lambda path, data: RoleSubscriptionData(data)
    ),
    'interaction_metadata': vessel.SetField(
        create = lambda path, data: MessageInteractionMetadata(data)
    )
}


class Message(_types.Object[_protocols.Message], fields = _Message_fields):

    """
    |dsrc| :ddoc:`Message Structure </resources/channel#message-object-message-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    author: 'User' = vessel.GetField(
        select = lambda root: root['author']
    )
    """
    |dsrc| **author**
    """
    content: _types.String = vessel.GetField(
        select = lambda root: root['content']
    )
    """
    |dsrc| **content**
    """
    timestamp: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['timestamp']
    )
    """
    |dsrc| **timestamp**
    """
    edited_timestamp: typing.Union[None, _types.ISO8601Timestamp] = vessel.GetField(
        select = lambda root: root['edited_timestamp']
    )
    """
    |dsrc| **edited_timestamp**
    """
    tts: _types.Boolean = vessel.GetField(
        select = lambda root: root['tts']
    )
    """
    |dsrc| **tts**
    """
    mention_everyone: _types.Boolean = vessel.GetField(
        select = lambda root: root['mention_everyone']
    )
    """
    |dsrc| **mention_everyone**
    """
    mentions: _types.Collection['User'] = vessel.GetField(
        select = lambda root: root['mentions']
    )
    """
    |dsrc| **mentions**
    """
    mention_roles: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['mention_roles']
    )
    """
    |dsrc| **mention_roles**
    """
    mention_channels: _types.Collection['Channel'] = vessel.GetField(
        select = lambda root: root['mention_channels']
    )
    """
    |dsrc| **mention_channels**
    """
    attachments: _types.Collection['Attachment'] = vessel.GetField(
        select = lambda root: root['attachments']
    )
    """
    |dsrc| **attachments**
    """
    embeds: _types.Collection['Embed'] = vessel.GetField(
        select = lambda root: root['embeds']
    )
    """
    |dsrc| **embeds**
    """
    reactions: _types.Collection['Reaction'] = vessel.GetField(
        select = lambda root: root['reactions']
    )
    """
    |dsrc| **reactions**
    """
    nonce: _types.String | _types.Integer = vessel.GetField(
        select = lambda root: root['nonce']
    )
    """
    |dsrc| **nonce**
    """
    pinned: _types.Boolean = vessel.GetField(
        select = lambda root: root['pinned']
    )
    """
    |dsrc| **pinned**
    """
    webhook_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['webhook_id']
    )
    """
    |dsrc| **webhook_id**
    """
    type: _enums.MessageType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    activity: 'MessageActivity' = vessel.GetField(
        select = lambda root: root['activity']
    )
    """
    |dsrc| **activity**
    """
    application: 'Application' = vessel.GetField(
        select = lambda root: root['application']
    )
    """
    |dsrc| **application**
    """
    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['application_id']
    )
    """
    |dsrc| **application_id**
    """
    message_reference: 'MessageReference' = vessel.GetField(
        select = lambda root: root['message_reference']
    )
    """
    |dsrc| **message_reference**
    """
    flags: _enums.MessageFlags = vessel.GetField(
        select = lambda root: root['flags']
    )
    """
    |dsrc| **flags**
    """
    referenced_message: typing.Union[None, 'Message'] = vessel.GetField(
        select = lambda root: root['referenced_message']
    )
    """
    |dsrc| **referenced_message**
    """
    interaction: 'MessageInteraction' = vessel.GetField(
        select = lambda root: root['interaction']
    )
    """
    |dsrc| **interaction** (deprecated)
    """
    thread: 'Channel' = vessel.GetField(
        select = lambda root: root['thread']
    )
    """
    |dsrc| **thread**
    """
    components: _types.Collection['MessageActionRowComponent'] = vessel.GetField(
        select = lambda root: root['components']
    )
    """
    |dsrc| **components**
    """
    stickers: _types.Collection['Sticker'] = vessel.GetField(
        select = lambda root: root['sticker_items']
    )
    """
    |dsrc| **sticker_items** 
    """
    position: _types.Integer = vessel.GetField(
        select = lambda root: root['position']
    )
    """
    |dsrc| **position**
    """
    role_subscription_data: 'RoleSubscriptionData' = vessel.GetField(
        select = lambda root: root['role_subscription_data']
    )
    """
    |dsrc| **role_subscription_data**
    """
    interaction_metadata: 'MessageInteractionMetadata' = vessel.GetField(
        select = lambda root: root['interaction_metadata']
    )
    """
    |dsrc| **interaction_metadata**
    """


_MessageInteractionMetadata_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data['id'])
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.InteractionType(data['type'])
    ),
    'user_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data['user_id'])
    ),
    'authorizing_integration_owners': vessel.SetField(
        create = lambda path, data: dict(
            map(
                lambda item: (
                    _enums.ApplicationIntegrationType(item[0]),
                    item[1]
                ),
                data.items()
            )
        )
    ),
    'original_response_message_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data['original_response_message_id'])
    ),
    'triggering_interaction_metadata': vessel.SetField(
        create = lambda path, data: MessageInteractionMetadata(data['triggering_interaction_metadata'])
    )
}

class MessageInteractionMetadata(_types.Object[_protocols.MessageInteractionMetadata], fields = _MessageInteractionMetadata_fields):

    """
    |dsrc| :ddoc:`Message Interaction Metadata Structure </resources/channel#message-interaction-metadata-object-message-interaction-metadata-structure`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    type: _enums.InteractionType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    user_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['user_id']
    )
    """
    |dsrc| **user_id**
    """
    authorizing_integration_owners: dict[_enums.ApplicationIntegrationType, _enums.InteractionContextType] = vessel.GetField(
        select = lambda root: root['authorizing_integration_owners']
    )
    """
    |dsrc| **authorizing_integration_owners**
    """
    original_response_message_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['original_response_message_id']
    )
    """
    |dsrc| **original_response_message_id**
    """
    interacted_message_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['interacted_message_id']
    )
    """
    |dsrc| **interacted_message_id**
    """
    triggering_interaction_metadata: 'MessageInteractionMetadata' = vessel.GetField(
        select = lambda root: root['triggering_interaction_metadata']
    )
    """
    |dsrc| **triggering_interaction_metadata**
    """
    

_MessageActivity_fields = {
    'type': vessel.SetField(
        create = lambda path, data: _enums.MessageActivityType(data)
    ),
    'party_id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class MessageActivity(_types.Object[_protocols.MessageActivity], fields = _MessageActivity_fields):

    """
    |dsrc| :ddoc:`Message Activity Structure </resources/channel#message-object-message-activity-structure>`
    """

    type: _enums.MessageActivityType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    party_id: _types.String = vessel.GetField(
        select = lambda root: root['party_id']
    )
    """
    |dsrc| **party_id**
    """


_MessageReference_fields = {
    'message_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'fail_if_not_exists': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class MessageReference(_types.Object[_protocols.MessageReference], fields = _MessageReference_fields):

    """
    |dsrc| :ddoc:`Message Reference Structure </resources/channel#message-reference-object-message-reference-structure>`
    """

    message_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['message_id']
    )
    """
    |dsrc| **message_id**
    """
    channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    fail_if_not_exists: _types.Boolean = vessel.GetField(
        select = lambda root: root['fail_if_not_exists']
    )
    """
    |dsrc| **fail_if_not_exists**
    """


_Reaction_fields = {
    'count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'me': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'emoji': vessel.SetField(
        create = lambda path, data: Emoji(data)
    )
}


class Reaction(_types.Object[_protocols.Reaction], fields = _Reaction_fields):

    """
    |dsrc| :ddoc:`Reaction Structure </resources/channel#reaction-object-reaction-structure>`
    """

    count: _types.Integer = vessel.GetField(
        select = lambda root: root['count']
    )
    """
    |dsrc| **count**
    """
    me: _types.Boolean = vessel.GetField(
        select = lambda root: root['me']
    )
    """
    |dsrc| **me**
    """
    emoji: 'Emoji' = vessel.GetField(
        select = lambda root: root['emoji']
    )
    """
    |dsrc| **emoji**
    """


_FollowedChannel_fields = {
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
    ),
    'webhook_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
    )
}


class FollowedChannel(_types.Object[_protocols.FollowedChannel], fields = _FollowedChannel_fields):

    """
    |dsrc| :ddoc:`Followed Channel Structure </resources/channel#followed-channel-object-followed-channel-structure>`
    """

    channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    webhook_id: _enums.OverwriteType = vessel.GetField(
        select = lambda root: root['webhook_id']
    )
    """
    |dsrc| **webhook_id**
    """



_Overwrite_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.OverwriteType(data)
    ),
    'allow': vessel.SetField(
        create = lambda path, data: _enums.Permissions(data)
    ),
    'deny': vessel.SetField(
        create = lambda path, data: _enums.Permissions(data)
    )
}


class Overwrite(_types.Object[_protocols.Overwrite], fields = _Overwrite_fields):

    """
    |dsrc| :ddoc:`Overwrite Structure </resources/channel#overwrite-object-overwrite-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    type: _enums.OverwriteType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    allow: _enums.Permissions = vessel.GetField(
        select = lambda root: root['allow']
    )
    """
    |dsrc| **allow**
    """
    deny: _enums.Permissions = vessel.GetField(
        select = lambda root: root['deny']
    )
    """
    |dsrc| **deny**
    """


_ThreadMetadata_fields = {
    'archived': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'auto_archive_duration': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'archive_timestamp': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'locked': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'invitable': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'create_timestamp': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    )
}


class ThreadMetadata(_types.Object[_protocols.ThreadMetadata], fields = _ThreadMetadata_fields):

    """
    |dsrc| :ddoc:`Thread Metadata Structure </resources/channel#thread-metadata-object-thread-metadata-structure>`
    """

    archived: _types.Boolean = vessel.GetField(
        select = lambda root: root['archived']
    )
    """
    |dsrc| **archived**
    """
    auto_archive_duration: _types.Integer = vessel.GetField(
        select = lambda root: root['auto_archive_duration']
    )
    """
    |dsrc| **auto_archive_duration**
    """
    archive_timestamp: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['archive_timestamp']
    )
    """
    |dsrc| **archive_timestamp**
    """
    locked: _types.Boolean = vessel.GetField(
        select = lambda root: root['locked']
    )
    """
    |dsrc| **locked**
    """
    invitable: _types.Boolean = vessel.GetField(
        select = lambda root: root['invitable']
    )
    """
    |dsrc| **invitable**
    """
    create_timestamp: typing.Union[None, _types.ISO8601Timestamp] = vessel.GetField(
        select = lambda root: root['create_timestamp']
    )
    """
    |dsrc| **create_timestamp**
    """


_ThreadMember_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'user_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'join_timestamp': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'flags': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'member': vessel.SetField(
        create = lambda path, data: GuildMember(data)
    )
}


class ThreadMember(_types.Object[_protocols.ThreadMember], fields = _ThreadMember_fields):

    """
    |dsrc| :ddoc:`Thread Member Structure </resources/channel#thread-member-object-thread-member-structure>`
    """

    thread_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    user_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['user_id']
    )
    """
    |dsrc| **user_id**
    """
    join_timestamp: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['join_timestamp']
    )
    """
    |dsrc| **join_timestamp**
    """
    flags: _types.Integer = vessel.GetField(
        select = lambda root: root['flags']
    )
    """
    |dsrc| **flags**
    """
    member: 'GuildMember' = vessel.GetField(
        select = lambda root: root['member']
    )
    """
    |dsrc| **member**
    """


_DefaultReaction_fields = {
    'emoji_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'emoji_name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class DefaultReaction(_types.Object[_protocols.DefaultReaction], fields = _DefaultReaction_fields):

    """
    |dsrc| :ddoc:`Default Reaction Structure </resources/channel#default-reaction-object-default-reaction-structure>`
    """

    emoji_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['emoji_id']
    )
    """
    |dsrc| **emoji_id**
    """
    emoji_name: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['emoji_name']
    )
    """
    |dsrc| **emoji_name**
    """


_ForumTag_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'moderated': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'emoji_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'emoji_name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class ForumTag(_types.Object[_protocols.ForumTag], fields = _ForumTag_fields):

    """
    |dsrc| :ddoc:`Forum Tag Structure </resources/channel#forum-tag-object-forum-tag-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    moderated: _types.Boolean = vessel.GetField(
        select = lambda root: root['moderated']
    )
    """
    |dsrc| **moderated**
    """
    emoji_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['emoji_id']
    )
    """
    |dsrc| **emoji_id**
    """
    emoji_name: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['emoji_name']
    )
    """
    |dsrc| **emoji_name**
    """


_Embed_fields = {
    'title': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.EmbedType(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'timestamp': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'color': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'footer': vessel.SetField(
        create = lambda path, data: EmbedFooter(data)
    ),
    'image': vessel.SetField(
        create = lambda path, data: EmbedImage(data)
    ),
    'thumbnail': vessel.SetField(
        create = lambda path, data: EmbedThumbnail(data)
    ),
    'video': vessel.SetField(
        create = lambda path, data: EmbedVideo(data)
    ),
    'provider': vessel.SetField(
        create = lambda path, data: EmbedProvider(data)
    ),
    'author': vessel.SetField(
        create = lambda path, data: EmbedAuthor(data)
    ),
    'fields': vessel.SetField(
        create = lambda path, data: _types.Collection(EmbedField, data)
    )
}


class Embed(_types.Object[_protocols.Embed], fields = _Embed_fields):

    """
    |dsrc| :ddoc:`Embed Structure </resources/channel#embed-object-embed-structure>`
    """

    title: _types.String = vessel.GetField(
        select = lambda root: root['title']
    )
    """
    |dsrc| **title**
    """
    type: _enums.EmbedType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """
    timestamp: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['timestamp']
    )
    """
    |dsrc| **timestamp**
    """
    color: _types.Integer = vessel.GetField(
        select = lambda root: root['color']
    )
    """
    |dsrc| **color**
    """
    footer: 'EmbedFooter' = vessel.GetField(
        select = lambda root: root['footer']
    )
    """
    |dsrc| **footer**
    """
    image: 'EmbedImage' = vessel.GetField(
        select = lambda root: root['image']
    )
    """
    |dsrc| **image**
    """
    thumbnail: 'EmbedThumbnail' = vessel.GetField(
        select = lambda root: root['thumbnail']
    )
    """
    |dsrc| **thumbnail**
    """
    video: 'EmbedVideo' = vessel.GetField(
        select = lambda root: root['video']
    )
    """
    |dsrc| **video**
    """
    provider: 'EmbedProvider' = vessel.GetField(
        select = lambda root: root['provider']
    )
    """
    |dsrc| **provider**
    """
    author: 'EmbedAuthor' = vessel.GetField(
        select = lambda root: root['author']
    )
    """
    |dsrc| **author**
    """
    fields: _types.Collection['EmbedField'] = vessel.GetField(
        select = lambda root: root['fields']
    )
    """
    |dsrc| **fields**
    """


_EmbedThumbnail_fields = {
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'proxy_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'height': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'width': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    )
}


class EmbedThumbnail(_types.Object[_protocols.EmbedThumbnail], fields = _EmbedThumbnail_fields):

    """
    |dsrc| :ddoc:`Embed Thumbnail Structure </resources/channel#embed-object-embed-thumbnail-structure>`
    """

    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """
    proxy_url: _types.String = vessel.GetField(
        select = lambda root: root['proxy_url']
    )
    """
    |dsrc| **proxy_url**
    """
    height: _types.Integer = vessel.GetField(
        select = lambda root: root['height']
    )
    """
    |dsrc| **height**
    """
    width: _types.Integer = vessel.GetField(
        select = lambda root: root['width']
    )
    """
    |dsrc| **width**
    """


_EmbedVideo_fields = {
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'proxy_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'height': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'width': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    )
}


class EmbedVideo(_types.Object[_protocols.EmbedVideo], fields = _EmbedVideo_fields):

    """
    |dsrc| :ddoc:`Embed Video Structure </resources/channel#embed-object-embed-video-structure>`
    """

    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """
    proxy_url: _types.String = vessel.GetField(
        select = lambda root: root['proxy_url']
    )
    """
    |dsrc| **proxy_url**
    """
    height: _types.Integer = vessel.GetField(
        select = lambda root: root['height']
    )
    """
    |dsrc| **height**
    """
    width: _types.Integer = vessel.GetField(
        select = lambda root: root['width']
    )
    """
    |dsrc| **width**
    """


_EmbedImage_fields = {
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'proxy_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'height': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'width': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    )
}


class EmbedImage(_types.Object[_protocols.EmbedImage], fields = _EmbedImage_fields):

    """
    |dsrc| :ddoc:`Embed Image Structure </resources/channel#embed-object-embed-image-structure>`
    """

    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """
    proxy_url: _types.String = vessel.GetField(
        select = lambda root: root['proxy_url']
    )
    """
    |dsrc| **proxy_url**
    """
    height: _types.Integer = vessel.GetField(
        select = lambda root: root['height']
    )
    """
    |dsrc| **height**
    """
    width: _types.Integer = vessel.GetField(
        select = lambda root: root['width']
    )
    """
    |dsrc| **width**
    """


_EmbedProvider_fields = {
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class EmbedProvider(_types.Object[_protocols.EmbedProvider], fields = _EmbedProvider_fields):

    """
    |dsrc| :ddoc:`Embed Provider Structure </resources/channel#embed-object-embed-provider-structure>`
    """

    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """


_EmbedAuthor_fields = {
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'icon_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'proxy_icon_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class EmbedAuthor(_types.Object[_protocols.EmbedAuthor], fields = _EmbedAuthor_fields):

    """
    |dsrc| :ddoc:`Embed Author Structure </resources/channel#embed-object-embed-author-structure>`
    """

    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """
    icon_url: _types.String = vessel.GetField(
        select = lambda root: root['icon_url']
    )
    """
    |dsrc| **icon_url**
    """
    proxy_icon_url: _types.String = vessel.GetField(
        select = lambda root: root['proxy_icon_url']
    )
    """
    |dsrc| **proxy_icon_url**
    """


_EmbedFooter_fields = {
    'text': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'icon_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'proxy_icon_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class EmbedFooter(_types.Object[_protocols.EmbedFooter], fields = _EmbedFooter_fields):

    """
    |dsrc| :ddoc:`Embed Footer Structure </resources/channel#embed-object-embed-footer-structure>`
    """

    text: _types.String = vessel.GetField(
        select = lambda root: root['text']
    )
    """
    |dsrc| **text**
    """
    icon_url: _types.String = vessel.GetField(
        select = lambda root: root['icon_url']
    )
    """
    |dsrc| **icon_url**
    """
    proxy_icon_url: _types.String = vessel.GetField(
        select = lambda root: root['proxy_icon_url']
    )
    """
    |dsrc| **proxy_icon_url**
    """


_EmbedField_fields = {
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'value': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'inline': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class EmbedField(_types.Object[_protocols.EmbedField], fields = _EmbedField_fields):

    """
    |dsrc| :ddoc:`Embed Field Structure </resources/channel#embed-object-embed-field-structure>`
    """

    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    value: _types.String = vessel.GetField(
        select = lambda root: root['value']
    )
    """
    |dsrc| **value**
    """
    inline: _types.Boolean = vessel.GetField(
        select = lambda root: root['inline']
    )
    """
    |dsrc| **inline**
    """


_Attachment_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'filename': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'content_type': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'size': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'proxy_url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'height': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'width': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'ephemeral': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'duration_secs': vessel.SetField(
        create = lambda path, data: _types.Decimal(data)
    ),
    'waveform': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class Attachment(_types.Object[_protocols.Attachment], fields = _Attachment_fields):

    """
    |dsrc| :ddoc:`Resources </resources/channel#embed-object-embed-field-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    filename: _types.String = vessel.GetField(
        select = lambda root: root['filename']
    )
    """
    |dsrc| **filename**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    content_type: _types.String = vessel.GetField(
        select = lambda root: root['content_type']
    )
    """
    |dsrc| **content_type**
    """
    size: _types.Integer = vessel.GetField(
        select = lambda root: root['size']
    )
    """
    |dsrc| **size**
    """
    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """
    proxy_url: _types.String = vessel.GetField(
        select = lambda root: root['proxy_url']
    )
    """
    |dsrc| **proxy_url**
    """
    height: typing.Union[None, _types.Integer] = vessel.GetField(
        select = lambda root: root['height']
    )
    """
    |dsrc| **height**
    """
    width: typing.Union[None, _types.Integer] = vessel.GetField(
        select = lambda root: root['width']
    )
    """
    |dsrc| **width**
    """
    ephemeral: _types.Boolean = vessel.GetField(
        select = lambda root: root['ephemeral']
    )
    """
    |dsrc| **ephemeral**
    """
    duration_secs: _types.Decimal = vessel.GetField(
        select = lambda root: root['duration_secs']
    )
    """
    |dsrc| **duration_secs**
    """
    waveform: _types.String = vessel.GetField(
        select = lambda root: root['waveform']
    )
    """
    |dsrc| **waveform**
    """


_AllowedMentions_fields = {
    'parse': vessel.SetField(
        create = lambda path, data: _types.Collection(_enums.AllowedMentionsType, data)
    ),
    'roles': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'users': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'replied_user': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class AllowedMentions(_types.Object[_protocols.AllowedMentions], fields = _AllowedMentions_fields):

    """
    |dsrc| :ddoc:`Allowed Mentions Structure </resources/channel#allowed-mentions-object-allowed-mentions-structure>`
    """

    parse: _types.Collection[_enums.AllowedMentionsType] = vessel.GetField(
        select = lambda root: root['parse']
    )
    """
    |dsrc| **parse**
    """
    roles: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['roles']
    )
    """
    |dsrc| **roles**
    """
    users: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['users']
    )
    """
    |dsrc| **users**
    """
    replied_user: _types.Boolean = vessel.GetField(
        select = lambda root: root['replied_user']
    )
    """
    |dsrc| **replied_user**
    """


_RoleSubscriptionData_fields = {
    'role_subscription_listing_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'tier_name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'total_months_subscribed': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'is_renewal': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class RoleSubscriptionData(_types.Object[_protocols.RoleSubscriptionData], fields = _RoleSubscriptionData_fields):

    """
    |dsrc| :ddoc:`Role Subscription Data Object </resources/channel#role-subscription-data-object>`
    """

    role_subscription_listing_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['role_subscription_listing_id']
    )
    """
    |dsrc| **role_subscription_listing_id**
    """
    tier_name: _types.String = vessel.GetField(
        select = lambda root: root['tier_name']
    )
    """
    |dsrc| **tier_name**
    """
    total_months_subscribed: _types.Integer = vessel.GetField(
        select = lambda root: root['total_months_subscribed']
    )
    """
    |dsrc| **total_months_subscribed**
    """
    is_renewal: _types.Boolean = vessel.GetField(
        select = lambda root: root['is_renewal']
    )
    """
    |dsrc| **is_renewal**
    """


# SECTION: https://discord.com/developers/docs/resources/emoji


_Emoji_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'roles': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'require_colons': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'managed': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'animated': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'available': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class Emoji(_types.Object[_protocols.Emoji], fields = _Emoji_fields):

    """
    |dsrc| :ddoc:`Emoji Structure </resources/emoji#emoji-object-emoji-structure>`
    """

    id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    roles: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['roles']
    )
    """
    |dsrc| **roles**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    require_colons: _types.Boolean = vessel.GetField(
        select = lambda root: root['require_colons']
    )
    """
    |dsrc| **require_colons**
    """
    managed: _types.Boolean = vessel.GetField(
        select = lambda root: root['managed']
    )
    """
    |dsrc| **managed**
    """
    animated: _types.Boolean = vessel.GetField(
        select = lambda root: root['animated']
    )
    """
    |dsrc| **animated**
    """
    available: _types.Boolean = vessel.GetField(
        select = lambda root: root['available']
    )
    """
    |dsrc| **available**
    """

    def mention(self):

        """
        Get the mention.
        """

        return _mentions.emoji(self.name, self.id, animated = self.animated)
    
    def image_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the image url.
        """

        return _images.emoji(self.id, **kwargs)


# SECTION: https://discord.com/developers/docs/resources/guild


_Guild_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'icon': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'icon_hash': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'splash': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'discovery_splash': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'owner': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'owner_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'permissions': vessel.SetField(
        create = lambda path, data: _enums.Permissions(data)
    ),
    'afk_channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'afk_timeout': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'widget_enabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'widget_channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'verification_level': vessel.SetField(
        create = lambda path, data: _enums.GuildVerificationLevel(data)
    ),
    'default_message_notifications': vessel.SetField(
        create = lambda path, data: _enums.GuildDefaultMessageNotificationLevel(data)
    ),
    'explicit_content_filter': vessel.SetField(
        create = lambda path, data: _enums.GuildExplicitContentFilterLevel(data)
    ),
    'roles': vessel.SetField(
        create = lambda path, data: _types.Collection(Role, data)
    ),
    'emojis': vessel.SetField(
        create = lambda path, data: _types.Collection(Emoji, data)
    ),
    'features': vessel.SetField(
        create = lambda path, data: _types.Collection(_enums.GuildFeature, data)
    ),
    'mfa_level': vessel.SetField(
        create = lambda path, data: _enums.GuildMFALevel(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'system_channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'system_channel_flags': vessel.SetField(
        create = lambda path, data: _enums.GuildSystemChannelFlags(data)
    ),
    'rules_channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'max_presences': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'max_members': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'vanity_url_code': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'banner': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'premium_tier': vessel.SetField(
        create = lambda path, data: _enums.GuildPremiumTier(data)
    ),
    'premium_subscription_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'preferred_locale': vessel.SetField(
        create = lambda path, data: _enums.Locale(data)
    ),
    'public_updates_channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'max_video_channel_users': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'max_stage_video_channel_users': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'approximate_member_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'approximate_presence_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'welcome_screen': vessel.SetField(
        create = lambda path, data: WelcomeScreen(data)
    ),
    'nsfw_level': vessel.SetField(
        create = lambda path, data: _enums.GuildNSFWLevel(data)
    ),
    'stickers': vessel.SetField(
        create = lambda path, data: _types.Collection(Sticker, data)
    ),
    'premium_progress_bar_enabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'joined_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'large': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'unavailable': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'member_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'voice_states': vessel.SetField(
        create = lambda path, data: _types.Collection(VoiceState, data)
    ),
    'members': vessel.SetField(
        create = lambda path, data: _types.Collection(GuildMember, data)
    ),
    'channels': vessel.SetField(
        create = lambda path, data: _types.Collection(Channel, data)
    ),
    'threads': vessel.SetField(
        create = lambda path, data: _types.Collection(Channel, data)
    ),
    'presences': vessel.SetField(
        create = lambda path, data: _types.Collection(Presence, data)
    ),
    'stage_instances': vessel.SetField(
        create = lambda path, data: _types.Collection(StageInstance, data)
    ),
    'scheduled_events': vessel.SetField(
        create = lambda path, data: _types.Collection(GuildScheduledEvent, data)
    ),
    'safety_alerts_channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    )
}


class Guild(_types.Object[_protocols.Guild], fields = _Guild_fields):

    """
    |dsrc| :ddoc:`Guild Structure </resources/guild#guild-object-guild-structure>` | 
    :ddoc:`Guild Create Guild Create Extra Fields </topics/gateway-events#guild-create-guild-create-extra-fields>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    icon: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['icon']
    )
    """
    |dsrc| **icon**
    """
    icon_hash: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['icon_hash']
    )
    """
    |dsrc| **icon_hash**
    """
    splash: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['splash']
    )
    """
    |dsrc| **splash**
    """
    discovery_splash: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['discovery_splash']
    )
    """
    |dsrc| **discovery_splash**
    """
    owner: _types.Boolean = vessel.GetField(
        select = lambda root: root['owner']
    )
    """
    |dsrc| **owner**
    """
    owner_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['owner_id']
    )
    """
    |dsrc| **owner_id**
    """
    permissions: _enums.Permissions = vessel.GetField(
        select = lambda root: root['permissions']
    )
    """
    |dsrc| **permissions**
    """
    afk_channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['afk_channel_id']
    )
    """
    |dsrc| **afk_channel_id**
    """
    afk_timeout: _types.Integer = vessel.GetField(
        select = lambda root: root['afk_timeout']
    )
    """
    |dsrc| **afk_timeout**
    """
    widget_enabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['widget_enabled']
    )
    """
    |dsrc| **widget_enabled**
    """
    widget_channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['widget_channel_id']
    )
    """
    |dsrc| **widget_channel_id**
    """
    verification_level: _enums.GuildVerificationLevel = vessel.GetField(
        select = lambda root: root['verification_level']
    )
    """
    |dsrc| **verification_level**
    """
    default_message_notifications: _enums.GuildDefaultMessageNotificationLevel = vessel.GetField(
        select = lambda root: root['default_message_notifications']
    )
    """
    |dsrc| **default_message_notifications**
    """
    explicit_content_filter: _enums.GuildExplicitContentFilterLevel = vessel.GetField(
        select = lambda root: root['explicit_content_filter']
    )
    """
    |dsrc| **explicit_content_filter**
    """
    roles: _types.Collection['Role'] = vessel.GetField(
        select = lambda root: root['roles']
    )
    """
    |dsrc| **roles**
    """
    emojis: _types.Collection['Emoji'] = vessel.GetField(
        select = lambda root: root['emojis']
    )
    """
    |dsrc| **emojis**
    """
    features: _types.Collection[_enums.GuildFeature] = vessel.GetField(
        select = lambda root: root['features']
    )
    """
    |dsrc| **features**
    """
    mfa_level: _types.Integer = vessel.GetField(
        select = lambda root: root['mfa_level']
    )
    """
    |dsrc| **mfa_level**
    """
    application_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['application_id']
    )
    """
    |dsrc| **application_id**
    """
    system_channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['system_channel_id']
    )
    """
    |dsrc| **system_channel_id**
    """
    system_channel_flags: _enums.GuildSystemChannelFlags = vessel.GetField(
        select = lambda root: root['system_channel_flags']
    )
    """
    |dsrc| **system_channel_flags**
    """
    rules_channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['rules_channel_id']
    )
    """
    |dsrc| **rules_channel_id**
    """
    max_presences: typing.Union[None, _types.Integer] = vessel.GetField(
        select = lambda root: root['max_presences']
    )
    """
    |dsrc| **max_presences**
    """
    max_members: _types.Integer = vessel.GetField(
        select = lambda root: root['max_members']
    )
    """
    |dsrc| **max_members**
    """
    vanity_url_code: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['vanity_url_code']
    )
    """
    |dsrc| **vanity_url_code**
    """
    description: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    banner: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['banner']
    )
    """
    |dsrc| **banner**
    """
    premium_tier: _enums.GuildPremiumTier = vessel.GetField(
        select = lambda root: root['premium_tier']
    )
    """
    |dsrc| **premium_tier**
    """
    premium_subscription_count: _types.Integer = vessel.GetField(
        select = lambda root: root['premium_subscription_count']
    )
    """
    |dsrc| **premium_subscription_count**
    """
    preferred_locale: _types.String = vessel.GetField(
        select = lambda root: root['preferred_locale']
    )
    """
    |dsrc| **preferred_locale**
    """
    public_updates_channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['public_updates_channel_id']
    )
    """
    |dsrc| **public_updates_channel_id**
    """
    max_video_channel_users: _types.Integer = vessel.GetField(
        select = lambda root: root['max_video_channel_users']
    )
    """
    |dsrc| **max_video_channel_users**
    """
    max_stage_video_channel_users: _types.Integer = vessel.GetField(
        select = lambda root: root['max_stage_video_channel_users']
    )
    """
    |dsrc| **max_stage_video_channel_users**
    """
    approximate_member_count: _types.Integer = vessel.GetField(
        select = lambda root: root['approximate_member_count']
    )
    """
    |dsrc| **approximate_member_count**
    """
    approximate_presence_count: _types.Integer = vessel.GetField(
        select = lambda root: root['approximate_presence_count']
    )
    """
    |dsrc| **approximate_presence_count**
    """
    welcome_screen: 'WelcomeScreen' = vessel.GetField(
        select = lambda root: root['welcome_screen']
    )
    """
    |dsrc| **welcome_screen**
    """
    nsfw_level: _enums.GuildNSFWLevel = vessel.GetField(
        select = lambda root: root['nsfw_level']
    )
    """
    |dsrc| **nsfw_level**
    """
    stickers: _types.Collection['Sticker'] = vessel.GetField(
        select = lambda root: root['stickers']
    )
    """
    |dsrc| **stickers**
    """
    premium_progress_bar_enabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['premium_progress_bar_enabled']
    )
    """
    |dsrc| **premium_progress_bar_enabled**
    """
    joined_at: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['joined_at']
    )
    """
    |dsrc| **joined_at**
    """
    large: _types.Boolean = vessel.GetField(
        select = lambda root: root['large']
    )
    """
    |dsrc| **large**
    """
    unavailable: _types.Boolean = vessel.GetField(
        select = lambda root: root['unavailable']
    )
    """
    |dsrc| **unavailable**
    """
    member_count: _types.Integer = vessel.GetField(
        select = lambda root: root['member_count']
    )
    """
    |dsrc| **member_count**
    """
    voice_states: _types.Collection['VoiceState'] = vessel.GetField(
        select = lambda root: root['voice_states']
    )
    """
    |dsrc| **voice_states**
    """
    members: _types.Collection['GuildMember'] = vessel.GetField(
        select = lambda root: root['members']
    )
    """
    |dsrc| **members**
    """
    channels: _types.Collection['Channel'] = vessel.GetField(
        select = lambda root: root['channels']
    )
    """
    |dsrc| **channels**
    """
    threads: _types.Collection['Channel'] = vessel.GetField(
        select = lambda root: root['threads']
    )
    """
    |dsrc| **threads**
    """
    presences: _types.Collection['Presence'] = vessel.GetField(
        select = lambda root: root['presences']
    )
    """
    |dsrc| **presences**
    """
    stage_instances: _types.Collection['StageInstance'] = vessel.GetField(
        select = lambda root: root['stage_instances']
    )
    """
    |dsrc| **stage_instances**
    """
    scheduled_events: _types.Collection['GuildScheduledEvent'] = vessel.GetField(
        select = lambda root: root['scheduled_events']
    )
    """
    |dsrc| **scheduled_events**
    """
    safety_alerts_channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['safety_alerts_channel_id']
    )
    """
    |dsrc| **safety_alerts_channel_id**
    """

    def icon_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the icon url.
        """

        return _images.guild_icon(self.id, self.icon, **kwargs)

    def splash_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the splash url.
        """

        return _images.guild_splash(self.id, self.splash, **kwargs)

    def discovery_splash_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the discovery splash url.
        """

        return _images.guild_discovery_splash(self.id, self.discovery_splash, **kwargs)

    def banner_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the banner url.
        """

        return _images.guild_banner(self.id, self.banner, **kwargs)


_GuildWidgetSettings_fields = {
    'enabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    )
}


class GuildWidgetSettings(_types.Object[_protocols.GuildWidgetSettings], fields = _GuildWidgetSettings_fields):

    """
    |dsrc| :ddoc:`Guild Widget Settings Structure </resources/guild#guild-widget-settings-object-guild-widget-settings-structure>`
    """

    enabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['enabled']
    )
    """
    |dsrc| **enabled**
    """
    channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """


_GuildWidget_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'instant_invite': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'channels': vessel.SetField(
        create = lambda path, data: _types.Collection(Channel, data)
    ),
    'members': vessel.SetField(
        create = lambda path, data: _types.Collection(User, data)
    ),
    'presence_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    )
}


class GuildWidget(_types.Object[_protocols.GuildWidget], fields = _GuildWidget_fields):

    """
    |dsrc| :ddoc:`Guild Widget Structure </resources/guild#guild-widget-object-guild-widget-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    instant_invite: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['instant_invite']
    )
    """
    |dsrc| **instant_invite**
    """
    channels: _types.Collection['Channel'] = vessel.GetField(
        select = lambda root: root['channels']
    )
    """
    |dsrc| **channels**
    """
    members: _types.Collection['User'] = vessel.GetField(
        select = lambda root: root['members']
    )
    """
    |dsrc| **members**
    """
    presence_count: _types.Integer = vessel.GetField(
        select = lambda root: root['presence_count']
    )
    """
    |dsrc| **presence_count**
    """


_GuildMember_fields = {
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'nick': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'avatar': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'roles': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'joined_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'premium_since': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'deaf': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'mute': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'flags': vessel.SetField(
        create = lambda path, data: _enums.GuildMemberFlags(data)
    ),
    'pending': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'permissions': vessel.SetField(
        create = lambda path, data: _enums.Permissions(data)
    ),
    'communication_disabled_until': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    )
}


def _GuildMember_keyify(path, data):

    data_user_id = data['user']['id']

    return _types.Snowflake(data_user_id)

    
class GuildMember(_types.Object[_protocols.GuildMember], fields = _GuildMember_fields, keyify = _GuildMember_keyify):

    """
    |dsrc| :ddoc:`Guild Member Structure </resources/guild#guild-member-object-guild-member-structure>` | 
    :ddoc:`Guild Member Add Guild Member Add Extra Fields </topics/gateway-events#guild-member-add-guild-member-add-extra-fields>`
    """

    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    nick: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['nick']
    )
    """
    |dsrc| **nick**
    """
    avatar: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['avatar']
    )
    """
    |dsrc| **avatar**
    """
    roles: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['roles']
    )
    """
    |dsrc| **roles**
    """
    joined_at: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['joined_at']
    )
    """
    |dsrc| **joined_at**
    """
    premium_since: typing.Union[None, _types.ISO8601Timestamp] = vessel.GetField(
        select = lambda root: root['premium_since']
    )
    """
    |dsrc| **premium_since**
    """
    deaf: _types.Boolean = vessel.GetField(
        select = lambda root: root['deaf']
    )
    """
    |dsrc| **deaf**
    """
    mute: _types.Boolean = vessel.GetField(
        select = lambda root: root['mute']
    )
    """
    |dsrc| **mute**
    """
    flags: _enums.GuildMemberFlags = vessel.GetField(
        select = lambda root: root['flags']
    )
    """
    |dsrc| **flags**
    """
    pending: _types.Boolean = vessel.GetField(
        select = lambda root: root['pending']
    )
    """
    |dsrc| **pending**
    """
    permissions: _enums.Permissions = vessel.GetField(
        select = lambda root: root['permissions']
    )
    """
    |dsrc| **permissions**
    """
    communication_disabled_until: typing.Union[None, _types.ISO8601Timestamp] = vessel.GetField(
        select = lambda root: root['communication_disabled_until']
    )
    """
    |dsrc| **communication_disabled_until**
    """

    def avatar_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the avatar url.
        """

        return _images.guild_member_avatar(self.guild_id, self.user.id, self.avatar, **kwargs)

    # NOTE: docs do not specify "banner" for this object
    # def banner_url(self, **kwargs: typing.Unpack[_images._make_hint]):
    #     """
    #     Get the cover url.
    #     """
    #     return _images.guild_member_banner(self.guild_id, self.user.id, self.banner, **kwargs)


_Integration_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'enabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'syncing': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'role_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'enable_emoticons': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'expire_behavior': vessel.SetField(
        create = lambda path, data: _enums.IntegrationExpireBehaviorType(data)
    ),
    'expire_grace_period': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'account': vessel.SetField(
        create = lambda path, data: IntegrationAccount(data)
    ),
    'synced_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'subscriber_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'revoked': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'application': vessel.SetField(
        create = lambda path, data: Application(data)
    ),
    'scopes': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    )
}


class Integration(_types.Object[_protocols.Integration], fields = _Integration_fields):

    """
    |dsrc| :ddoc:`Integration Structure </resources/guild#integration-object-integration-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    type: _types.String = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    enabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['enabled']
    )
    """
    |dsrc| **enabled**
    """
    syncing: _types.Boolean = vessel.GetField(
        select = lambda root: root['syncing']
    )
    """
    |dsrc| **syncing**
    """
    role_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['role_id']
    )
    """
    |dsrc| **role_id**
    """
    enable_emoticons: _types.Boolean = vessel.GetField(
        select = lambda root: root['enable_emoticons']
    )
    """
    |dsrc| **enable_emoticons**
    """
    expire_behavior: _enums.IntegrationExpireBehaviorType = vessel.GetField(
        select = lambda root: root['expire_behavior']
    )
    """
    |dsrc| **expire_behavior**
    """
    expire_grace_period: _types.Integer = vessel.GetField(
        select = lambda root: root['expire_grace_period']
    )
    """
    |dsrc| **expire_grace_period**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    account: 'IntegrationAccount' = vessel.GetField(
        select = lambda root: root['account']
    )
    """
    |dsrc| **account**
    """
    synced_at: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['synced_at']
    )
    """
    |dsrc| **synced_at**
    """
    subscriber_count: _types.Integer = vessel.GetField(
        select = lambda root: root['subscriber_count']
    )
    """
    |dsrc| **subscriber_count**
    """
    revoked: _types.Boolean = vessel.GetField(
        select = lambda root: root['revoked']
    )
    """
    |dsrc| **revoked**
    """
    application: 'Application' = vessel.GetField(
        select = lambda root: root['application']
    )
    """
    |dsrc| **application**
    """
    scopes: _types.Collection[_types.String] = vessel.GetField(
        select = lambda root: root['scopes']
    )
    """
    |dsrc| **scopes**
    """


_IntegrationAccount_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class IntegrationAccount(_types.Object[_protocols.IntegrationAccount], fields = _IntegrationAccount_fields):

    """
    |dsrc| :ddoc:`Integration Account Structure </resources/guild#integration-account-object-integration-account-structure>`
    """

    id: _types.String = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """


_IntegrationApplication_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'icon': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'bot': vessel.SetField(
        create = lambda path, data: User(data)
    )
}


class IntegrationApplication(_types.Object[_protocols.IntegrationApplication], fields = _IntegrationApplication_fields):

    """
    |dsrc| :ddoc:`Integration Application Structure </resources/guild#integration-application-object-integration-application-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    icon: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['icon']
    )
    """
    |dsrc| **icon**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    bot: 'User' = vessel.GetField(
        select = lambda root: root['bot']
    )
    """
    |dsrc| **bot**
    """


_Ban_fields = {
    'reason': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    )
}


class Ban(_types.Object[_protocols.Ban], fields = _Ban_fields):

    """
    |dsrc| :ddoc:`Ban Structure </resources/guild#ban-object-ban-structure>`
    """

    reason: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['reason']
    )
    """
    |dsrc| **reason**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """


_WelcomeScreen_fields = {
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'welcome_channels': vessel.SetField(
        create = lambda path, data: _types.Collection(WelcomeScreenChannel, data)
    )
}


class WelcomeScreen(_types.Object[_protocols.WelcomeScreen], fields = _WelcomeScreen_fields):

    """
    |dsrc| :ddoc:`Welcome Screen Structure </resources/guild#welcome-screen-object-welcome-screen-structure>`
    """

    description: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    welcome_channels: _types.Collection['WelcomeScreenChannel'] = vessel.GetField(
        select = lambda root: root['welcome_channels']
    )
    """
    |dsrc| **welcome_channels**
    """


_WelcomeScreenChannel_fields = {
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'emoji_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'emoji_name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class WelcomeScreenChannel(_types.Object[_protocols.WelcomeScreenChannel], fields = _WelcomeScreenChannel_fields):

    """
    |dsrc| :ddoc:`Welcome Screen Channel Structure </resources/guild#welcome-screen-object-welcome-screen-channel-structure>`
    """

    channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    emoji_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['emoji_id']
    )
    """
    |dsrc| **emoji_id**
    """
    emoji_name: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['emoji_name']
    )
    """
    |dsrc| **emoji_name**
    """


_GuildOnboarding_fields = {
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'prompts': vessel.SetField(
        create = lambda path, data: _types.Collection(GuildOnboardingPrompt, data)
    ),
    'default_channel_ids': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'enabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class GuildOnboarding(_types.Object[_protocols.GuildOnboarding], fields = _GuildOnboarding_fields):

    """
    |dsrc| :ddoc:`Guild Onboarding Structure </resources/guild#guild-onboarding-object-guild-onboarding-structure>`
    """

    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    prompts: _types.Collection['GuildOnboardingPrompt'] = vessel.GetField(
        select = lambda root: root['prompts']
    )
    """
    |dsrc| **prompts**
    """
    default_channel_ids: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['default_channel_ids']
    )
    """
    |dsrc| **default_channel_ids**
    """
    enabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['enabled']
    )
    """
    |dsrc| **enabled**
    """


_GuildOnboardingPrompt_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.GuildOnboardingPromptType(data)
    ),
    'options': vessel.SetField(
        create = lambda path, data: _types.Collection(GuildOnboardingPromptOption, data)
    ),
    'title': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'single_select': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'required': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'in_onboarding': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class GuildOnboardingPrompt(_types.Object[_protocols.GuildOnboardingPrompt], fields = _GuildOnboardingPrompt_fields):

    """
    |dsrc| :ddoc:`Onboarding Prompt Structure </resources/guild#guild-onboarding-object-onboarding-prompt-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    type: _enums.GuildOnboardingPromptType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    options: _types.Collection['GuildOnboardingPromptOption'] = vessel.GetField(
        select = lambda root: root['options']
    )
    """
    |dsrc| **options**
    """
    title: _types.String = vessel.GetField(
        select = lambda root: root['title']
    )
    """
    |dsrc| **title**
    """
    single_select: _types.Boolean = vessel.GetField(
        select = lambda root: root['single_select']
    )
    """
    |dsrc| **single_select**
    """
    required: _types.Boolean = vessel.GetField(
        select = lambda root: root['required']
    )
    """
    |dsrc| **required**
    """
    in_onboarding: _types.Boolean = vessel.GetField(
        select = lambda root: root['in_onboarding']
    )
    """
    |dsrc| **in_onboarding**
    """


_GuildOnboardingPromptOption_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'channel_ids': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'role_ids': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Snowflake, data)
    ),
    'emoji': vessel.SetField(
        create = lambda path, data: Emoji(data)
    ),
    'title': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class GuildOnboardingPromptOption(_types.Object[_protocols.GuildOnboardingPromptOption], fields = _GuildOnboardingPromptOption_fields):

    """
    |dsrc| :ddoc:`Prompt Option Structure </resources/guild#guild-onboarding-object-prompt-option-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    channel_ids: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['channel_ids']
    )
    """
    |dsrc| **channel_ids**
    """
    role_ids: _types.Collection[_types.Snowflake] = vessel.GetField(
        select = lambda root: root['role_ids']
    )
    """
    |dsrc| **role_ids**
    """
    emoji: 'Emoji' = vessel.GetField(
        select = lambda root: root['emoji']
    )
    """
    |dsrc| **emoji**
    """
    title: _types.String = vessel.GetField(
        select = lambda root: root['title']
    )
    """
    |dsrc| **title**
    """
    description: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """


# SECTION: https://discord.com/developers/docs/resources/guild-scheduled-event


_GuildScheduledEvent_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'creator_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'scheduled_start_time': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'scheduled_end_time': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'privacy_level': vessel.SetField(
        create = lambda path, data: _enums.GuildScheduledEventPrivacyLevel(data)
    ),
    'status': vessel.SetField(
        create = lambda path, data: _enums.GuildScheduledEventStatus(data)
    ),
    'entity_type': vessel.SetField(
        create = lambda path, data: _enums.GuildScheduledEventEntityType(data)
    ),
    'entity_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'entity_metadata': vessel.SetField(
        create = lambda path, data: GuildScheduledEventEntityMetadata(data)
    ),
    'creator': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'user_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'image': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class GuildScheduledEvent(_types.Object[_protocols.GuildScheduledEvent], fields = _GuildScheduledEvent_fields):

    """
    |dsrc| :ddoc:`Guild Scheduled Event Structure </resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    creator_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['creator_id']
    )
    """
    |dsrc| **creator_id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    description: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    scheduled_start_time: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['scheduled_start_time']
    )
    """
    |dsrc| **scheduled_start_time**
    """
    scheduled_end_time: typing.Union[None, _types.ISO8601Timestamp] = vessel.GetField(
        select = lambda root: root['scheduled_end_time']
    )
    """
    |dsrc| **scheduled_end_time**
    """
    privacy_level: _enums.GuildScheduledEventPrivacyLevel = vessel.GetField(
        select = lambda root: root['privacy_level']
    )
    """
    |dsrc| **privacy_level**
    """
    status: _enums.GuildScheduledEventStatus = vessel.GetField(
        select = lambda root: root['status']
    )
    """
    |dsrc| **status**
    """
    entity_type: _enums.GuildScheduledEventEntityType = vessel.GetField(
        select = lambda root: root['entity_type']
    )
    """
    |dsrc| **entity_type**
    """
    entity_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['entity_id']
    )
    """
    |dsrc| **entity_id**
    """
    entity_metadata: typing.Union[None, 'GuildScheduledEventEntityMetadata'] = vessel.GetField(
        select = lambda root: root['entity_metadata']
    )
    """
    |dsrc| **entity_metadata**
    """
    creator: 'User' = vessel.GetField(
        select = lambda root: root['creator']
    )
    """
    |dsrc| **creator**
    """
    user_count: _types.Integer = vessel.GetField(
        select = lambda root: root['user_count']
    )
    """
    |dsrc| **user_count**
    """
    cover: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['image']
    )
    """
    |dsrc| **image**
    """

    def cover_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the cover url.
        """

        return _images.team_icon(self.id, self.cover, **kwargs)


_GuildScheduledEventEntityMetadata_fields = {
    'location': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class GuildScheduledEventEntityMetadata(_types.Object[_protocols.GuildScheduledEventEntityMetadata], fields = _GuildScheduledEventEntityMetadata_fields):

    """
    |dsrc| :ddoc:`Guild Scheduled Event Entity Metadata </resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata>`
    """

    location: _types.String = vessel.GetField(
        select = lambda root: root['location']
    )
    """
    |dsrc| **location**
    """


_GuildScheduledEventUser_fields = {
    'guild_scheduled_event_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'member': vessel.SetField(
        create = lambda path, data: GuildMember(data)
    )
}


class GuildScheduledEventUser(_types.Object[_protocols.GuildScheduledEventUser], fields = _GuildScheduledEventUser_fields):

    """
    |dsrc| :ddoc:`Guild Scheduled Event User Structure </resources/guild-scheduled-event#guild-scheduled-event-user-object-guild-scheduled-event-user-structure>`
    """

    guild_scheduled_event_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_scheduled_event_id']
    )
    """
    |dsrc| **guild_scheduled_event_id**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    member: 'GuildMember' = vessel.GetField(
        select = lambda root: root['member']
    )
    """
    |dsrc| **member**
    """


#   >o)
#   (_>
# SECTION: https://discord.com/developers/docs/resources/guild-template


_GuildTemplate_fields = {
    'code': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'usage_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'creator_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'creator': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'created_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'updated_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'source_guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'serialized_source_guild': vessel.SetField(
        create = lambda path, data: Guild(data)
    ),
    'is_dirty': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class GuildTemplate(_types.Object[_protocols.GuildTemplate], fields = _GuildTemplate_fields):

    """
    |dsrc| :ddoc:`Guild Template Structure </resources/guild-template#guild-template-object-guild-template-structure>`
    """

    code: _types.String = vessel.GetField(
        select = lambda root: root['code']
    )
    """
    |dsrc| **code**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    description: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    usage_count: _types.Integer = vessel.GetField(
        select = lambda root: root['usage_count']
    )
    """
    |dsrc| **usage_count**
    """
    creator_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['creator_id']
    )
    """
    |dsrc| **creator_id**
    """
    creator: 'User' = vessel.GetField(
        select = lambda root: root['creator']
    )
    """
    |dsrc| **creator**
    """
    created_at: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['created_at']
    )
    """
    |dsrc| **created_at**
    """
    updated_at: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['updated_at']
    )
    """
    |dsrc| **updated_at**
    """
    source_guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['source_guild_id']
    )
    """
    |dsrc| **source_guild_id**
    """
    serialized_source_guild: 'Guild' = vessel.GetField(
        select = lambda root: root['serialized_source_guild']
    )
    """
    |dsrc| **serialized_source_guild**
    """
    is_dirty: typing.Union[None, _types.Boolean] = vessel.GetField(
        select = lambda root: root['is_dirty']
    )
    """
    |dsrc| **is_dirty**
    """
    

# SECTION: https://discord.com/developers/docs/resources/invite


_Invite_fields = {
    'code': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'guild': vessel.SetField(
        create = lambda path, data: Guild(data)
    ),
    'channel': vessel.SetField(
        create = lambda path, data: Channel(data)
    ),
    'inviter': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'target_type': vessel.SetField(
        create = lambda path, data: _enums.InviteTargetType(data)
    ),
    'target_user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'target_application': vessel.SetField(
        create = lambda path, data: Application(data)
    ),
    'approximate_presence_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'approximate_member_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'expires_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'stage_instance': vessel.SetField(
        create = lambda path, data: InviteStageInstance(data)
    ),
    'guild_scheduled_event': vessel.SetField(
        create = lambda path, data: GuildScheduledEvent(data)
    ),
    'uses': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'max_uses': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'max_age': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'temporary': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'created_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    )
}


class Invite(_types.Object[_protocols.Invite], fields = _Invite_fields):

    """
    |dsrc| :ddoc:`Invite Structure </resources/invite#invite-object-invite-structure>` (:ddoc:`Invite Metadata Structure </resources/invite#invite-object-example-invite-object>`)
    """

    code: _types.String = vessel.GetField(
        select = lambda root: root['code']
    )
    """
    |dsrc| **code**
    """
    guild: 'Guild' = vessel.GetField(
        select = lambda root: root['guild']
    )
    """
    |dsrc| **guild**
    """
    channel: typing.Union[None, 'Channel'] = vessel.GetField(
        select = lambda root: root['channel']
    )
    """
    |dsrc| **channel**
    """
    inviter: 'User' = vessel.GetField(
        select = lambda root: root['inviter']
    )
    """
    |dsrc| **inviter**
    """
    target_type: _enums.InviteTargetType = vessel.GetField(
        select = lambda root: root['target_type']
    )
    """
    |dsrc| **target_type**
    """
    target_user: 'User' = vessel.GetField(
        select = lambda root: root['target_user']
    )
    """
    |dsrc| **target_user**
    """
    target_application: 'Application' = vessel.GetField(
        select = lambda root: root['target_application']
    )
    """
    |dsrc| **target_application**
    """
    approximate_presence_count: _types.Integer = vessel.GetField(
        select = lambda root: root['approximate_presence_count']
    )
    """
    |dsrc| **approximate_presence_count**
    """
    approximate_member_count: _types.Integer = vessel.GetField(
        select = lambda root: root['approximate_member_count']
    )
    """
    |dsrc| **approximate_member_count**
    """
    expires_at: typing.Union[None, _types.ISO8601Timestamp] = vessel.GetField(
        select = lambda root: root['expires_at']
    )
    """
    |dsrc| **expires_at**
    """
    stage_instance: 'InviteStageInstance' = vessel.GetField(
        select = lambda root: root['stage_instance']
    )
    """
    |dsrc| **stage_instance**
    """
    guild_scheduled_event: 'GuildScheduledEvent' = vessel.GetField(
        select = lambda root: root['guild_scheduled_event']
    )
    """
    |dsrc| **guild_scheduled_event**
    """
    uses: _types.Integer = vessel.GetField(
        select = lambda root: root['uses']
    )
    """
    |dsrc| **uses**
    """
    max_uses: _types.Integer = vessel.GetField(
        select = lambda root: root['max_uses']
    )
    """
    |dsrc| **max_uses**
    """
    max_age: _types.Integer = vessel.GetField(
        select = lambda root: root['max_age']
    )
    """
    |dsrc| **max_age**
    """
    temporary: _types.Boolean = vessel.GetField(
        select = lambda root: root['temporary']
    )
    """
    |dsrc| **temporary**
    """
    created_at: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: root['created_at']
    )
    """
    |dsrc| **created_at**
    """
    

_InviteStageInstance_fields = {
    'members': vessel.SetField(
        create = lambda path, data: _types.Collection(GuildMember, data)
    ),
    'participant_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'speaker_count': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'topic': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class InviteStageInstance(_types.Object[_protocols.InviteStageInstance], fields = _InviteStageInstance_fields):

    """
    |dsrc| :ddoc:`Invite Stage Instance Structure </resources/invite#invite-stage-instance-object-invite-stage-instance-structure>`
    """

    members: _types.Collection['GuildMember'] = vessel.GetField(
        select = lambda root: root['members']
    )
    """
    |dsrc| **members**
    """
    participant_count: _types.Integer = vessel.GetField(
        select = lambda root: root['participant_count']
    )
    """
    |dsrc| **participant_count**
    """
    speaker_count: _types.Integer = vessel.GetField(
        select = lambda root: root['speaker_count']
    )
    """
    |dsrc| **speaker_count**
    """
    topic: _types.String = vessel.GetField(
        select = lambda root: root['topic']
    )
    """
    |dsrc| **topic**
    """


# SECTION: https://discord.com/developers/docs/resources/stage-instance


_StageInstance_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'topic': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'privacy_level': vessel.SetField(
        create = lambda path, data: _enums.StageInstancePrivacyLevel(data)
    ),
    'discoverable_disabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'guild_scheduled_event_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    )
}


class StageInstance(_types.Object[_protocols.StageInstance], fields = _StageInstance_fields):

    """
    |dsrc| :ddoc:`Stage Instance Structure </resources/stage-instance#stage-instance-object-stage-instance-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    channel_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    topic: _types.String = vessel.GetField(
        select = lambda root: root['topic']
    )
    """
    |dsrc| **topic**
    """
    privacy_level: _enums.StageInstancePrivacyLevel = vessel.GetField(
        select = lambda root: root['privacy_level']
    )
    """
    |dsrc| **privacy_level**
    """
    discoverable_disabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['discoverable_disabled']
    )
    """
    |dsrc| **discoverable_disabled**
    """
    guild_scheduled_event_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['guild_scheduled_event_id']
    )
    """
    |dsrc| **guild_scheduled_event_id**
    """


# SECTION: https://discord.com/developers/docs/resources/sticker


_Sticker_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'pack_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'tags': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'asset': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.StickerType(data)
    ),
    'format_type': vessel.SetField(
        create = lambda path, data: _enums.StickerFormatType(data)
    ),
    'available': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'sort_value': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    )
}


class Sticker(_types.Object[_protocols.Sticker], fields = _Sticker_fields):

    """
    |dsrc| :ddoc:`Sticker Structure </resources/sticker#sticker-object-sticker-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    pack_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['pack_id']
    )
    """
    |dsrc| **pack_id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    description: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    tags: _types.String = vessel.GetField(
        select = lambda root: root['tags']
    )
    """
    |dsrc| **tags**
    """
    asset: _types.String = vessel.GetField(
        select = lambda root: root['asset']
    )
    """
    |dsrc| **asset**
    """
    type: _enums.StickerType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    format_type: _enums.StickerFormatType = vessel.GetField(
        select = lambda root: root['format_type']
    )
    """
    |dsrc| **format_type**
    """
    available: _types.Boolean = vessel.GetField(
        select = lambda root: root['available']
    )
    """
    |dsrc| **available**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    sort_value: _types.Integer = vessel.GetField(
        select = lambda root: root['sort_value']
    )
    """
    |dsrc| **sort_value**
    """

    def image_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the icon url.
        """

        return _images.sticker(self.id, **kwargs)


_StickerPack_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'stickers': vessel.SetField(
        create = lambda path, data: _types.Collection(Sticker, data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'sku_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'cover_sticker_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'description': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'banner_asset_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    )
}


class StickerPack(_types.Object[_protocols.StickerPack], fields = _StickerPack_fields):

    """
    |dsrc| :ddoc:`Sticker Pack Structure </resources/sticker#sticker-pack-object-sticker-pack-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    stickers: _types.Collection['Sticker'] = vessel.GetField(
        select = lambda root: root['stickers']
    )
    """
    |dsrc| **stickers**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    sku_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['sku_id']
    )
    """
    |dsrc| **sku_id**
    """
    cover_sticker_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['cover_sticker_id']
    )
    """
    |dsrc| **cover_sticker_id**
    """
    description: _types.String = vessel.GetField(
        select = lambda root: root['description']
    )
    """
    |dsrc| **description**
    """
    banner_asset_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['banner_asset_id']
    )
    """
    |dsrc| **banner_asset_id**
    """

    def banner_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the icon url.
        """

        return _images.sticker_pack_banner(self.id, self.banner_asset_id, **kwargs)


# SECTION: https://discord.com/developers/docs/resources/user


_User_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'username': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'discriminator': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'avatar': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'bot': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'system': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'mfa_enabled': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'banner': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'accent_color': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'locale': vessel.SetField(
        create = lambda path, data: _enums.Locale(data)
    ),
    'verified': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'email': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'flags': vessel.SetField(
        create = lambda path, data: _enums.UserFlags(data)
    ),
    'premium_type': vessel.SetField(
        create = lambda path, data: _enums.UserPremiumType(data)
    ),
    'public_flags': vessel.SetField(
        create = lambda path, data: _enums.UserFlags(data)
    )
}


class User(_types.Object[_protocols.User], fields = _User_fields):

    """
    |dsrc| :ddoc:`User Structure </resources/user#user-object-user-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    username: _types.String = vessel.GetField(
        select = lambda root: root['username']
    )
    """
    |dsrc| **username**
    """
    discriminator: _types.String = vessel.GetField(
        select = lambda root: root['discriminator']
    )
    """
    |dsrc| **discriminator**
    """
    avatar: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['avatar']
    )
    """
    |dsrc| **avatar**
    """
    bot: _types.Boolean = vessel.GetField(
        select = lambda root: root['bot']
    )
    """
    |dsrc| **bot**
    """
    system: _types.Boolean = vessel.GetField(
        select = lambda root: root['system']
    )
    """
    |dsrc| **system**
    """
    mfa_enabled: _types.Boolean = vessel.GetField(
        select = lambda root: root['mfa_enabled']
    )
    """
    |dsrc| **mfa_enabled**
    """
    banner: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['banner']
    )
    """
    |dsrc| **banner**
    """
    accent_color: typing.Union[None, _types.Integer] = vessel.GetField(
        select = lambda root: root['accent_color']
    )
    """
    |dsrc| **accent_color**
    """
    locale: _enums.Locale = vessel.GetField(
        select = lambda root: root['locale']
    )
    """
    |dsrc| **locale**
    """
    verified: _types.Boolean = vessel.GetField(
        select = lambda root: root['verified']
    )
    """
    |dsrc| **verified**
    """
    email: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['email']
    )
    """
    |dsrc| **email**
    """
    flags: _enums.UserFlags = vessel.GetField(
        select = lambda root: root['flags']
    )
    """
    |dsrc| **flags**
    """
    premium_type: _enums.UserPremiumType = vessel.GetField(
        select = lambda root: root['premium_type']
    )
    """
    |dsrc| **premium_type**
    """
    public_flags: _enums.UserFlags = vessel.GetField(
        select = lambda root: root['public_flags']
    )
    """
    |dsrc| **public_flags**
    """

    def mention(self):

        """
        Get the mention.
        """

        return _mentions.user(self.id)
    
    def banner_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the banner url.
        """

        return _images.guild_banner(self.id, self.banner, **kwargs)

    def avatar_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the avatar url.
        """

        return _images.user_avatar(self.id, self.avatar, **kwargs)


_Connection_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'revoked': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'integrations': vessel.SetField(
        create = lambda path, data: _types.Collection(Integration, data)
    ),
    'verified': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'friend_sync': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'show_activity': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'two_way_link': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'visibility': vessel.SetField(
        create = lambda path, data: _enums.ConnectionVisibilityType(data)
    )
}


class Connection(_types.Object[_protocols.Connection], fields = _Connection_fields):

    """
    |dsrc| :ddoc:`Connection Structure </resources/user#connection-object-connection-structure>`
    """

    id: _types.String = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    type: _types.String = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    revoked: _types.Boolean = vessel.GetField(
        select = lambda root: root['revoked']
    )
    """
    |dsrc| **revoked**
    """
    integrations: _types.Collection['Integration'] = vessel.GetField(
        select = lambda root: root['integrations']
    )
    """
    |dsrc| **integrations**
    """
    verified: _types.Boolean = vessel.GetField(
        select = lambda root: root['verified']
    )
    """
    |dsrc| **verified**
    """
    friend_sync: _types.Boolean = vessel.GetField(
        select = lambda root: root['friend_sync']
    )
    """
    |dsrc| **friend_sync**
    """
    show_activity: _types.Boolean = vessel.GetField(
        select = lambda root: root['show_activity']
    )
    """
    |dsrc| **show_activity**
    """
    two_way_link: _types.Boolean = vessel.GetField(
        select = lambda root: root['two_way_link']
    )
    """
    |dsrc| **two_way_link**
    """
    visibility: _enums.ConnectionVisibilityType = vessel.GetField(
        select = lambda root: root['visibility']
    )
    """
    |dsrc| **visibility**
    """


_ApplicationRoleConnection_fields = {
    'platform_name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'platform_username': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'metadata': vessel.SetField(
        create = lambda path, data: {
            _types.String(data_key): ApplicationRoleConnectionMetadata(data_val) for data_key, data_val in data.items()
        }
    )
}


class ApplicationRoleConnection(_types.Object[_protocols.ApplicationRoleConnection], fields = _ApplicationRoleConnection_fields):

    """
    |dsrc| :ddoc:`Application Role Connection Structure </resources/user#application-role-connection-object-application-role-connection-structure>`
    """

    platform_name: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['platform_name']
    )
    """
    |dsrc| **platform_name**
    """
    platform_username: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['platform_username']
    )
    """
    |dsrc| **platform_username**
    """
    metadata: dict[_types.String, 'ApplicationRoleConnectionMetadata'] = vessel.GetField(
        select = lambda root: root['metadata']
    )
    """
    |dsrc| **metadata**
    """


# SECTION: https://discord.com/developers/docs/resources/voice


_VoiceState_fields = {
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'user_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'member': vessel.SetField(
        create = lambda path, data: GuildMember(data)
    ),
    'session_id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'deaf': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'mute': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'self_deaf': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'self_mute': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'self_stream': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'self_video': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'suppress': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'request_to_speak_timestamp': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    )
}


class VoiceState(_types.Object[_protocols.VoiceState], fields = _VoiceState_fields):

    """
    |dsrc| :ddoc:`Voice State Structure </resources/voice#voice-state-object-voice-state-structure>`
    """

    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    user_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['user_id']
    )
    """
    |dsrc| **user_id**
    """
    member: 'GuildMember' = vessel.GetField(
        select = lambda root: root['member']
    )
    """
    |dsrc| **member**
    """
    session_id: _types.String = vessel.GetField(
        select = lambda root: root['session_id']
    )
    """
    |dsrc| **session_id**
    """
    deaf: _types.Boolean = vessel.GetField(
        select = lambda root: root['deaf']
    )
    """
    |dsrc| **deaf**
    """
    mute: _types.Boolean = vessel.GetField(
        select = lambda root: root['mute']
    )
    """
    |dsrc| **mute**
    """
    self_deaf: _types.Boolean = vessel.GetField(
        select = lambda root: root['self_deaf']
    )
    """
    |dsrc| **self_deaf**
    """
    self_mute: _types.Boolean = vessel.GetField(
        select = lambda root: root['self_mute']
    )
    """
    |dsrc| **self_mute**
    """
    self_stream: _types.Boolean = vessel.GetField(
        select = lambda root: root['self_stream']
    )
    """
    |dsrc| **self_stream**
    """
    self_video: _types.Boolean = vessel.GetField(
        select = lambda root: root['self_video']
    )
    """
    |dsrc| **self_video**
    """
    suppress: _types.Boolean = vessel.GetField(
        select = lambda root: root['suppress']
    )
    """
    |dsrc| **suppress**
    """
    request_to_speak_timestamp: typing.Union[None, _types.ISO8601Timestamp] = vessel.GetField(
        select = lambda root: root['request_to_speak_timestamp']
    )
    """
    |dsrc| **request_to_speak_timestamp**
    """


_VoiceRegion_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'optimal': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'deprecated': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'custom': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class VoiceRegion(_types.Object[_protocols.VoiceRegion], fields = _VoiceRegion_fields):

    """
    |dsrc| :ddoc:`Voice Region Structure </resources/voice#voice-region-object-voice-region-structure>`
    """

    id: _types.String = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    optimal: _types.Boolean = vessel.GetField(
        select = lambda root: root['optimal']
    )
    """
    |dsrc| **optimal**
    """
    deprecated: _types.Boolean = vessel.GetField(
        select = lambda root: root['deprecated']
    )
    """
    |dsrc| **deprecated**
    """
    custom: _types.Boolean = vessel.GetField(
        select = lambda root: root['custom']
    )
    """
    |dsrc| **custom**
    """


# SECTION: https://discord.com/developers/docs/resources/webhook


_Webhook_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.WebhookType(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'channel_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'avatar': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'token': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'source_guild': vessel.SetField(
        create = lambda path, data: Guild(data)
    ),
    'source_channel': vessel.SetField(
        create = lambda path, data: Channel(data)
    ),
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class Webhook(_types.Object[_protocols.Webhook], fields = _Webhook_fields):

    """
    |dsrc| :ddoc:`Webhook Structure </resources/webhook#webhook-object-webhook-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    type: _enums.WebhookType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    guild_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    channel_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['channel_id']
    )
    """
    |dsrc| **channel_id**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    name: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    avatar: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['avatar']
    )
    """
    |dsrc| **avatar**
    """
    token: _types.String = vessel.GetField(
        select = lambda root: root['token']
    )
    """
    |dsrc| **token**
    """
    application_id: typing.Union[None, _types.Snowflake] = vessel.GetField(
        select = lambda root: root['application_id']
    )
    """
    |dsrc| **application_id**
    """
    source_guild: 'Guild' = vessel.GetField(
        select = lambda root: root['source_guild']
    )
    """
    |dsrc| **source_guild**
    """
    source_channel: 'Channel' = vessel.GetField(
        select = lambda root: root['source_channel']
    )
    """
    |dsrc| **source_channel**
    """
    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """


# SECTION: https://discord.com/developers/docs/topics/gateway-events


_Presence_fields = {
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'status': vessel.SetField(
        create = lambda path, data: _enums.StatusType(data)
    ),
    'activities': vessel.SetField(
        create = lambda path, data: _types.Collection(Activity, data)
    ),
    'client_status': vessel.SetField(
        create = lambda path, data: ClientStatus(data)
    )
}


def _Presence_keyify(path, data):

    user_id = data['user']['id']

    return _types.Snowflake(user_id)


class Presence(_types.Object[_protocols.Presence], fields = _Presence_fields, keyify = _Presence_keyify):

    """
    |dsrc| :ddoc:`Presence Update Presence Update Event Fields </topics/gateway-events#presence-update-presence-update-event-fields>`
    """

    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['guild_id']
    )
    """
    |dsrc| **guild_id**
    """
    status: _enums.StatusType = vessel.GetField(
        select = lambda root: root['status']
    )
    """
    |dsrc| **status**
    """
    activities: _types.Collection['Activity'] = vessel.GetField(
        select = lambda root: root['activities']
    )
    """
    |dsrc| **activities**
    """
    client_status: 'ClientStatus' = vessel.GetField(
        select = lambda root: root['client_status']
    )
    """
    |dsrc| **client_status**
    """


_ClientStatus_fields = {
    'desktop': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'mobile': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'web': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class ClientStatus(_types.Object[_protocols.ClientStatus], fields = _ClientStatus_fields):

    """
    |dsrc| :ddoc:`</topics/gateway-events#client-status-object>`
    """

    desktop: _types.String = vessel.GetField(
        select = lambda root: root['desktop']
    )
    """
    |dsrc| **desktop**
    """
    mobile: _types.String = vessel.GetField(
        select = lambda root: root['mobile']
    )
    """
    |dsrc| **mobile**
    """
    web: _types.String = vessel.GetField(
        select = lambda root: root['web']
    )
    """
    |dsrc| **web**
    """


_Activity_fields = {
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.ActivityType(data)
    ),
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'created_at': vessel.SetField(
        create = lambda path, data: _types.Timestamp(data)
    ),
    'timestamps': vessel.SetField(
        create = lambda path, data: ActivityTimestamps(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'details': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'state': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'emoji': vessel.SetField(
        create = lambda path, data: Emoji(data)
    ),
    'party': vessel.SetField(
        create = lambda path, data: ActivityParty(data)
    ),
    'assets': vessel.SetField(
        create = lambda path, data: ActivityAssets(data)
    ),
    'secrets': vessel.SetField(
        create = lambda path, data: ActivitySecrets(data)
    ),
    'instance': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'flags': vessel.SetField(
        create = lambda path, data: _enums.ActivityFlags(data)
    ),
    'buttons': vessel.SetField(
        create = lambda path, data: _types.Collection(ActivityButton, data)
    )
}


class Activity(_types.Object[_protocols.Activity], fields = _Activity_fields):

    """
    |dsrc| :ddoc:`Activity Structure </topics/gateway-events#activity-object-activity-structure>`
    """

    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    type: _enums.ActivityType = vessel.GetField(
        select = lambda root: root['type']
    )
    """
    |dsrc| **type**
    """
    url: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """
    created_at: _types.Timestamp = vessel.GetField(
        select = lambda root: root['created_at']
    )
    """
    |dsrc| **created_at**
    """
    timestamps: 'ActivityTimestamps' = vessel.GetField(
        select = lambda root: root['timestamps']
    )
    """
    |dsrc| **timestamps**
    """
    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['application_id']
    )
    """
    |dsrc| **application_id**
    """
    details: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['details']
    )
    """
    |dsrc| **details**
    """
    state: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['state']
    )
    """
    |dsrc| **state**
    """
    emoji: typing.Union[None, 'Emoji'] = vessel.GetField(
        select = lambda root: root['emoji']
    )
    """
    |dsrc| **emoji**
    """
    party: 'ActivityParty' = vessel.GetField(
        select = lambda root: root['party']
    )
    """
    |dsrc| **party**
    """
    assets: 'ActivityAssets' = vessel.GetField(
        select = lambda root: root['assets']
    )
    """
    |dsrc| **assets**
    """
    secrets: 'ActivitySecrets' = vessel.GetField(
        select = lambda root: root['secrets']
    )
    """
    |dsrc| **secrets**
    """
    instance: _types.Boolean = vessel.GetField(
        select = lambda root: root['instance']
    )
    """
    |dsrc| **instance**
    """
    flags: _enums.ActivityFlags = vessel.GetField(
        select = lambda root: root['flags']
    )
    """
    |dsrc| **flags**
    """
    buttons: _types.Collection['ActivityButton'] = vessel.GetField(
        select = lambda root: root['buttons']
    )
    """
    |dsrc| **buttons**
    """


_ActivityTimestamps_fields = {
    'start': vessel.SetField(
        create = lambda path, data: _types.Timestamp(data)
    ),
    'end': vessel.SetField(
        create = lambda path, data: _types.Timestamp(data)
    )
}


class ActivityTimestamps(_types.Object[_protocols.ActivityTimestamps], fields = _ActivityTimestamps_fields):

    """
    |dsrc| :ddoc:`Activity Timestamps </topics/gateway-events#activity-object-activity-timestamps>`
    """

    start: _types.Timestamp = vessel.GetField(
        select = lambda root: root['start']
    )
    """
    |dsrc| **start**
    """
    end: _types.Timestamp = vessel.GetField(
        select = lambda root: root['end']
    )
    """
    |dsrc| **end**
    """


_ActivityParty_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'size': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.Integer, data)
    )
}


class ActivityParty(_types.Object[_protocols.ActivityParty], fields = _ActivityParty_fields):

    """
    |dsrc| :ddoc:`Activity Party </topics/gateway-events#activity-object-activity-party>`
    """

    id: _types.String = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    size: _types.Collection[_types.Integer] = vessel.GetField(
        select = lambda root: root['size']
    )
    """
    |dsrc| **size**
    """


_ActivityAssets_fields = {
    'large_image': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'large_text': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'small_image': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'small_text': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class ActivityAssets(_types.Object[_protocols.ActivityAssets], fields = _ActivityAssets_fields):

    """
    |dsrc| :ddoc:`Activity Assets </topics/gateway-events#activity-object-activity-assets>`
    """

    large_image: _types.String = vessel.GetField(
        select = lambda root: root['large_image']
    )
    """
    |dsrc| **large_image**
    """
    large_text: _types.String = vessel.GetField(
        select = lambda root: root['large_text']
    )
    """
    |dsrc| **large_text**
    """
    small_image: _types.String = vessel.GetField(
        select = lambda root: root['small_image']
    )
    """
    |dsrc| **small_image**
    """
    small_text: _types.String = vessel.GetField(
        select = lambda root: root['small_text']
    )
    """
    |dsrc| **small_text**
    """


_ActivitySecrets_fields = {
    'join': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'spectate': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'match': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class ActivitySecrets(_types.Object[_protocols.ActivitySecrets], fields = _ActivitySecrets_fields):

    """
    |dsrc| :ddoc:`Activity Secrets </topics/gateway-events#activity-object-activity-secrets>`
    """

    join: _types.String = vessel.GetField(
        select = lambda root: root['join']
    )
    """
    |dsrc| **join**
    """
    spectate: _types.String = vessel.GetField(
        select = lambda root: root['spectate']
    )
    """
    |dsrc| **spectate**
    """
    match: _types.String = vessel.GetField(
        select = lambda root: root['match']
    )
    """
    |dsrc| **match**
    """


_ActivityButton_fields = {
    'label': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'url': vessel.SetField(
        create = lambda path, data: _types.String(data)
    )
}


class ActivityButton(_types.Object[_protocols.ActivityButton], fields = _ActivityButton_fields):

    """
    |dsrc| :ddoc:`Activity Buttons </topics/gateway-events#activity-object-activity-buttons>`
    """

    label: _types.String = vessel.GetField(
        select = lambda root: root['label']
    )
    """
    |dsrc| **label**
    """
    url: _types.String = vessel.GetField(
        select = lambda root: root['url']
    )
    """
    |dsrc| **url**
    """


_Role_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'color': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'hoist': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'icon': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'unicode_emoji': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'position': vessel.SetField(
        create = lambda path, data: _types.Integer(data)
    ),
    'permissions': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'managed': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'mentionable': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'tags': vessel.SetField(
        create = lambda path, data: RoleTags(data)
    )
}


class Role(_types.Object[_protocols.Role], fields = _Role_fields):

    """
    |dsrc| :ddoc:`Role Structure </topics/permissions#role-object-role-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    color: _types.Integer = vessel.GetField(
        select = lambda root: root['color']
    )
    """
    |dsrc| **color**
    """
    hoist: _types.Boolean = vessel.GetField(
        select = lambda root: root['hoist']
    )
    """
    |dsrc| **hoist**
    """
    icon: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['icon']
    )
    """
    |dsrc| **icon**
    """
    unicode_emoji: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['unicode_emoji']
    )
    """
    |dsrc| **unicode_emoji**
    """
    position: _types.Integer = vessel.GetField(
        select = lambda root: root['position']
    )
    """
    |dsrc| **position**
    """
    permissions: _types.String = vessel.GetField(
        select = lambda root: root['permissions']
    )
    """
    |dsrc| **permissions**
    """
    managed: _types.Boolean = vessel.GetField(
        select = lambda root: root['managed']
    )
    """
    |dsrc| **managed**
    """
    mentionable: _types.Boolean = vessel.GetField(
        select = lambda root: root['mentionable']
    )
    """
    |dsrc| **mentionable**
    """
    tags: 'RoleTags' = vessel.GetField(
        select = lambda root: root['tags']
    )
    """
    |dsrc| **tags**
    """

    def mention(self):

        """
        Get the mention.
        """

        return _mentions.role(self.id)
    
    def icon_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the icon url.
        """

        return _images.team_icon(self.id, self.icon, **kwargs)


_RoleTags_fields = {
    'bot_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'integration_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'premium_subscriber': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'subscription_listing_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'available_for_purchase': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    ),
    'guild_connections': vessel.SetField(
        create = lambda path, data: _types.Boolean(data)
    )
}


class RoleTags(_types.Object[_protocols.RoleTags], fields = _RoleTags_fields):

    """
    |dsrc| :ddoc:`Role Tags Structure </topics/permissions#role-object-role-tags-structure>`
    """

    bot_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['bot_id']
    )
    """
    |dsrc| **bot_id**
    """
    integration_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['integration_id']
    )
    """
    |dsrc| **integration_id**
    """
    # NOTE: null
    premium_subscriber: _types.Boolean = vessel.GetField(
        select = lambda root: root['premium_subscriber']
    )
    """
    |dsrc| **premium_subscriber**
    """
    subscription_listing_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['subscription_listing_id']
    )
    """
    |dsrc| **subscription_listing_id**
    """
    # NOTE: null
    available_for_purchase: _types.Boolean = vessel.GetField(
        select = lambda root: root['available_for_purchase']
    )
    """
    |dsrc| **available_for_purchase**
    """
    # NOTE: null
    guild_connections: _types.Boolean = vessel.GetField(
        select = lambda root: root['guild_connections']
    )
    """
    |dsrc| **guild_connections**
    """


_Team_fields = {
    'icon': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data),
        unique = True
    ),
    'members': vessel.SetField(
        create = lambda path, data: _types.Collection(TeamMember, data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'owner_user_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    )
}


class Team(_types.Object[_protocols.Team], fields = _Team_fields):

    """
    |dsrc| :ddoc:`Data Models Team Object </topics/teams#data-models-team-object>`
    """

    icon: typing.Union[None, _types.String] = vessel.GetField(
        select = lambda root: root['icon']
    )
    """
    |dsrc| **icon**
    """
    id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['id']
    )
    """
    |dsrc| **id**
    """
    members: _types.Collection['TeamMember'] = vessel.GetField(
        select = lambda root: root['members']
    )
    """
    |dsrc| **members**
    """
    name: _types.String = vessel.GetField(
        select = lambda root: root['name']
    )
    """
    |dsrc| **name**
    """
    owner_user_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['owner_user_id']
    )
    """
    |dsrc| **owner_user_id**
    """

    def image_url(self, **kwargs: typing.Unpack[_images._make_hint]):

        """
        Get the image url.
        """

        return _images.team_icon(self.id, self.icon, **kwargs)


_TeamMember_fields = {
    'membership_state': vessel.SetField(
        create = lambda path, data: _enums.TeamMemberMembershipState(data)
    ),
    'permissions': vessel.SetField(
        create = lambda path, data: _types.Collection(_types.String, data)
    ),
    'team_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'user': vessel.SetField(
        create = lambda path, data: User(data)
    )
}


class TeamMember(_types.Object[_protocols.TeamMember], fields = _TeamMember_fields):

    """
    |dsrc| :ddoc:`Data Models Team Member Object </topics/teams#data-models-team-member-object>`
    """

    membership_state: _enums.TeamMemberMembershipState = vessel.GetField(
        select = lambda root: root['membership_state']
    )
    """
    |dsrc| **membership_state**
    """
    permissions: _types.Collection[_types.String] = vessel.GetField(
        select = lambda root: root['permissions']
    )
    """
    |dsrc| **permissions**
    """
    team_id: _types.Snowflake = vessel.GetField(
        select = lambda root: root['team_id']
    )
    """
    |dsrc| **team_id**
    """
    user: 'User' = vessel.GetField(
        select = lambda root: root['user']
    )
    """
    |dsrc| **user**
    """


_SKU_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.SKUType(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'name': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'slug': vessel.SetField(
        create = lambda path, data: _types.String(data)
    ),
    'flags': vessel.SetField(
        create = lambda path, data: _enums.SKUFlags(data)
    )
}


class SKU(_types.Object[_protocols.SKU], fields = _SKU_fields):

    """
    |dsrc| :ddoc:`SKU Structure </monetization/skus#sku-object-sku-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: ['id']
    )
    type: _enums.SKUType = vessel.GetField(
        select = lambda root: ['type']
    )
    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: ['application_id']
    )
    name: _types.String = vessel.GetField(
        select = lambda root: ['name']
    )
    slug: _types.String = vessel.GetField(
        select = lambda root: ['slug']
    )
    flags: _enums.SKUFlags = vessel.GetField(
        select = lambda root: ['flags']
    )


_Entitlement_fields = {
    'id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'sku_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'application_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'user_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    ),
    'type': vessel.SetField(
        create = lambda path, data: _enums.EntitlementType(data)
    ),
    'deleted': vessel.SetField(
        create = lambda path, data: data
    ),
    'starts_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'ends_at': vessel.SetField(
        create = lambda path, data: _types.ISO8601Timestamp(data)
    ),
    'guild_id': vessel.SetField(
        create = lambda path, data: _types.Snowflake(data)
    )
}


class Entitlement(_types.Object[_protocols.Entitlement], fields = _Entitlement_fields):

    """
    |dsrc| :ddoc:`Entitlement Structure </monetization/entitlements#entitlement-object-entitlement-structure>`
    """

    id: _types.Snowflake = vessel.GetField(
        select = lambda root: _types.Snowflake(root['id'])
    )
    sku_id: _types.Snowflake = vessel.GetField(
        select = lambda root: _types.Snowflake(root['sku_id'])
    )
    application_id: _types.Snowflake = vessel.GetField(
        select = lambda root: _types.Snowflake(root['application_id'])
    )
    user_id: _types.Snowflake = vessel.GetField(
        select = lambda root: _types.Snowflake(root['user_id'])
    )
    type = _enums.EntitlementType = vessel.GetField(
        select = lambda root: _enums.EntitlementType(root['type'])
    )
    deleted: _types.Boolean = vessel.GetField(
        select = lambda path, data: _types.Boolean(data)
    )
    starts_at: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: _types.ISO8601Timestamp(root['starts_at'])
    )
    ends_at: _types.ISO8601Timestamp = vessel.GetField(
        select = lambda root: _types.ISO8601Timestamp(root['ends_at'])
    )
    guild_id: _types.Snowflake = vessel.GetField(
        select = lambda root: _types.Snowflake(root['guild_id'])
    )