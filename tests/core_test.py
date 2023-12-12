from collatz.core import collatz_basic


class TestCollatzBasic:
    def test_15(self, seq_15):
        expected = seq_15
        actual = collatz_basic(15)
        assert actual == expected

    def test_16(self, seq_16):
        expected = seq_16
        actual = collatz_basic(16)
        assert actual == expected
