Welcome
-------

This library aims to offer a complete, intuitive and streamlined away for building Discord apps both quickly and at scale.

Installation
------------

.. code-block:: bash
   
      pip install aiocord

Quickstart
----------

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

Check out the :ref:`Examples` section for more and, when ready, explore :ref:`Core` to learn about the underlying mechanisms.

.. note::
    This documentation describes how the Discord API is implemented, **not** how it behaves. 
    
    There are links relevant parts of :ddoc:`Discord's Documentation </intro>`, for consulting as the main source of truth.

.. toctree::
    :hidden:

    pages/reference
    pages/examples