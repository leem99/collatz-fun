import pytest
from typing import List


@pytest.fixture(scope="function", autouse=True)
def seq_16() -> List[int]:
    sequence = [16, 8, 4, 2, 1]

    return sequence


@pytest.fixture(scope="function", autouse=True)
def seq_15() -> List[int]:
    sequence = [15, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]

    return sequence
