from typing import List, Callable, Iterable


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


def collatz_recursive(n: int, seq: list = None) -> (int, List[int]):
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

    if seq is None:
        seq = [n]

    if n == 1:
        return seq
    elif (n % 2) == 0:
        n = int(n / 2)
        seq.append(n)
        return collatz_recursive(n, seq)
    else:
        n = int(n * 3 + 1)
        seq.append(n)
        return collatz_recursive(n, seq)


def batch_runner(func: Callable, batch: Iterable):
    """
    Run the Collatz sequence for a batch of numbers

    Parameters
    ----------
    func: Callable
        the function we will use to generate the Collatz sequence
    seq: Interable
        A list of values for which we want to compute the Collatz sequence

    Returns
    -------
    seq_list: List[List[int]]
        A list containing the Collatz sequence for each

    """

    seq_list: List[List[int]] = []
    for val in batch:
        seq_list.append(func(val))

    return seq_list
