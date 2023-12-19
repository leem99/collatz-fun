import os
import time
import mlflow
from typing import Callable
from collatz.runners import write_seq_log


def timer(
    collatz_func: Callable,
    runner: Callable,
    verbose: bool = True,
    with_mlflow: bool = False,
    batch_start: int = 1,
    batch_end: int = 1_000_000,
    write_path: str = None,
    clear_previous: bool = False,
):
    batch = range(batch_start, batch_end + 1)

    # clear out previous results
    if clear_previous:
        os.system(f"rm -rf {write_path}/*")

    start = time.time()
    seq_log = runner(collatz_func, batch)

    if write_path is not None:
        write_seq_log(seq_log, write_path)

    finish = time.time()
    total_seconds = finish - start

    if verbose:
        print(f"total_seconds: {total_seconds}")

    if with_mlflow is True:
        with mlflow.start_run(run_name=collatz_func.__name__):
            mlflow.log_metric("total_seconds", total_seconds)

    return total_seconds
