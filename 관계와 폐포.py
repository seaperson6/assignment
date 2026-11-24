"""집합 A = {1, 2, 3, 4, 5}의 관계 판별과 폐포 계산"""

import argparse

SIZE = 5
A = tuple(range(1, SIZE + 1))


def read_matrix():
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
    return all(
        matrix[i][j] == matrix[j][i]
        for i in range(SIZE)
        for j in range(SIZE)
    )


def is_transitive(matrix):
    return all(
        not (matrix[i][k] and matrix[k][j]) or matrix[i][j]
        for i in range(SIZE)
        for k in range(SIZE)
        for j in range(SIZE)
    )


def properties(matrix):
    return (
        is_reflexive(matrix),
        is_symmetric(matrix),
        is_transitive(matrix),
    )


def reflexive_closure(matrix):
    closed = [row[:] for row in matrix]

    for i in range(SIZE):
        closed[i][i] = 1

    return closed


def symmetric_closure(matrix):
    return [
        [int(matrix[i][j] or matrix[j][i]) for j in range(SIZE)]
        for i in range(SIZE)
    ]


def transitive_closure(matrix):
    # 워셜 알고리즘: k번 원소를 경유하는 경로를 차례대로 반영
    closed = [row[:] for row in matrix]

    for k in range(SIZE):
        for i in range(SIZE):
            for j in range(SIZE):
                if closed[i][k] and closed[k][j]:
                    closed[i][j] = 1

    return closed


def equivalence_classes(matrix):
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
    reflexive, symmetric, transitive = properties(matrix)

    print(
        f"반사: {'O' if reflexive else 'X'} | "
        f"대칭: {'O' if symmetric else 'X'} | "
        f"추이: {'O' if transitive else 'X'}"
    )

    if reflexive and symmetric and transitive:
        print("동치관계: O")

        for members in equivalence_classes(matrix):
            label = "{" + ", ".join(map(str, members)) + "}"
            print(f"동치류 [{members[0]}] = {label}")
    else:
        print("동치관계: X")


def run(matrix):
    print("\n[입력 관계 행렬]")
    display_matrix(matrix)

    print("\n[원래 관계의 판별]")
    display_properties(matrix)

    if properties(matrix) == (True, True, True):
        print("\n이미 동치관계이므로 폐포 계산을 생략합니다.")
        return

    for title, closure in (
        ("반사", reflexive_closure),
        ("대칭", symmetric_closure),
        ("추이", transitive_closure),
    ):
        result = closure(matrix)

        print(f"\n[{title} 폐포의 행렬]")
        display_matrix(result)

        print(f"[{title} 폐포의 재판별]")
        display_properties(result)


DEMO_CASES = {
    # 조건 1: 반사 O, 대칭 O, 추이 O
    1: [
        [int(i == j) for j in range(SIZE)]
        for i in range(SIZE)
    ],

    # 조건 2: 반사 O, 대칭 X, 추이 O
    2: [
        [int(i <= j) for j in range(SIZE)]
        for i in range(SIZE)
    ],

    # 조건 3: 반사 X, 대칭 O, 추이 X
    3: [
        [int((i, j) in ((0, 1), (1, 0))) for j in range(SIZE)]
        for i in range(SIZE)
    ],

    # 조건 4: 반사 X, 대칭 X, 추이 X
    4: [
        [int((i, j) in ((0, 1), (1, 2))) for j in range(SIZE)]
        for i in range(SIZE)
    ],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--demo-case",
        type=int,
        choices=DEMO_CASES,
        help="보고서에 사용한 입력 사례 1~4",
    )
    args = parser.parse_args()

    if args.demo_case is None:
        run(read_matrix())
    else:
        print(f"$ python report2_relation.py --demo-case {args.demo_case}")
        run(DEMO_CASES[args.demo_case])


if __name__ == "__main__":
    main()
