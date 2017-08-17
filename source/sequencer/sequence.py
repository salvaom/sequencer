import logging

logger = logging.getLogger(__name__)


class Sequence(object):
    def __init__(self, head, frames, padding, tail):
        self._frames = []

        self.head = head
        self._orig_head = head

        self.frames = list(sorted(set(frames)))
        self._orig_frames = self.frames

        self.padding = padding
        self._orig_padding = padding

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

    def __repr__(self):
        return '<%s "%s%s%s" [%s-%s]>' % (
            __name__ + '.' + self.__class__.__name__,
            self.head,
            self._padding_format(),
            self.tail,
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
        self._frames = list(sorted(set(value)))
        self.missing = self.find_missing_in_range(self._frames)

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
        mapping = {}
        for index, frame in enumerate(self.frames):
            original = self._orig_head \
                + self._padding_format() % self._orig_frames[index] \
                + self._orig_tail

            dest = self.head \
                + self._padding_format() % frame \
                + self.tail

            mapping[original] = dest

        return mapping
