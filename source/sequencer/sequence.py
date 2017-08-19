import collections
import logging

logger = logging.getLogger(__name__)


class Sequence(object):
    '''Represents a sequence of elements. The sequence is defined by 4
    variables:

    1. **Head**: The head is whatever comes before the number. For example, \
        in ``weta.01.jpg``, it would be ``weta``
    2. **Frames**: The list of frames that the sequence spans
    3. **Padding**: The zero padding of those frames
    4. **Tail**: The tail is whatever comes after the number. For example, in \
        ``weta.01.jpg``, it would be ``.jpg``

    The :obj:`Sequence` instance also remembers it's original data to easily
    create a mapping from the original to the a sequence.

    .. warning::

        If the frame range is changed with another bigger than the original
        frame range, this class will still attempt to get a mapping from the
        original, even if the original doest not have the frames in the
        mapping. Use with caution.

    Example:

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

    Args:
        head (str): Head of the sequence
        frames (list): List of frames the sequence contains
        padding (int): Frame padding
        tail (str): Tail of the sequence
    '''

    def __init__(self, head, frames, padding, tail):
        self._frames = []

        self._orig_head = head
        self._orig_frames = list(sorted(set(frames)))
        self._orig_padding = padding
        self._orig_tail = tail

        self.head = head
        self.frames = self._orig_frames
        self.padding = padding if padding > 1 else None
        self.tail = tail
        self.missing = self.find_missing_in_range(frames)

    @staticmethod
    def find_missing_in_range(iterable):
        '''Given a range of integers, return any holes in it.

        Args:
            iterable (iter): Integer range

        Returns:
            list: List of missing integers in the sequence
        '''
        missing = []
        for i in range(min(iterable), max(iterable) + 1):
            if i not in iterable:
                missing.append(i)

        return missing

    def __repr__(self):  # pragma: no cover
        return '<%s "%s" [%s-%s]>' % (
            __name__ + '.' + self.__class__.__name__,
            self.format(),
            self.start(),
            self.end()
        )

    def _padding_format(self):
        if self.padding:
            return '%' + str(self.padding).zfill(2) + 'd'
        return '%d'

    @property
    def frames(self):
        '''List of frames in the sequence'''
        return self._frames

    @frames.setter
    def frames(self, value):
        self._frames = list(sorted(set(value)))
        self.missing = self.find_missing_in_range(self._frames)

    def format(self):
        return '%s%s%s' % (
            self.head,
            self._padding_format(),
            self.tail
        )

    def reset(self):
        self.head = self._orig_head
        self.tail = self._orig_tail
        self.frames = self._orig_frames
        self.padding = self._orig_padding

    def start(self):
        return min(self.frames)

    def end(self):
        return max(self.frames)

    def offset(self, amount):
        self.frames = [x + amount for x in self.frames]

    def set_start(self, start):
        offset = start - self.start()
        self.offset(offset)

    def set_end(self, end):
        offset = end - self.end()
        self.offset(offset)

    def get_mapping(self):
        mapping = collections.OrderedDict()
        for index, frame in enumerate(self.frames):

            orig_len = len(self._orig_frames) - 1
            if index > orig_len:
                number = max(self._orig_frames) + (index - orig_len)
            else:
                number = self._orig_frames[index]

            original = self._orig_head \
                + self._padding_format() % number \
                + self._orig_tail

            dest = self.head \
                + self._padding_format() % frame \
                + self.tail

            mapping[original] = dest

        return mapping
