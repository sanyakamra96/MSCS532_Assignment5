# Assignment 5: Quicksort Implementation, Analysis, and Randomization

**Sanya Kamra**  
University of the Cumberlands  
MSCS 532 M70 — Algorithms and Data Structures  
October 17, 2026

## Overview

This project implements deterministic last-element-pivot Quicksort and randomized-pivot Quicksort in Python. Both use the same in-place Lomuto partition. The smaller partition is sorted recursively, and the larger partition is processed in a loop, guaranteeing O(log n) auxiliary stack space even on quadratic-time inputs.

## Run

Python 3.10 or later is required. The sorting implementation, tests, and benchmark use only the Python standard library.

From this directory:

```bash
python3 quicksort.py
python3 -m unittest -v
python3 benchmark.py
```

The benchmark runs five trials for each of five sizes and five distributions, producing 250 measured sorts. It overwrites the CSV files and environment metadata in `results/`. Exact elapsed times vary with hardware and system load. The submitted report describes the included original measurements.

For a quick run without replacing the submitted data:

```bash
python3 benchmark.py --sizes 250 500 1000 --trials 3 --output quick_results
```

To regenerate the figure (optional):

```bash
python3 -m pip install -r requirements-plot.txt
python3 plot_results.py
```

## API example

```python
from random import Random
from quicksort import quicksort, randomized_quicksort

values = [10, 7, 8, 9, 1, 5, 5, -2]
quicksort(values)  # Mutates the list; returns None.
assert values == [-2, 1, 5, 5, 7, 8, 9, 10]

other = [3, 1, 2]
randomized_quicksort(other, rng=Random(42))
assert other == [1, 2, 3]
```

## Files

| File | Purpose |
| --- | --- |
| `quicksort.py` | Both sorting functions, documented shared partition, and executable demonstration |
| `test_quicksort.py` | Five correctness test methods, including exhaustive small arrays and partition invariants |
| `benchmark.py` | Paired seeded experiments and CSV/metadata generation |
| `plot_results.py` | Recreates the measured runtime figure |
| `MSCS532_Assignment5_Report_Sanya_Kamra.docx` | Detailed implementation, theoretical analysis, measurements, discussion, and references |
| `results/raw_timings.csv` | All 250 measured sorts, input seeds, pivot seeds, and times |
| `results/summary.csv` | Median, minimum, maximum, and trial count for each condition |
| `results/environment.json` | Python version, platform, seeds, sizes, and timing method |
| `results/runtime_comparison.png` | Chart of measured distinct-key performance |
| `results/test_output.txt` | Captured successful unit-test run |
| `results/demo_output.txt` | Captured output from the demonstration |
| `results/benchmark_output.txt` | Captured benchmark progress and validation summary |

## Method

- Sizes: 250, 500, 1,000, 2,000, and 4,000.
- Distributions: random distinct permutations, sorted, reverse sorted, ten possible values, and all equal.
- Five paired trials per condition; three warmups per algorithm; algorithm order alternates each trial.
- `perf_counter_ns` measures sorting only. Generation, copying, RNG construction, and validation are excluded; random pivot draws during sorting are included.
- Base seed: 53205. Data and pivot seeds are recorded for every observation.
- Every measured result is checked against `sorted` outside the timed interval.
- Tests include all 1,093 arrays of lengths 0–6 over {-1, 0, 1} for both versions, 100 random arrays, sorted/reversed arrays of length 2,000, edge cases, and partition invariants.

## Findings

Medians for n = 4,000 on the recorded CPython 3.12.14 Linux x86_64 run:

| Input | Deterministic ms | Randomized ms |
| --- | ---: | ---: |
| Random distinct | 5.998 | 6.353 |
| Sorted | 695.364 | 5.664 |
| Reverse sorted | 621.111 | 7.250 |
| Ten values | 66.003 | 73.151 |
| All equal | 649.689 | 802.701 |

Randomization provided about 122.8× and 85.7× speedups on sorted and reverse-sorted data, respectively. It added overhead on random input, where last-element selection already has a random rank. The shared two-way partition degrades on equal keys; random pivot selection alone cannot repair that behavior.

## Complexity

| Property | Deterministic | Randomized |
| --- | --- | --- |
| Best time | Θ(n log n) | Θ(n log n) |
| Average/expected time with distinct keys | Θ(n log n), averaging uniformly random permutations | Θ(n log n), averaging uniform pivot choices for any fixed input |
| Worst time | Θ(n²) | Θ(n²) |
| All-equal input with this partition | Θ(n²) | Θ(n²) |
| Auxiliary stack in this implementation | O(log n) worst case | O(log n) worst case |
| Partition workspace | O(1) | O(1) |
| Stable | No | No |

The usual two-recursive-branch implementation can consume O(n) stack in the worst case. This implementation avoids that through smaller-partition recursion; it does not eliminate quadratic time. Benchmark copies are additional O(n) harness allocations, not sorting workspace.

## Assignment coverage

| Requirement | Location |
| --- | --- |
| Deterministic Python Quicksort with partitioning and recursion | `quicksort.py`: `partition`, `_sort`, `quicksort` |
| Random pivot from the current subarray | `quicksort.py`: `_sort`, `randomized_quicksort` |
| Best, average, worst time and space analysis | Report sections on time, randomization, and memory |
| Comparisons across sizes and distributions | `benchmark.py`, raw/summary CSV files, Tables 1–2 and Figure 1 in report |
| Interpretation tied to theory | Report sections on growth patterns and duplicates |
| Run instructions and findings | This README |

## References

Massachusetts Institute of Technology. (2005). *Lecture 4: Quicksort, randomized algorithms*. MIT OpenCourseWare. https://ocw.mit.edu/courses/6-046j-introduction-to-algorithms-sma-5503-fall-2005/resources/lecture-4-quicksort-randomized-algorithms/

Sedgewick, R., & Wayne, K. (n.d.). *2.3 Quicksort* [Lecture slides]. Princeton University. https://algs4.cs.princeton.edu/lectures/keynote/23Quicksort.pdf

## Reproduce the completed verification (optional)

From the project folder, run:

```bash
python3 quicksort.py
python3 -m unittest -v
python3 benchmark.py --output my_results
```

The demonstration produces `[-2, 1, 5, 5, 7, 8, 9, 10]` for both algorithms. The tests end with `OK`; the benchmark ends with `Validated all 250 timed sorts.` New timings are saved separately in `my_results/`.

Appendix A contains recorded execution output; Appendix B contains reproduction instructions.

## Final submission

Submit this repository URL:

https://github.com/sanyakamra96/MSCS532_Assignment5
