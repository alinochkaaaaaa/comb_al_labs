from collections import deque
#deque - двусторонняя очередь для BFS

def chess_to_coords(pos):
    """Конвертация шахматных клетов в координаты, пр. (0, 0) => a8"""

    col = ord(pos[0]) - ord('a') # (числовой код - 97) - это столбец
    row = 8 - int(pos[1]) # (8 - цифра) - это строка

    return row, col

def coords_to_chess(row, col):
    """Конверт. координат в клетки шахматного поля"""

    return chr(col + ord('a')) + str(8 - row) #строка: код буквы и ряд

def get_horse_moves(row, col):
    """Получение всевозможных ходов коня из позиции (row, col)"""

    moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]

    #порядок из условия задачи
    ordered = [moves[3], moves[5], moves[7], moves[6],
               moves[4], moves[2], moves[0], moves[1]]

    return ordered

def valid_position(row, col):
    """Проверка, что позиция находится в пределах доски"""

    return (0 <= row < 8) and (0 <= col < 8)

def get_pawn_attacks(pawn_row, pawn_col):
    """Поля, которые могут быть атакованы пешкой"""

    attacks = []
    for i in [-1, 1]: # удар влево и вправо
        atrack_row = pawn_row + 1 # вниз (т.к пешка черная)
        atrack_col = pawn_col + i
        if valid_position(atrack_row, atrack_col):
            attacks.append((atrack_row, atrack_col))

    return attacks

def find_horse_path(horse_pos, pawn_pos):
    """Поиск кратчайшего пути конем до пешки"""

    # позиции коня и пешкки
    h_row, h_col = chess_to_coords(horse_pos)
    p_row, p_col = chess_to_coords(pawn_pos)

    # поля под ударом пешки
    pawn_attack = get_pawn_attacks(p_row, p_col)

    # BFS
    queue = deque()
    queue.append((h_row, h_col))

    # хранит информацию из какой клетки мы пришли в данную
    # Ключ — текущая клетка, значение — предыдущая
    parent = {}
    parent[(h_row, h_col)] = None

    visited = set()
    visited.add((h_row, h_col))

    while queue:
        cur_row, cur_col = queue.popleft()

        # дошли до пешки
        if (cur_row, cur_col) == (p_row, p_col):
            # восстанавливаем путь
            path = []
            pos = (cur_row, cur_col)
            # идем назад по родителям до None
            while pos is not None:
                path.append(pos)
                pos = parent[pos]
            path.reverse() # тк нам нужно в обратном порядке

            return [coords_to_chess(r, c) for r, c in path]

        # все ходы коня
        for dr, dc in get_horse_moves(cur_row, cur_col):
            new_row, new_col = cur_row + dr, cur_col + dc

            if not valid_position(new_row, new_col): continue

            # нельзя быть под ударом пешки
            if (new_row, new_col) in pawn_attack : continue

            if (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                parent[(new_row, new_col)] = (cur_row, cur_col)
                queue.append((new_row, new_col))

    return None # путь не найден

def main():
    try:
        with open('in.txt') as f:
            horse_pos = f.readline().strip()
            pawn_pos = f.readline().strip()

        path = find_horse_path(horse_pos, pawn_pos)

        with open('out.txt', 'w') as f:
            try:
                for move in path:
                    f.write(move + '\n')
            except TypeError:
                error_msg = "Путь не найден"
                print(f"\n{error_msg}")
    except FileNotFoundError:
        print("File in.txt not found")
    except Exception as e:
        print(f"Exeption: {e}")

if __name__ == "__main__":
    main()