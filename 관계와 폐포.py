import argparse

SIZE = 5
A = tuple(range(1, SIZE + 1))


def read_matrix():
    """Read five rows; re-prompt a malformed row instead of silently changing it."""
    print("A = {1, 2, 3, 4, 5}")
    print("관계 행렬을 한 행씩 입력하세요. 각 행은 0 또는 1 다섯 개입니다.")
    matrix = []
    for row_number in A:
        while True:
            parts = input(f"{row_number}행 > ").split()
            if len(parts) == SIZE and all(part in ("0", "1") for part in parts):
                matrix.append([int(part) for part in parts])
                break
            print("입력 오류: 공백으로 구분한 0 또는 1을 정확히 5개 입력하세요.")
    return matrix


def is_reflexive(matrix):
    return all(matrix[i][i] == 1 for i in range(SIZE))


def is_symmetric(matrix):
    return all(matrix[i][j] == matrix[j][i]
               for i in range(SIZE) for j in range(SIZE))


def is_transitive(matrix):
    return all(not (matrix[i][k] and matrix[k][j]) or matrix[i][j]
               for i in range(SIZE) for k in range(SIZE)
               for j in range(SIZE))


def properties(matrix):
    return is_reflexive(matrix), is_symmetric(matrix), is_transitive(matrix)


def reflexive_closure(matrix):
    closed = [row[:] for row in matrix]
    for i in range(SIZE):
        closed[i][i] = 1
    return closed


def symmetric_closure(matrix):
    return [[int(matrix[i][j] or matrix[j][i]) for j in range(SIZE)]
            for i in range(SIZE)]


def transitive_closure(matrix):
    """Warshall: after iteration k, paths via vertices 0..k are included."""
    closed = [row[:] for row in matrix]
    for k in range(SIZE):
        for i in range(SIZE):
            for j in range(SIZE):
                if closed[i][k] and closed[k][j]:
                    closed[i][j] = 1
    return closed


def equivalence_classes(matrix):
    """Return the distinct classes, in ascending order of first appearance."""
    if properties(matrix) != (True, True, True):
        raise ValueError("동치류는 동치관계에 대해서만 정의합니다.")
    seen = set()
    classes = []
    for i in range(SIZE):
        if i in seen:
            continue
        members = {j for j in range(SIZE) if matrix[i][j]}
        seen.update(members)
        classes.append(tuple(j + 1 for j in sorted(members)))
    return classes


def display_matrix(matrix):
    for row in matrix:
        print("  " + " ".join(map(str, row)))


def display_properties(matrix):
    r, s, t = properties(matrix)
    print(f"반사: {'O' if r else 'X'} | 대칭: {'O' if s else 'X'} | 추이: {'O' if t else 'X'}")
    if r and s and t:
        print("동치관계: O")
        for members in equivalence_classes(matrix):
            label = "{" + ", ".join(map(str, members)) + "}"