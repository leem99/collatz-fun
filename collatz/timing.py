import time
import mlflow
from typing import Callable


def timer_1_million(
    collatz_func: Callable,
    runner: Callable,
    verbose: bool = True,
    with_mlflow: bool = False,
):
    batch = range(1, 1_000_001)

    start = time.time()
    runner(collatz_func, batch)
    finish = time.time()
    total_seconds = finish - start

    if verbose:
        print(f"total_seconds: {total_seconds}")

    if with_mlflow is True:
        with mlflow.start_run(run_name=collatz_func.__name__):
            mlflow.log_metric("total_seconds", total_seconds)

    return total_seconds
