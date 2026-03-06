def solve():
    with open('in.txt', 'r') as f:
        n = int(f.readline())
        # матрица смежности: для каждой из n строк преобразуем её в список чисел
        graph = [list(map(int, f.readline().split())) for _ in range(n)]

    color = [-1] * n  # -1 - не покрашена, 0 и 1 - цвета
    is_bipartite = True

    def dfs(v, c):
        nonlocal is_bipartite
        color[v] = c
        for u in range(n):
            if graph[v][u]:  # если есть ребро
                if color[u] == -1: # не покрашена, то красив в противоположный цвет
                    dfs(u, 1 - c)
                elif color[u] == c: # цвет смежных вершин совпал
                    is_bipartite = False

    # DFS от первой вершины (граф связный)
    dfs(0, 0)

    with open('out.txt', 'w') as f:
        if not is_bipartite:
            f.write("N\n")
        else:
            # Собираем вершины по долям
            part1 = [i + 1 for i in range(n) if color[i] == 0]
            part2 = [i + 1 for i in range(n) if color[i] == 1]

            # Проверяем, какая доля содержит вершину 1
            if 1 in part2:
                part1, part2 = part2, part1

            f.write("Y\n")
            f.write(" ".join(map(str, part1)) + "\n")
            f.write(" ".join(map(str, part2)) + "\n")


if __name__ == "__main__":
    solve()