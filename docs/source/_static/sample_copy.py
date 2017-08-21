from __future__ import print_function
import sequencer
import os
import shutil


# Source and target folders
source_dir = 'test/resources/seq_01'
target_dir = 'target'

# List the source files
source_files = [os.path.join(source_dir, x) for x in os.listdir(source_dir)]

# Collect the sequence
seq = sequencer.collect(source_files)[0][0]

# Create the target directory
if not os.path.isdir(target_dir):
    os.makedirs(target_dir)

# Change the folder and offset it 20 frames
seq.folder = target_dir
seq.set_start(1001)
seq.padding = 4
seq.head = seq.head + '.'

# Copy the files there
for source, target in seq.get_mapping().items():
    print('Copying "%s" to "%s"' % (source, target))
    shutil.copy2(source, target)
