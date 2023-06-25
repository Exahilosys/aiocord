Core
====

The core mechanisms for using all of the library's components collaboratively.

client
------

.. automodule:: aiocord.client

events
------

.. automodule:: aiocord.events

enums
-----

.. automodule:: aiocord.enums

utils
-----

.. automodule:: aiocord.utils

widget
------

.. automodule:: aiocord.widget

vendor
------

Starting
`````````

Installing the library attaches a script to your terminal.

To use it, create an example ``blep/__init__.py`` file (relative imports are allowed). 

.. note::
    See :func:`aiocord.widget.load` and :func:`aiocord.widget.drop` for further details.

Then, simply run:

.. code-block:: bash

    aiocord --token <TOKEN> start blep

Executing will create a client, connect to the gateway and begin listening to any events defined.

Updating
````````

Defining interaction callbacks will do nothing unless you have created commands.

This can be achieved by creating a ``commands.json`` containing all desired commands. 

Then, simply run:

.. code-block:: bash

    aiocord --token <TOKEN> update commands

Executing will overwrite (delete/create/replace) the existing commands for the application.

Creating commands by hand can be cumbersome due to the complexity of the data required.

This can be eliviated using intellisense by creating a ``commands.py`` and defining a ``commands`` variable.

.. code-block:: python

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

Then, run the script as shown above. 

The ``.py`` file will be used to generate the ``.json`` file before continuing.

Internal
========

The internal mechanisms of the library.

When scoped functionality is desired, these may be used directly.

http
----

The REST part of the Discord API.

client
``````

.. automodule:: aiocord.http.client

routes
``````

.. automodule:: aiocord.http.routes

errors
``````

.. automodule:: aiocord.http.errors

gateway
-------

The :ddoc:`Gateway </topics/gateway>` part of the Discord API.

client
``````

.. automodule:: aiocord.gateway.client

errors
``````

.. automodule:: aiocord.gateway.errors

voice
-----

The :ddoc:`Voice </topics/voice-connections>` part of the Discord API.

client
``````

.. automodule:: aiocord.voice.client

audio
`````

.. automodule:: aiocord.voice.audio

player
``````

.. automodule:: aiocord.voice.player

errors
``````

.. automodule:: aiocord.voice.errors

model
-----

All forms of data that may be encountered while interacting Discord API.

types
`````

All types found within more complex objects.

.. automodule:: aiocord.model.types

enums
`````

All enumerations found within more complex objects.

.. automodule:: aiocord.model.enums

protocols
`````````

All data models that may be sent or received.

These can be used directly when formulating request payloads.

.. automodule:: aiocord.model.protocols

objects
```````

Dynamic versions of models that may be updated at any point.

These will be found in responses or cached during live connections. 

.. automodule:: aiocord.model.objects

mentions
````````

:ddoc:`Message Formatting </reference#message-formatting-formats>` using basic types.

.. automodule:: aiocord.model.mentions

images
``````

:ddoc:`Image Formatting </reference#image-formatting-cdn-endpoints>` using basic types.

.. automodule:: aiocord.model.images

