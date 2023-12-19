import os
from typing import Callable, Dict, Iterable, List
import ray
import pyarrow.parquet as pq
import pyarrow as pa
import multiprocessing


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


def batch_runner_with_lookup(
    func: Callable, batch: Iterable, seq_log: Dict[int, List[int]] = None
):
    """
    Run the Collatz sequence for a batch of numbers

    Parameters
    ----------
    func: Callable
        the function we will use to generate the Collatz sequence
    seq: Interable
        A list of values for which we want to compute the Collatz sequence
    seq_log: Dict[int, List[int]]
        A lookup of pre-commputed Collatz sequences

    Returns
    -------
    seq_log:  Dict[int, List[int]]
        A dictionary containing all of the computed Collatz sequences

    """

    if seq_log is None:
        seq_log = {}

    for val in batch:
        seq_log = func(val, seq_log)

    return seq_log


def read_seq_log(read_path: str) -> Dict[int, List[int]]:
    """
    Read the sequence log from a parquet file

    Parameters:
    -----------
    read_path: str
        The path to the parquet file containing the sequence log

    Returns:
    --------
    seq_log: Dict[int, List[int]]
        A dictionary containing all of the computed Collatz sequences
    """

    retry_count = 0
    max_retries = 10

    while retry_count < max_retries:
        try:
            seq_table = pq.read_table(read_path, use_threads=False)
            seq_log = {d["numbers"]: d["sequences"] for d in seq_table.to_pylist()}
            return seq_log
        except FileNotFoundError:
            seq_log = {}
            return seq_log
        except Exception as e:
            retry_count += 1
            print(
                f"Failed to read {read_path} on attempt {retry_count} of {max_retries}"
            )

    raise Exception(f"Failed to read {read_path} after {max_retries} retries")


def write_seq_log(seq_log: Dict[int, List[int]], write_path: str) -> None:
    """
    Write the sequence log to a parquet file

    Parameters:
    -----------
    seq_log: Dict[int, List[int]]
        A dictionary containing all of the computed Collatz sequences
    write_path: str
        The path to the parquet file containing the sequence log
    """

    numbers = pa.array(seq_log.keys())
    sequences = pa.array(seq_log.values())

    sequence_table = pa.Table.from_pydict({"numbers": numbers, "sequences": sequences})
    pq.write_table(sequence_table, write_path)


@ray.remote
def batch_runner_with_lookup_wrapper(
    func: Callable, batch: Iterable, read_path: str, write_path: str
):
    # read seq_log
    seq_log = read_seq_log(read_path)

    # Genearate next part of the sequence
    new_seq_log = batch_runner_with_lookup(func, batch, seq_log)

    # write seq_log
    write_seq_log(new_seq_log, write_path)


def run_distributed_collatz(
    func: Callable,
    start_val: int,
    end_val: int,
    batch_size: int,
    working_dir: str,
    data_path: str,
    max_workers: int = None,
    clear_previous: bool = False,
    local_mode: bool = False,
) -> None:
    # clear out previous results
    if clear_previous:
        os.system(f"rm -rf {data_path}/*")

    # make sure we kill previous session
    ray.shutdown()

    # initiate ray
    runtime_env = {
        "env_vars": {"PYTHONPATH": "$PYTHONPATH:collatz"},
        "working_dir": working_dir,
        "excludes": ["**/tests/**", "bin"],
    }
    ray.init(runtime_env=runtime_env, local_mode=local_mode)

    start_indicies = list(range(start_val, end_val, batch_size))

    # This is the amount of rows we distribute to each worker.
    if max_workers is None:
        max_workers = multiprocessing.cpu_count() - 1
        print(f"max_workers: {max_workers}")

    result_refs: list[ray.ObjectRef] = []

    for ix, i in enumerate(start_indicies):
        batch_start = i
        batch_end = batch_start + batch_size

        batch = range(batch_start, batch_end)

        read_path = data_path
        write_path = f"{data_path}/seq_log_{ix}.parquet"

        result_refs.append(
            batch_runner_with_lookup_wrapper.remote(func, batch, read_path, write_path)
        )

        while len(result_refs) > max_workers:
            finished, result_refs = ray.wait(result_refs, num_returns=1)
            print(f"Returned Sorted {len(finished)}, Waiting on {len(result_refs)}")
            ray.get(finished)

    unfinished = result_refs
    while unfinished:
        # Returns the first ObjectRef that is ready.
        finished, unfinished = ray.wait(unfinished, num_returns=1)
        print(f"Returned Sorted {len(finished)}, Waiting on {len(unfinished)}")
    ray.get(finished)

    print("done!")
    ray.shutdown()
