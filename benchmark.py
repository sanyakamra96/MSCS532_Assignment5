"""Paired seeded trials; input creation, copies and validation are not timed."""
import argparse
import csv
import json
import platform
import random
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter_ns
from quicksort import quicksort, randomized_quicksort

DISTRIBUTIONS = ('random', 'sorted', 'reverse', 'few_unique', 'all_equal')


def make_input(n, distribution, seed):
    rng = random.Random(seed)
    values = list(range(n))
    if distribution == 'random':
        rng.shuffle(values)
    elif distribution == 'reverse':
        values.reverse()
    elif distribution == 'few_unique':
        values = [rng.randrange(10) for _ in range(n)]
    elif distribution == 'all_equal':
        values = [7] * n
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sizes', nargs='+', type=int, default=[250, 500, 1000, 2000, 4000])
    parser.add_argument('--trials', type=int, default=5)
    parser.add_argument('--seed', type=int, default=53205)
    parser.add_argument('--output', type=Path, default=Path('results'))
    args = parser.parse_args()
    if args.trials < 1 or any(n < 2 for n in args.sizes):
        parser.error('trials must be positive and sizes must be at least 2')
    args.output.mkdir(parents=True, exist_ok=True)
    for _ in range(3):
        warm = make_input(200, 'random', args.seed)
        quicksort(warm.copy())
        randomized_quicksort(warm.copy(), rng=random.Random(args.seed))
    raw, summary = [], []
    for distribution_index, distribution in enumerate(DISTRIBUTIONS):
        for n in args.sizes:
            samples = {'deterministic': [], 'randomized': []}
            for trial in range(args.trials):
                data_seed = args.seed + distribution_index * 10000000 + n * 100 + trial
                pivot_seed = data_seed + 100000000
                source = make_input(n, distribution, data_seed)
                expected = sorted(source)
                order = ['deterministic', 'randomized']
                if trial % 2:
                    order.reverse()
                for name in order:
                    values = source.copy()
                    rng = random.Random(pivot_seed)
                    start = perf_counter_ns()
                    if name == 'deterministic':
                        quicksort(values)
                    else:
                        randomized_quicksort(values, rng=rng)
                    elapsed = (perf_counter_ns() - start) / 1000000
                    if values != expected:
                        raise AssertionError(f'Incorrect output: {name}, {distribution}, {n}')
                    samples[name].append(elapsed)
                    raw.append(dict(distribution=distribution, n=n, trial=trial+1,
                                    algorithm=name, data_seed=data_seed,
                                    pivot_seed=pivot_seed, elapsed_ms=elapsed))
            for name, times in samples.items():
                summary.append(dict(distribution=distribution, n=n, algorithm=name,
                                    median_ms=statistics.median(times), min_ms=min(times),
                                    max_ms=max(times), trials=args.trials))
            print(f'{distribution:11s} n={n:5d}  deterministic={statistics.median(samples["deterministic"]):9.3f} ms'
                  f'  randomized={statistics.median(samples["randomized"]):9.3f} ms', flush=True)
    for name, rows in [('raw_timings.csv', raw), ('summary.csv', summary)]:
        with (args.output / name).open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    metadata = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                    python=sys.version, platform=platform.platform(),
                    machine=platform.machine(), processor=platform.processor(),
                    sizes=args.sizes, trials=args.trials, base_seed=args.seed,
                    total_timed_sorts=len(raw), timer='perf_counter_ns',
                    method='Median of paired trials; alternating order; three warmups per algorithm. '
                    'Input generation, copies, RNG construction and validation excluded. '
                    'Python garbage collection kept at default settings. Shared execution environment.')
    (args.output / 'environment.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(f'Validated all {len(raw)} timed sorts.')


if __name__ == '__main__':
    main()
