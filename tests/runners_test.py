from collatz.core import collatz_looping, collatz_looping_with_lookup
from collatz.runners import batch_runner, batch_runner_with_lookup


def test_batch_runner(seq_15, seq_16):
    expected = [seq_15, seq_16]
    actual = batch_runner(collatz_looping, [15, 16])

    assert actual == expected


def test_batch_runner_with_lookup(seq_15, seq_16):
    expected = {8: [8, 4, 2, 1], 15: seq_15, 16: seq_16}

    actual = batch_runner_with_lookup(
        collatz_looping_with_lookup, batch=[15, 16], seq_log={8: [8, 4, 2, 1]}
    )

    assert actual == expected
