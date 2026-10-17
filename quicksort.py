"""In-place deterministic and randomized Quicksort using Lomuto partitioning.

Both functions mutate the supplied list and return None, like list.sort().
Recurse on the smaller partition and iterate over the larger one to bound
call-stack space by O(log n), including quadratic-time input cases.
"""
from random import Random
from typing import MutableSequence, TypeVar

T = TypeVar('T')


def partition(values: MutableSequence[T], low: int, high: int) -> int:
    """Place the last element at its final index in inclusive [low, high].

    During scanning, values[low:i] <= pivot and values[i:j] > pivot.
    Afterward the pivot separates a <= region from a > region.
    Requires 0 <= low <= high < len(values).
    """
    pivot = values[high]
    i = low
    for j in range(low, high):
        if values[j] <= pivot:
            values[i], values[j] = values[j], values[i]
            i += 1
    values[i], values[high] = values[high], values[i]
    return i


def _sort(values: MutableSequence[T], low: int, high: int,
          rng: Random | None) -> None:
    while low < high:
        if rng is not None:
            # randrange excludes its upper bound; high + 1 includes high.
            pivot_index = rng.randrange(low, high + 1)
            values[pivot_index], values[high] = values[high], values[pivot_index]
        p = partition(values, low, high)
        # Each actual recursive call receives at most half the active elements.
        if p - low < high - p:
            _sort(values, low, p - 1, rng)
            low = p + 1
        else:
            _sort(values, p + 1, high, rng)
            high = p - 1


def quicksort(values: MutableSequence[T]) -> None:
    """Sort ascending with the last element as a deterministic pivot.

    Time: best/average Theta(n log n), worst Theta(n^2).
    Average assumes a uniformly random permutation of distinct keys.
    Auxiliary space: O(log n) worst-case stack; O(1) partition workspace.
    """
    _sort(values, 0, len(values) - 1, None)


def randomized_quicksort(values: MutableSequence[T], *,
                         rng: Random | None = None) -> None:
    """Sort ascending with a uniform random pivot in every active subarray.

    With distinct keys, expected time is Theta(n log n) for any fixed input;
    worst time is Theta(n^2). This two-way partition remains quadratic on
    all-equal input. Supply Random(seed) for reproducible experiments.
    """
    if rng is None:
        rng = Random()
    _sort(values, 0, len(values) - 1, rng)


if __name__ == '__main__':
    source = [10, 7, 8, 9, 1, 5, 5, -2]
    print('Input:', source)
    for name, sort in [('Deterministic', quicksort),
                       ('Randomized', randomized_quicksort)]:
        values = source.copy()
        sort(values)
        print(f'{name}: {values}')
