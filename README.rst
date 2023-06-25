A modern API wrapper for Discord.

Installation
------------

.. code-block:: bash
   
      pip install aiocord

Features
--------

- **Complete**: Implements the entirety of Discord's services.
- **Asynchronous**: Written in pure ``asyncio`` for native parallelism.
- **Modular**: Any component (such as HTTP) can be used in isolation.
- **Ergonomic**: Comes with extreme purpose-driven data reception and cacehing.
- **Interactive**: Supports slash-commands and related utilities out of the box.

Example
-------

Create a ``widget/__init__.py`` file.

.. code-block:: python

    import aiocord

    @aiocord.widget.callback(aiocord.events.CreateMessage)
    async def handle(info, event):
        if (message := event.message).author.id == info.client.cache.user.id:
            return
        await info.client.create_message(message.channel_id, content = f'{message.author.mention()} said {message.content}!')

And run the following in your terminal:

.. code-block:: bash

    aiocord --token <TOKEN> start widget

This is a simple example to get you started in seconds, but the library covers a vast wealth tools to fit any scenario.

Check out the `Documentation <https://aiocord.readthedocs.io>`_'s `Examples <https://aiocord.readthedocs.io/en/latest/pages/examples.html>`_ section for more, 
such as how to use `Commands <https://aiocord.readthedocs.io/en/latest/pages/examples.html#commands>`_ and `Interactions <https://aiocord.readthedocs.io/en/latest/pages/examples.html#interactions>`_.
