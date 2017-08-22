from __future__ import print_function
import sequencer
import os
import shutil


# Source folder
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
