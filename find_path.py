from collections import deque


def read_input(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    idx = 0
    N = int(lines[idx])
    idx += 1

    # Списки предшественников для каждой вершины (1-indexed)
    predecessors = [[] for _ in range(N + 1)]

    for v in range(1, N + 1):
        # Парсим строку предшественников
        parts = list(map(int, lines[idx].split()))
        idx += 1

        i = 0
        while i < len(parts):
            if parts[i] == 0:
                break
            prev = parts[i]
            weight = parts[i + 1]
            predecessors[v].append((prev, weight))
            i += 2

    source = int(lines[idx]);
    idx += 1
    target = int(lines[idx])

    return N, predecessors, source, target


def topological_sort(N, adj):
    """Топологическая сортировка"""
    in_degree = [0] * (N + 1)
    for u in range(1, N + 1):
        for v, _ in adj[u]:
            in_degree[v] += 1

    queue = deque()
    for v in range(1, N + 1):
        if in_degree[v] == 0:
            queue.append(v)

    topo_order = []
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v, _ in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return topo_order


def find_max_weight_path(N, predecessors, source, target):
    # Строим граф прямых рёбер для топологической сортировки
    adj = [[] for _ in range(N + 1)]
    for v in range(1, N + 1):
        for prev, weight in predecessors[v]:
            adj[prev].append((v, weight))

    # Топологическая сортировка
    topo_order = topological_sort(N, adj)

    # DP: максимальный вес пути от источника до вершины
    dp = [-float('inf')] * (N + 1)
    parent = [-1] * (N + 1)
    dp[source] = 0

    # Проходим в топологическом порядке
    for u in topo_order:
        if dp[u] != -float('inf'):  # если вершина достижима
            for v, weight in adj[u]:
                new_weight = dp[u] + weight
                if new_weight > dp[v]:
                    dp[v] = new_weight
                    parent[v] = u

    # Проверяем, достижима ли цель
    if dp[target] == -float('inf'):
        return None, None

    # Восстанавливаем путь
    path = []
    curr = target
    while curr != -1:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    return path, dp[target]


def main():
    # Чтение входных данных
    N, predecessors, source, target = read_input('in.txt')

    # Поиск максимального пути
    path, max_weight = find_max_weight_path(N, predecessors, source, target)

    # Запись результата
    with open('out.txt', 'w') as f:
        if path is None:
            f.write("N\n")
        else:
            f.write("Y\n")
            f.write(" ".join(map(str, path)) + "\n")
            f.write(str(max_weight) + "\n")


if __name__ == "__main__":
    main()