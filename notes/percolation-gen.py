import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def percolate(L, p, seed=None):
    rng = np.random.RandomState(seed)
    bonds = rng.random((L, L, 2)) < p
    return bonds

def find_clusters(bonds, L):
    parent = list(range(L * L))
    rank = [0] * (L * L)

    def idx(i, j):
        return i * L + j

    def find(x):
        result = x
        while parent[result] != result:
            result = parent[result]
        while parent[x] != result:
            parent[x], x = result, parent[x]
        return result

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    for i in range(L):
        for j in range(L):
            if bonds[i, j, 0] and j + 1 < L:
                union(idx(i, j), idx(i, j + 1))
            if bonds[i, j, 1] and i + 1 < L:
                union(idx(i, j), idx(i + 1, j))

    clusters = {}
    for i in range(L):
        for j in range(L):
            root = find(idx(i, j))
            if root not in clusters:
                clusters[root] = []
            clusters[root].append((i, j))

    return {k: v for k, v in clusters.items() if len(v) > 1}

def plot_percolation(L, p, seed, filename):
    bonds = percolate(L, p, seed=seed)
    clusters = find_clusters(bonds, L)

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L-0.5)
    ax.set_ylim(-0.5, L-0.5)
    ax.axis('off')

    # Draw bonds
    for i in range(L):
        for j in range(L):
            if bonds[i, j, 0]:
                ax.plot([j, j+1], [L-1-i, L-1-i], 'k-', lw=0.8, zorder=1)
            if bonds[i, j, 1]:
                ax.plot([j, j], [L-1-i, L-i], 'k-', lw=0.8, zorder=1)

    # Color clusters by size using a colormap
    cmap = plt.cm.cividis
    sizes = [len(v) for v in clusters.values()]
    max_size = max(sizes) if sizes else 1

    for key, members in clusters.items():
        norm_size = len(members) / max_size
        color = cmap(norm_size)
        xs = [m[1] + 0.5 for m in members]
        ys = [L - 1 - m[0] + 0.5 for m in members]
        ax.scatter(xs, ys, s=2.5, color=color, zorder=2, edgecolors='none')

    # Highlight percolating cluster
    percolating = []
    for key, members in clusters.items():
        ys = [m[0] for m in members]
        if min(ys) == 0 and max(ys) == L - 1:
            percolating = members
            break

    if percolating:
        xs = [m[1] + 0.5 for m in percolating]
        ys = [L - 1 - m[0] + 0.5 for m in percolating]
        ax.scatter(xs, ys, s=15, color='gold', zorder=3, edgecolors='darkgoldenrod',
                   linewidths=0.3, alpha=0.8)

    n_clusters = len(clusters)
    largest_n = max(sizes) if sizes else 0
    percolates = "yes" if percolating else "no"

    ax.text(0.02, 0.98,
            f'p = {p:.4f}\nclusters = {n_clusters}\nlargest = {largest_n}\npercolates = {percolates}',
            transform=ax.transAxes, ha='left', va='top', fontsize=9, color='gold',
            family='monospace',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', edgecolor='none'))

    plt.savefig(filename, dpi=150, facecolor='black', edgecolor='none', pad_inches=0)
    plt.close()
    return filename

L = 100
filenames = []
filenames.append(plot_percolation(L, 0.55, 42, "assets/percolation-subcritical.webp"))
filenames.append(plot_percolation(L, 0.5927, 42, "assets/percolation-critical.webp"))
filenames.append(plot_percolation(L, 0.65, 42, "assets/percolation-supercritical.webp"))

for f in filenames:
    print(f)
