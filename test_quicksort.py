"""Correctness, partition-invariant, and recursion safety checks."""
import itertools
import random
import unittest
from quicksort import partition, quicksort, randomized_quicksort


class QuicksortTests(unittest.TestCase):
    def check_both(self, source):
        for kind in ('deterministic', 'randomized'):
            with self.subTest(kind=kind, source=source[:10], size=len(source)):
                values = list(source)
                identity = id(values)
                result = (quicksort(values) if kind == 'deterministic' else
                          randomized_quicksort(values, rng=random.Random(42)))
                self.assertEqual(values, sorted(source))
                self.assertIsNone(result)
                self.assertEqual(id(values), identity)

    def test_edge_cases(self):
        for source in ([], [1], [2, 1], [1, 2], [7]*30,
                       [-5, 0, -1, 8, -5], ['z', 'a', 'b', 'a']):
            self.check_both(source)

    def test_exhaustive_small_duplicate_arrays(self):
        for size in range(7):
            for source in itertools.product((-1, 0, 1), repeat=size):
                self.check_both(source)

    def test_random_arrays(self):
        rng = random.Random(31415)
        for _ in range(100):
            self.check_both([rng.randrange(-100, 101)
                             for _ in range(rng.randrange(501))])

    def test_ordered_above_default_recursion_limit(self):
        # A naive two-branch recursive last-pivot sort would exceed the limit.
        for source in (list(range(2000)), list(range(1999, -1, -1))):
            self.check_both(source)

    def test_partition_invariant_and_subarray_boundaries(self):
        rng = random.Random(27)
        for _ in range(100):
            middle = [rng.randrange(10) for _ in range(20)]
            values = [-999] + middle + [999]
            pivot = values[20]
            p = partition(values, 1, 20)
            self.assertEqual(values[p], pivot)
            self.assertTrue(all(x <= pivot for x in values[1:p]))
            self.assertTrue(all(x > pivot for x in values[p+1:21]))
            self.assertEqual(sorted(values[1:21]), sorted(middle))
            self.assertEqual((values[0], values[-1]), (-999, 999))


if __name__ == '__main__':
    unittest.main(verbosity=2)
