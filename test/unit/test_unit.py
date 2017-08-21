'''
This module is the generic unittesting for the Collector/Sequence classes.

This test must ensure that the following conventions are supported:

    * foo%d.jpg
    * foo.%d.jpg
    * foo.v%d.%d.jpg
    * foo_v%d.%d.jpg

Where "%d" can have any padding.
'''
import pytest
import sequencer
import os

resources = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'resources'))


# Python 3.x
def lrange(*args):
    return list(range(*args))


def seq(head, tail, padding, frames):
    sequence_ = []
    for i in frames:
        sequence_.append('%s%s%s' % (head, str(i).zfill(padding), tail))

    return sequence_


INGEST_PARMS = [
    [seq('foo', '.bar', 0, range(10)), 'foo', (0, 9), '.bar'],
    [seq('foo.', '.bar', 0, range(10)), 'foo.', (0, 9), '.bar'],
    [seq('foo_v001', '.bar', 0, range(10)), 'foo_v001', (0, 9), '.bar'],
    [seq('foo_v1', '.bar', 0, range(10)), 'foo_v1', (0, 9), '.bar'],
    [seq('foo_v1', '.baz.bar', 0, range(10)), 'foo_v1', (0, 9), '.baz.bar'],
    [seq('foo_v1', '.baz_bar', 0, range(10)), 'foo_v1', (0, 9), '.baz_bar'],
]


@pytest.mark.parametrize('items,exp_head,exp_range,exp_tail', INGEST_PARMS)
def test_sequence_ingestion(items, exp_head, exp_range, exp_tail):

    seq_ = sequencer.collect(items)[0][0]

    assert seq_.head == exp_head
    assert (seq_.start(), seq_.end()) == exp_range
    assert seq_.tail == exp_tail


RANGE_PARMS = [
    [seq('foo', '.bar', 0, range(10)), 'offset', 10, (10, 19), None],
    [seq('foo', '.bar', 0, range(10, 20)), 'offset', -10, (0, 9), None],
    [seq('foo', '.bar', 0, range(10, 20)), 'set_start', 1, (1, 10), None],
    [seq('foo', '.bar', 0, range(10, 20)), 'set_end', 99, (90, 99), None],
    [seq('foo', '.bar', 0, range(10, 20)), 'set', range(10), (0, 9), None],
    [seq('foo', '.bar', 0, range(10)), 'set', range(11), (0, 10), None],
]


@pytest.mark.parametrize('items,action,value,exp_range,exp_raise', RANGE_PARMS)
def test_range_change(items, action, value, exp_range, exp_raise):
    seq_ = sequencer.collect(items)[0][0]

    try:
        if action == 'offset':
            seq_.offset(value)
        elif action == 'set_start':
            seq_.set_start(value)
        elif action == 'set_end':
            seq_.set_end(value)
        elif action == 'set':
            seq_.frames = value
    except Exception as e:
        if type(e) == exp_raise:
            return
        raise
    else:
        if exp_raise:
            raise ValueError('Did not raise %s' % exp_raise)

    assert (seq_.start(), seq_.end()) == exp_range


MISSING_PARMS = [
    [seq('foo', '.bar', 0, lrange(10) + lrange(15, 20)), [10, 11, 12, 13, 14]],
    [seq('foo_v001.', '.bar', 5, lrange(5) + lrange(6, 7)), [5]],
]


@pytest.mark.parametrize('items,exp_missing', MISSING_PARMS)
def test_missing_frames(items, exp_missing):
    seq_ = sequencer.collect(items)[0][0]

    assert seq_.missing == exp_missing


SEQ_ALTER_PARMS = [
    [
        seq('foo', '.bar', 0, range(10)),
        'weta', '.exr',
        seq('weta', '.exr', 0, range(10))
    ]
]


