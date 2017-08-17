import re
import os
import collections
import logging
from pprint import pformat

from sequencer import sequence

logger = logging.getLogger(__name__)

# Python 3 compatibility
try:
    unicode
except NameError:
    unicode = str

COLLECTION_REGEX = re.compile(
    r'(?P<name>\D+(?P<version>\.?\_?v\d+)?[\.\_]?)'
    r'(?P<number>\d+)'
    r'(?P<tail>[\.\_]?\w+)?'
    r'(?P<ext>\.\w+)$'
)


def collect(iterable, collection_regex=None, minimum_instances=2):
    # Initial variables
    extra = []
    sequences = collections.defaultdict(list)
    collection_regex = collection_regex or COLLECTION_REGEX

    # If it's a path, listdir ir
    if isinstance(iterable, (str, unicode)) and os.path.isdir(iterable):
        iterable = os.listdir(iterable)

    for item in iterable:
        result = collection_regex.match(item)
        if not result:
            extra.append(item)
            continue

        res = result.groupdict()
        res = {x: _format_nones(y) for x, y in res.items()}

        # For a sequence to match, the ony difference must be the number,
        # the only exception to this should be different paddings in the same
        # sequence, but we'll take care of that later.
        sequence_id = res['name'] + res['version'] + res['tail'] + res['ext']
        sequences[sequence_id].append([item, res])

    # Discard round
    deferred_pop = []
    for sequence_id, sequence_items in sequences.items():

        # Discard condition #1: Alternating paddings
        all_numbers = [x[1]['number'] for x in sequence_items]
        is_padded = not all([len(str(int(x))) == len(x) for x in all_numbers])
        all_paddings = set([len(x) for x in all_numbers])

        if is_padded and len(all_paddings) > 1:
            logger.warn('Sequence "%s" has alternating padding' % sequence_id)

            deferred_pop.append(sequence_id)
            [extra.append(x[0]) for x in sequence_items]
            continue

        elif len(all_paddings) == 1:
            for i, _ in enumerate(sequence_items):
                sequences[sequence_id][i].append(int(list(all_paddings)[0]))
        else:
            for i, _ in enumerate(sequence_items):
                sequences[sequence_id][i].append(None)

        # Discard condition #2: less elements than the minimum
        if len(sequence_items) < minimum_instances:
            for orig, _ in sequence_items:
                extra.append(orig)

            continue

    for pop in deferred_pop:
        sequences.pop(pop)

    sequence_objs = []
    for sequence_id, sequence_items in sequences.items():
        original, data, padding = sequence_items[0]
        frames = [int(x[1]['number']) for x in sequence_items]

        sequence_ = sequence.Sequence(
            head=data['name'] + data['version'],
            frames=set(frames),
            padding=padding,
            tail=data['tail'] + data['ext']
        )
        sequence_objs.append(sequence_)

    return sequence_objs, extra


def _format_nones(item):
    return '' if item is None else item


if __name__ == '__main__':
    print collect(r'G:\Dropbox\projects\weta\sequencer\test\resources\seq_01')
