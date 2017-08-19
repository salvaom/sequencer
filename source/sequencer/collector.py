import re
import os
import collections
import logging

from sequencer import sequence

logger = logging.getLogger(__name__)

# Python 3 compatibility
try:
    unicode
except NameError:  # pragma: no cover
    unicode = str

COLLECTION_REGEX = re.compile(
    r'(?P<name>\D+?(?P<version>[\.\_]?v\d+)?[\.\_]?)'
    r'(?P<number>\d+)'
    r'(?P<tail>[\.\_]?\w+)?'
    r'(?P<ext>\.\w+)$'
)


def collect(iterable, collection_regex=None, minimum_instances=2):
    '''From either an iterable or a file path, attempts to detect all sequenced
    elements within the list and returns them as a
    :obj:`~sequencer.sequence.Sequence` object.

    Example:

        >>> import sequencer
        >>> sequences, extra = sequencer.collect('test/resources/seq_01')
        >>> sequences
        [<sequencer.sequence.Sequence "weta%02d.jpg" [1-18]>]
        >>> sequences[0].start(), sequences[0].end()
        (1, 18)

    Args:
        iterable (:obj:`iter`, :obj:`str`): Iterable to detect sequenced
            elements in. If a file path is passed as the argument, it will
            use `os.listdir` of that path as the element list.
        collection_regex (:obj:`str`, optional): If set, it will use the given
            regular expression to detect sequences in an iterable.

            .. warning::

                The regular expression **must** contain the following keys:
                ``name``, ``number``, ``tail`` and ``ext``

        minimum_instances (:obj:`int`, optional): Minimum number of matches in
            an element to be consider a sequence. Defaults to 2.

    Returns:
        tuple: A tuple with a list of all sequences found in the first index
        and a list of all files non-sequence related in the second index.

        Sequences are instances of :obj:`sequencer.sequence.Sequence` and the
        extra files are :obj:`str`

    '''
    # Initial variables
    extra = []
    sequences = collections.defaultdict(list)
    collection_regex = collection_regex or COLLECTION_REGEX

    # If it's a path, listdir it
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
        sequence_id = res['name'] + res['tail'] + res['ext']
        sequences[sequence_id].append([item, res])

    # Data digestion
    deferred_pop = []
    deferred_add = {}
    for sequence_id, sequence_items in sequences.items():

        # Check the paddings first
        all_numbers = [x[1]['number'] for x in sequence_items]
        is_padded = not all([len(str(int(x))) == len(x) for x in all_numbers])
        all_paddings = set([len(x) for x in all_numbers])

        # If it's padded but the paddings are different, we need to split in
        # subsequences
        if is_padded and len(all_paddings) > 1:
            subsequences = {}

            # All subsequences will have their original ID + the padding,
            # which should be enough to make them unique
            for item, result in sequence_items:
                key = str(len(result['number']))
                if key not in subsequences:
                    subsequences[key] = []

                subsequences[key].append([item, result, int(key)])

            for subsequence, data in subsequences.items():
                # Since we are a bit out of the loop here, the minimum check
                # has to be repeated here as well
                if len(data) < minimum_instances:
                    [extra.append(x[0]) for x in data]
                    continue

                deferred_add[sequence_id + subsequence] = data

            deferred_pop.append(sequence_id)

        # If all paddings match, put the padding
        elif len(all_paddings) == 1:
            for i, _ in enumerate(sequence_items):
                sequences[sequence_id][i].append(int(list(all_paddings)[0]))

        # If they don't we can assume they are not padded
        else:
            for i, _ in enumerate(sequence_items):
                sequences[sequence_id][i].append(None)

        # Discard condition: less elements than the minimum
        if len(sequence_items) < minimum_instances:
            [extra.append(x[0]) for x in sequence_items]
            deferred_pop.append(sequence_id)

    # You shall not delete indices on an iterable while iterating it
    for pop in deferred_pop:
        sequences.pop(pop)

    # Nor add them
    sequences.update(deferred_add)

    # And we can now build the sequences
    sequence_objs = []
    for sequence_id, sequence_items in sequences.items():
        original, data, padding = sequence_items[0]
        frames = [int(x[1]['number']) for x in sequence_items]

        sequence_ = sequence.Sequence(
            head=data['name'],
            frames=set(frames),
            padding=padding,
            tail=data['tail'] + data['ext']
        )
        sequence_objs.append(sequence_)

    return sequence_objs, extra


def _format_nones(item):
    return '' if item is None else item
