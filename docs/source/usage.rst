Usage
=====


Collecting a sequence
---------------------


.. code-block:: python

    >>> import sequencer
    >>> # feeding a folder
    ...
    >>> sequences, extra = sequencer.collect('test/resources/seq_01')
    >>> sequences
    [<sequencer.sequence.Sequence "weta%02d.jpg" [1-18]>]
    >>> sequences[0].start(), sequences[0].end()
    (1, 18)
    >>> # OR feeding an iterable
    ...
    >>> seq_ = ['foo.001.jpg', 'foo.002.jpg']
    >>> sequences, extra = sequencer.collect(seq_)
    >>> sequences
    [<sequencer.sequence.Sequence "foo.%03d.jpg" [1-2]>]
    >>> sequences[0].start(), sequences[0].end()
    (1, 2)


Creating a sequence
-------------------

.. code-block:: python

    >>> import sequencer
    >>> seq = sequencer.Sequence(head='atew.', tail='.jpg', padding=5, frames=range(1, 19), folder='/foo/bar')
    >>> repr(seq)
    '<sequencer.sequence.Sequence "/foo/bar/atew.%05d.jpg" [1-18]>'
    >>> seq.format()
    '\\foo\\bar\\atew.%05d.jpg'


Sequence attributes
-------------------

.. code-block:: python

    >>> import sequencer
    >>> seq = sequencer.Sequence(head='atew.', tail='.jpg', padding=5, frames=[1, 2, 5, 6], folder='/foo/bar')
    >>> seq.head
    'atew.'
    >>> seq.padding
    5
    >>> seq.frames
    [1, 2, 5, 6]
    >>> seq.tail
    '.jpg'
    >>> seq.folder
    '/foo/bar'
    >>> seq.missing
    [3, 4]
    >>> print '\n'.join(seq.formatted_frames())
    /foo/bar/atew.00001.jpg
    /foo/bar/atew.00002.jpg
    /foo/bar/atew.00005.jpg
    /foo/bar/atew.00006.jpg

For more information, please refer to :class:`sequencer.sequence.Sequence`.



Editing a sequence
------------------

.. code-block:: python

    >>> import sequencer
    >>> sequence = sequencer.Sequence(
    ... head='weta.', tail='.jpg', frames=[0, 1], padding=3)
    >>> sequence.frames
    [0, 1]
    >>> sequence.format()
    'weta.%03d.jpg'
    >>> sequence.padding = None
    >>> sequence.format()
    'weta.%d.jpg'
    >>> sequence.head = 'atew.'
    >>> sequence.format()
    'atew.%d.jpg'
    >>> sequence.offset(10)
    >>> sequence.frames
    [10, 11]
    >>> sequence.get_mapping()
    OrderedDict([('weta.0.jpg', 'atew.10.jpg'), ('weta.1.jpg', 'atew.11.jpg')])
    >>> sequence.frames = [1001, 1002, 1010]
    >>> sequence.make_continuous()
    >>> sequence.frames
    [1001, 1002, 1003]



Usage examples
--------------

Making a sequence continuous
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. literalinclude:: _static/make_continuous.py
    :emphasize-lines: 18


Shifting and copying an existing sequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: _static/sample_copy.py
    :emphasize-lines: 23