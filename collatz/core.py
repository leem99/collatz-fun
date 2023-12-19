from typing import List, Dict
from copy import copy


def collatz_looping(n: int) -> List[int]:
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
    seq: list[int]
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


# version where we take advantage of pre-computed history


def collatz_looping_with_lookup(
    n: int, seq_log: Dict[int, List[int]] = None
) -> List[int]:
    """
    A basic while loop implementation of Collatz conjecture function.

    Parameters
    ----------
    n: int
        Our starting number
    seq_log: Dict[int, List[int]]
        Collatz sequences that we have computed for other numbers.
        Once we hit a value in our lookup, we know the rest of the sequence.

    Returns
    -------
    sequence: list[int]
        The path it taken to get to one.
    seq_log: Dict[int, List[int]]
        Our lookup dictionary with the sequence for n added.
    """

    if seq_log is None:
        seq_log = {}

    input_n = copy(n)
    sequence = [n]

    while n != 1:
        n_seq = seq_log.get(n)
        if n_seq is not None:
            # once if n is our log, we can
            # just append the sequence for n
            # and we are done
            sequence += n_seq[1:]
            break

        if (n % 2) == 0:
            n //= 2
        else:
            n = 3 * n + 1

        sequence.append(n)

    seq_log[input_n] = sequence

    return seq_log
