import csv
import matplotlib.pyplot as plt
import os


def read_csv(path='tests/metrics.csv'):
    rows = []
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k: (float(v) if k not in ('mode','N') else (v if k=='mode' else int(v))) for k,v in r.items()})
    return rows


def plot(rows, out_dir='docs'):
    os.makedirs(out_dir, exist_ok=True)
    # organize by mode
    modes = {'node': [], 'subtree': []}
    for r in rows:
        modes[r['mode']].append(r)
    for m in modes:
        modes[m].sort(key=lambda x: x['N'])

    Ns_node = [r['N'] for r in modes['node']]
    build_node = [r['build_time_s'] for r in modes['node']]
    mem_node = [r['mem_peak_mb'] for r in modes['node']]
    cold_node = [r['cold_lookup_s'] for r in modes['node']]

    Ns_sub = [r['N'] for r in modes['subtree']]
    build_sub = [r['build_time_s'] for r in modes['subtree']]
    mem_sub = [r['mem_peak_mb'] for r in modes['subtree']]
    cold_sub = [r['cold_lookup_s'] for r in modes['subtree']]

    # Build time
    plt.figure()
    plt.plot(Ns_node, build_node, marker='o', label='node-stored')
    plt.plot(Ns_sub, build_sub, marker='o', label='subtree')
    plt.xlabel('N (number of products)')
    plt.ylabel('Build time (s)')
    plt.title('Build time vs N')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(out_dir,'fig_build_time.png'), dpi=150)
    plt.close()

    # Memory
    plt.figure()
    plt.plot(Ns_node, mem_node, marker='o', label='node-stored')
    plt.plot(Ns_sub, mem_sub, marker='o', label='subtree')
    plt.xlabel('N (number of products)')
    plt.ylabel('Peak memory (MB)')
    plt.title('Peak memory vs N')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(out_dir,'fig_memory.png'), dpi=150)
    plt.close()

    # Cold lookup
    plt.figure()
    plt.plot(Ns_node, cold_node, marker='o', label='node-stored')
    plt.plot(Ns_sub, cold_sub, marker='o', label='subtree')
    plt.xlabel('N (number of products)')
    plt.ylabel('Cold prefix lookup time (s)')
    plt.title('Cold prefix lookup time vs N')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(out_dir,'fig_cold_lookup.png'), dpi=150)
    plt.close()

    print('Saved charts to', out_dir)


if __name__ == '__main__':
    rows = read_csv()
    plot(rows)
