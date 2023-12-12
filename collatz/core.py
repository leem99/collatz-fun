from typing import List
import time


def collatz_basic(n: int) -> List[int]:
    """
    A basic while loop implementation of Collatz conjecture function.


    Parameters
    ----------
    n: int
        Our starting number

    Returns
    -------
    history: list[int]
        The path it taken to get to one.

    """

    history = [n]

    while n != 1:
        if (n % 2) == 0:
            n /= 2
        else:
            n = 3 * n + 1

        history.append(int(n))

    return history
