from collections import defaultdict


def read_file(filename: str) -> (defaultdict, int, int):
    data = defaultdict(list[tuple])
    with open(filename) as file:
        for x, line in enumerate(file):
            for y, letter in enumerate(line.strip()):
                if letter != ".":
                    data[letter].append((x, y))
                width: int = y
                height: int = x
    return data, width, height


def find_anti_node(data: defaultdict[str, list[tuple[int, int]]], width: int, height: int) -> (
        set[tuple[int, int]], set[tuple[int, int]]):
    result_p1 = set()
    result_p2 = set()

    for key, nodes in data.items():
        for index in range(len(nodes) - 1):
            for node in nodes[index + 1:]:
                anti_nodes = calculate_position_of_anti_node(nodes[index], node,
                                                             manhattan_distance(nodes[index], node))
                anti_nodes_p2 = resonant_harmonics(nodes[index], node, width)
                for anti_node_p2 in anti_nodes_p2:
                    x, y = anti_node_p2
                    if (0 <= x <= min(nodes[index][0], node[0]) or max(nodes[index][0],
                                                                       node[0]) <= x <= height) and (
                            0 <= y <= min(nodes[index][1], node[1]) or max(nodes[index][1], node[1]) <= y <= width):
                        result_p2.add(anti_node_p2)

                for anti_node in anti_nodes:
                    if 0 <= anti_node[0] <= height and 0 <= anti_node[1] <= width:
                        result_p1.add(anti_node)
    return result_p1, result_p2


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = p1
    x2, y2 = p2
    distance: tuple[int, int] = (abs(x2 - x1), abs(y2 - y1))
    return distance


def calculate_position_of_anti_node(p1: tuple[int, int], p2: tuple[int, int], distance: tuple[int, int]) -> (
        tuple[int, int], tuple[int, int]):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = distance
    if x1 <= x2 and y1 <= y2:
        return (x1 - dx, y1 - dy), (x2 + dx, y2 + dy)
    elif x1 <= x2 and y1 >= y2:
        return (x1 - dx, y1 + dy), (x2 + dx, y2 - dy)
    elif x1 > x2 and y1 > y2:
        return (x1 + dx, y1 + dy), (x2 - dx, y2 - dy)
    elif x1 > x2 and y1 < y2:
        return (x1 + dx, y1 - dy), (x2 - dx, y2 + dy)


def resonant_harmonics(p1: tuple[int, int], p2: tuple[int, int], width: int) -> list[tuple[int, int]]:
    result: list = []
    x1, y1 = p1
    x2, y2 = p2
    m = (x2 - x1) / (y2 - y1)
    b = x1 - m * y1
    delta = manhattan_distance(p1, p2)[1]
    for y in range(min(y1, y2), 0 - delta, -delta):
        x = m * y + b
        result.append((int(x), y))
    for y in range(max(y1, y2), width + delta, delta):
        x = m * y + b
        result.append((int(x), y))
    return result


def visualize_frequency(data: defaultdict[str, list[tuple[int, int]]], result: list[tuple[int, int]], width: int,
                        height: int) -> None:
    grid = [["." for i in range(width + 1)] for j in range(height + 1)]
    for symbol, positions in data.items():
        for position in positions:
            x, y = position
            grid[x][y] = symbol

    for position in result:
        x, y = position
        if grid[x][y] == ".":
            grid[x][y] = "#"

    print("\n".join("".join(line) for line in grid))

    return None


def main():
    data, width, height = read_file("08_input.txt")
    result_p1, result_p2 = find_anti_node(data, width, height)
    visualize_frequency(data, result_p1, width, height)
    print()
    visualize_frequency(data, result_p2, width, height)
    print()
    print(result_p2)
    result_p1 = len(result_p1)
    result_p2 = len(result_p2)
    print(f"Solution Part 1: {result_p1}")
    print(f"Solution Part 2: {result_p2}")


if __name__ == "__main__":
    main()
