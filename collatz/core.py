def collatz_basic(n: int) -> list(int):
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

    history = []

    while n != 1:
        if n % 2 == 0:
            n /= 2
        else:
            n += 3 * n + 1

        history.append(n)

    return history
