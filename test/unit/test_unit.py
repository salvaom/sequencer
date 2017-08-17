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


def seq(head, tail, padding, frames):
    sequence_ = []
    for i in frames:
        sequence_.append('%s%s%s' % (head, str(i).zfill(padding), tail))

    return sequence_


# Parametrization for sequence ingestion
# 0:
SEQUENCE_INGEST_PARAMETERS = [
    [seq('foo', '.bar', 0, range(10)), 'foo', (0, 9), '.bar', None],
    [seq('foo.', '.bar', 0, range(10)), 'foo.', (0, 9), '.bar', None],
    [seq('foo_v001', '.bar', 0, range(10)), 'foo_v001', (0, 9), '.bar', None],
    [seq('foo_v1', '.bar', 0, range(10)), 'foo_v1', (0, 9), '.bar', None],
    [seq('foo_v1', '.baz.bar', 0, range(10)), 'foo_v1', (0, 9), '.baz.bar', None],
    [seq('foo_v1', '.baz_bar', 0, range(10)), 'foo_v1', (0, 9), '.baz_bar', None],
]


@pytest.mark.parametrize(
    "items,exp_head,exp_range,exp_tail,ex_raise",
    SEQUENCE_INGEST_PARAMETERS
)
def test_sequence_ingestion(items, exp_head, exp_range, exp_tail, ex_raise):

    if ex_raise:
        with pytest.raised(ex_raise):
            seq_ = sequencer.collect(items)[0][0]
    else:
        seq_ = sequencer.collect(items)[0][0]

    assert seq_.head == exp_head
    assert (seq_.start(), seq_.end()) == exp_range
    assert seq_.tail == exp_tail
