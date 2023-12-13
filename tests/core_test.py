from collatz.core import collatz_basic, collatz_recursive, batch_runner


class TestCollatzBasic:
    def test_15(self, seq_15):
        expected = seq_15
        actual = collatz_basic(15)
        assert actual == expected

    def test_16(self, seq_16):
        expected = seq_16
        actual = collatz_basic(16)
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


def test_batch_runner(seq_15, seq_16):
    expected = [seq_15, seq_16]
    actual = batch_runner(collatz_basic, [15, 16])

    assert actual == expected