@pytest.mark.parametrize('items,new_head,new_tail,exp_items', SEQ_ALTER_PARMS)
def test_sequence_alter(items, new_head, new_tail, exp_items):
    seq_ = sequencer.collect(items)[0][0]

    seq_.head = new_head
    seq_.tail = new_tail

    assert list(seq_.get_mapping().keys()) == items
    assert list(seq_.get_mapping().values()) == exp_items


COLLECTOR_PARMS = [
    [['foo01.jpg'], 0, ['foo01.jpg']],
    [['myfile.txt'], 0, ['myfile.txt']],
    [['foo1.jpg', 'foo02.jpg'], 0, ['foo1.jpg', 'foo02.jpg']],
    [['foo1.jpg', 'foo2.jpg', 'foo03.jpg', 'foo04.jpg'], 2, []],
    [['foo01.jpg', 'foo02.jpg'], 1, []],
]


@pytest.mark.parametrize('items,exp_seq_count,exp_single', COLLECTOR_PARMS)
def test_collector_extra_files(items, exp_seq_count, exp_single):
    collection = sequencer.collect(items)
    assert len(collection[0]) == exp_seq_count
    assert all([x in collection[1] for x in exp_single])


FORMAT_PARMS = [
    [seq('foo_v001', '.bar', 0, range(10)), 'foo_v001%d.bar'],
    [seq('foo_v001.', '.bar', 0, range(10)), 'foo_v001.%d.bar'],
    [seq('foo_v001.', '.bar', 4, range(10)), 'foo_v001.%04d.bar'],
]


@pytest.mark.parametrize('items,exp_format', FORMAT_PARMS)
def test_format(items, exp_format):
    seq_ = sequencer.collect(items)[0][0]

    assert seq_.format() == exp_format


def test_dir_scan_01():
    seq_ = sequencer.collect(os.path.join(resources, 'seq_01'))[0][0]

    assert seq_.head == 'weta'
    assert seq_.tail == '.jpg'
    assert (seq_.start(), seq_.end()) == (1, 18)


def test_collect_with_path():
    seq_path = os.path.abspath(os.path.join(resources, 'seq_01'))
    seq_path = os.path.normpath(seq_path)
    iterable = [os.path.join(seq_path, x) for x in os.listdir(seq_path)]

    seq_ = sequencer.collect(iterable)[0][0]

    assert seq_.head == 'weta'
    assert seq_.tail == '.jpg'
    assert (seq_.start(), seq_.end()) == (1, 18)
    assert seq_.folder == seq_path
    assert seq_.format() == os.path.join(seq_path, 'weta%02d.jpg')
    assert list(seq_.get_mapping().keys()) == iterable


def test_different_folders():
    iterable = [
        '/foo/bar.001.jpg',
        '/foo/bar.002.jpg',
        '/baz/bar.003.jpg',
        '/baz/bar.004.jpg',
    ]

    seq_ = sequencer.collect(iterable)
    assert len(seq_[0]) == 2


def test_increment_range_mapping():

    sequence = sequencer.Sequence(
        head='foo.',
        tail='.jpg',
        frames=range(5),
        padding=3
    )
    expected = seq('foo.', '.jpg', 3, range(10))

    sequence.frames = range(10)

    assert list(sequence.get_mapping().keys()) == expected


def test_reset():
    sequence = sequencer.Sequence(
        head='foo.',
        tail='.jpg',
        frames=range(5),
        padding=3
    )
    sequence.frames = range(10)
    sequence.offset(10)
    sequence.head = 'bar.'
    sequence.tail = '.foo'
    sequence.padding = 10
    sequence.reset()

    assert sequence.head == 'foo.'
    assert sequence.tail == '.jpg'
    assert sequence.frames == lrange(5)
    assert sequence.padding == 3


def test_formatted_frames():
    sequence = sequencer.Sequence(
        head='foo.',
        tail='.jpg',
        frames=range(5),
        padding=3
    )

    assert sequence.formatted_frames() == seq('foo.', '.jpg', 3, range(5))
