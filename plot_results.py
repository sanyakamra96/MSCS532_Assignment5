"""Regenerate the report figures from measured summary.csv (Matplotlib required)."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent

def main():
    with (ROOT / 'results/summary.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), sharey=False)
    for ax, distribution, title in zip(axes, ('random', 'sorted', 'reverse'),
                                       ('Random distinct keys', 'Sorted distinct keys', 'Reverse sorted keys')):
        for name, color, marker in [('deterministic', '#215a82', 'o'),
                                     ('randomized', '#b75125', 's')]:
            selected = [r for r in rows if r['distribution'] == distribution and r['algorithm'] == name]
            ax.plot([int(r['n']) for r in selected], [float(r['median_ms']) for r in selected],
                    label=name.capitalize(), color=color, marker=marker, linewidth=1.7)
        ax.set(title=title, xlabel='Input size n', ylabel='Median time (ms)')
        ax.set_yscale('log')
        ax.set_xticks([250, 1000, 2000, 4000])
        ax.tick_params(axis='x', labelsize=8)
        ax.grid(True, alpha=.2)
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(ROOT / 'results/runtime_comparison.png', dpi=220)
    plt.close(fig)

if __name__ == '__main__':
    main()
