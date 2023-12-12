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


def collatz_recursive(n: int, seq: list) -> (int, List[int]):
    """
    A recursive Collatz conjecture function


    Parameters
    ----------
    n: int
        Our starting number
    seq: List[Int]
        The Collatz sequence that we have traversed up to this point.

    Returns
    -------
    history: list[int]
        The path it taken to get to one.

    """

    if n == 1:
        return n, seq
    elif (n % 2) == 0:
        n = int(n / 2)
        seq.append(n)
        return collatz_recursive(n, seq)
    else:
        n = int(n * 3 + 1)
        seq.append(n)
        return collatz_recursive(n, seq)
