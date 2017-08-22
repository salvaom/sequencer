[![Build Status](https://travis-ci.org/salvaom/sequencer.svg?branch=master)](https://travis-ci.org/salvaom/sequencer)

# Installation

On the root directory, run `pip install .` or `python setup.py install`. If it's a manual installation, you can also add the `source` directory to the environment variable `PYTHONPATH` to make it work.


# Building the docs

To build the docs, in the root directory run `python setup.py build_sphinx`. Depending on the build method (by default `html`) the built docs can be found in `docs/build/<type>`.


# Running tests

To run tests, in the root directory run `python setup.py test`


# Basic usage

To create a sequence object:

``` python
>>> import sequencer
>>> iterable = ['weta01.jpg', 'weta02.jpg', 'weta03.jpg']
>>> sequences, extra_files = sequencer.collect(iterable)
>>> sequences[0].head, sequences[0].padding, sequences[0].tail
('weta', 2, '.jpg')
```

If instead of an iterable `collect` is given a path to a directory, it will use the `os.listdir` function to retrieve the elements within.

Sequences can then be changed:

``` python
>>> sequence = sequences[0]
>>> sequence.offset(10)
>>> sequence.start(), sequence.end()
(11, 13)
>>> sequence.head = 'atwe.'
>>> sequence.format()
'atwe.%02d.jpg'
```

For advanced usage, please see the docs.


## Making a sequence continuous


``` python
from __future__ import print_function
import sequencer
import os
import shutil


# Source and target folders
source_dir = 'test/resources/seq_02'

# List the source files
source_files = [os.path.join(source_dir, x) for x in os.listdir(source_dir)]

# Collect the sequence
sequences = sequencer.collect(source_files)[0]

for seq in sequences:
    # Make it continuous
    seq.make_continuous()

    # Copy the files there
    for source, target in seq.get_mapping().items():
        if not os.path.isfile(target):
            print('Moving "%s" to "%s"' % (source, target))
            shutil.move(source, target)


```