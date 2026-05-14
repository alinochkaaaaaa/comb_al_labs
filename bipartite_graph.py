def solve():
    with open('in.txt', 'r') as f:
        n = int(f.readline())
        graph = [list(map(int, f.readline().split())) for _ in range(n)]

    color = [-1] * n
    is_bipartite = True

    def dfs(v, c):
        nonlocal is_bipartite
        color[v] = c
        for u in range(n):
            if graph[v][u]:
                if color[u] == -1:
                    dfs(u, 1 - c)
                elif color[u] == c:
                    is_bipartite = False

    dfs(0, 0)

    with open('out.txt', 'w') as f:
        if not is_bipartite:
            f.write("N\n")
        else:
            part1 = [i + 1 for i in range(n) if color[i] == 0]
            part2 = [i + 1 for i in range(n) if color[i] == 1]

            if 1 in part2:
                part1, part2 = part2, part1

            f.write("Y\n")
            f.write(" ".join(map(str, part1)) + "\n")
            f.write(" ".join(map(str, part2)) + "\n")


if __name__ == "__main__":
    solve()