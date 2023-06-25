Examples
========

All ``aiocord`` terminal commands assume you either:

- Set the ``DISCORD_TOKEN`` environment variable
- Use the ``--token <TOKEN>`` flag before any subcommands 

Widgets
-------

Make a ``blep/__init__.py`` python package:

.. literalinclude:: examples/widget.py

.. note::
    Relative imports of package level are allowed.

.. note::
    Loading other modules using :func:`aiocord.widget.load` is allowed.

Then, run the following:

.. code-block:: bash

    aiocord start blep

Integration
-----------

Finer control over starting, loading, dropping and stopping.

.. literalinclude:: examples/control.py
    
Commands
--------

Make a ``commands.py`` python script and define a ``commands`` variable:

.. literalinclude:: examples/commands.py

Then, run the following:

.. code-block:: bash

    aiocord update commands

A ``commands.json`` will be created and the application's commands will be updated with its contents.

Interactions
------------

Naive Approach
``````````````

Creating a ``shop`` command routine for buying sweets and potentially gifting them.

.. literalinclude:: examples/interact.naive.py

Smart Approach
``````````````

Using the following:

- Funneling with :func:`aiocord.utils.interact`
- Returning :code:`response` in elligible functions

Trivializes the following:

- Managing :code:`custom_id`
- Waiting with :meth:`.client.Client.wait`
- Responding with :meth:`.client.Client.create_interaction_response`

Additionally, code organization and readability improve.

.. literalinclude:: examples/interact.smart.py
    :emphasize-lines: 13,21-24,39,53,61-64,81,90,106,134,159

.. note::
    Since :func:`.aiocord.utils.interact` only passes the event to the callback, :func:`functools.partial` is necessary for carrying information (such as :code:`stock` and :code:`item`) along the routine.

HTTP-Only
---------

Invoking HTTP routes without connecting to the gateway.

.. literalinclude:: examples/http.py
    :emphasize-lines: 5-6

Voice
-----

Joining a voice channel and playing music via a local file.

.. literalinclude:: examples/voice.file.py
    :emphasize-lines: 9,10,11

Audio data may be directly fed programatically.

.. literalinclude:: examples/voice.data.py
    :lines: 4-5,10-15

.. note::
    For **linux** and **macos**, ffmpeg can be installed with ``homebrew`` via :code:`brew install ffmpeg`.
    Since this creates a shell command, there is no need to specify the executable location.

    For **windows**, ``ffmpeg.exe`` must be on the system. It can be found `here <https://ffmpeg.org/download.html>`_. 
    To avoid having to specify the executable location with :code:`Audio(executable = ...)`, it can be added to the PATH.