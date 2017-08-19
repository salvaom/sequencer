import collections
import logging

logger = logging.getLogger(__name__)


class Sequence(object):
    def __init__(self, head, frames, padding, tail):
        self._frames = []

        self.head = head
        self._orig_head = head

        self._orig_frames = list(sorted(set(frames)))
        self.frames = self._orig_frames

        self.padding = padding if padding > 1 else None
        self._orig_padding = self.padding

        self.tail = tail
        self._orig_tail = tail

        self.missing = self.find_missing_in_range(frames)
        self._orig_missing = None

    @staticmethod
    def find_missing_in_range(iterable):
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
        return self._frames

    @frames.setter
    def frames(self, value):
        if len(value) > len(self._orig_frames):
            raise ValueError(
                'Frame count must match the original (%s frames)'
                % len(self._orig_frames)
            )

        self._frames = list(sorted(set(value)))
        self.missing = self.find_missing_in_range(self._frames)

    def format(self):
        return '%s%s%s' % (
            self.head,
            self._padding_format(),
            self.tail
        )

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
            original = self._orig_head \
                + self._padding_format() % self._orig_frames[index] \
                + self._orig_tail

            dest = self.head \
                + self._padding_format() % frame \
                + self.tail

            mapping[original] = dest

        return mapping
