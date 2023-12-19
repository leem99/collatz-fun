from collatz.core import (
    collatz_looping,
    collatz_looping_with_lookup,
    collatz_recursive,
)


class TestCollatzLooping:
    def test_15(self, seq_15):
        expected = seq_15
        actual = collatz_looping(15)
        assert actual == expected

    def test_16(self, seq_16):
        expected = seq_16
        actual = collatz_looping(16)
        assert actual == expected


class TestCollatzRecursive:
    def test_15(self, seq_15):
        expected = seq_15
        actual = collatz_recursive(15)
        assert actual == expected

    def test_16(self, seq_16):
        expected = seq_16
        actual = collatz_recursive(16)
        assert actual == expected


# Test code where we taked advantage of pre-computed history
class TestCollatzLoopingWithLookup:
    def test_15(self, seq_15):
        actual = collatz_looping_with_lookup(15)
        expected = {15: seq_15}
        assert actual == expected

    def test_16_without_helpful_lookup(self, seq_15, seq_16):
        seq_log = {15: seq_15}
        actual = collatz_looping_with_lookup(16, seq_log)
        expected = {15: seq_15, 16: seq_16}
        assert actual == expected

    def test_16_with_helpful_lookup(self, seq_15, seq_16):
        seq_log = {8: [8, 4, 2, 1], 15: seq_15}
        actual = collatz_looping_with_lookup(16, seq_log)
        expected = {8: [8, 4, 2, 1], 15: seq_15, 16: seq_16}
        assert actual == expected
