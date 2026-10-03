# 소행렬 생성
def minor(matrix, i, j):
    return [
        row[:j] + row[j + 1:]
        for r, row in enumerate(matrix) if r != i
    ]


# 행렬식 계산
def determinant(matrix):
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return (
            matrix[0][0] * matrix[1][1]
            - matrix[0][1] * matrix[1][0]
        )

    det = 0
    for j in range(n):
        det += (
            (-1) ** j * matrix[0][j]
            * determinant(minor(matrix, 0, j))
        )
    return det


# 행렬식을 이용한 역행렬
def inverse_matrix(matrix):
    n = len(matrix)
    det = determinant(matrix)

    if det == 0:
        return None

    # 여인수 행렬 생성
    cofactor = []
    for i in range(n):
        row = []
        for j in range(n):
            value = (-1) ** (i + j) * determinant(minor(matrix, i, j))
            row.append(value)
        cofactor.append(row)

    # 전치하면서 행렬식으로 나누기
    return [
        [cofactor[j][i] / det for j in range(n)]
        for i in range(n)
    ]


# 가우스-조던 소거법을 이용한 역행렬
def gauss_jordan_inverse(matrix):
    n = len(matrix)

    if determinant(matrix) == 0:
        return None

    # 확장행렬 생성
    augmented = []
    for i in range(n):
        identity_row = [0] * n
        identity_row[i] = 1
        augmented.append(matrix[i] + identity_row)

    for i in range(n):
        # 절댓값이 가장 큰 피벗 선택
        pivot_row = i
        for k in range(i + 1, n):
            if abs(augmented[k][i]) > abs(augmented[pivot_row][i]):
                pivot_row = k

        augmented[i], augmented[pivot_row] = (
            augmented[pivot_row], augmented[i]
        )

        pivot = augmented[i][i]
        if pivot == 0:
            return None

        # 피벗을 1로 만들기
        for j in range(2 * n):
            augmented[i][j] /= pivot

        # 다른 행의 현재 열을 0으로 만들기
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(2 * n):
                    augmented[k][j] -= factor * augmented[i][j]

    return [row[n:] for row in augmented]


# 차수 입력
while True:
    n = int(input("정방행렬의 차수를 입력하세요 (2~4): "))
    if 2 <= n <= 4:
        break
    print("2~4 사이의 정수를 입력해주세요.")


# 행렬 입력
matrix = []
for i in range(n):
    while True:
        row = list(map(int, input(f"{i + 1}행: ").split()))
        if len(row) == n:
            matrix.append(row)
            break
        print(f"정수를 {n}개 입력해주세요.")


# 결과 출력
result1 = inverse_matrix(matrix)
result2 = gauss_jordan_inverse(matrix)

print("\n행렬식으로 구한 역행렬:")
if result1 is None:
    print("역행렬이 존재하지 않습니다.")
else:
    for row in result1:
        print([round(value, 6) for value in row])

print("\n가우스-조던 소거법으로 구한 역행렬:")
if result2 is None:
    print("역행렬을 계산할 수 없습니다.")
else:
    for row in result2:
        print([round(value, 6) for value in row])

#----------------------------
# 추가 기능 구현
# 원래 행렬과 역행렬을 곱해서 검산
def check_inverse(matrix, inverse):
    n = len(matrix)
    product = []

    for i in range(n):
        row = []

        for j in range(n):
            value = 0

            for k in range(n):
                value += matrix[i][k] * inverse[k][j]

            row.append(value)

        product.append(row)

    print("\n원래 행렬 × 역행렬:")
    for row in product:
        print([round(value, 6) for value in row])

    # 단위행렬인지 확인
    for i in range(n):
        for j in range(n):
            expected = 1 if i == j else 0

            if abs(product[i][j] - expected) > 1e-8:
                return False

    return True

# 결과 비교
if result1 is not None and result2 is not None:
    same = True
    for i in range(n):
        for j in range(n):
            if abs(result1[i][j] - result2[i][j]) > 1e-8:
                same = False

    if same:
        print("\n두 방법의 결과가 오차 범위 내에서 동일합니다.")
    else:
        print("\n두 방법의 결과가 다릅니다.")
    
if result1 is not None:
    print("\n[행렬식 방법 검산]")
    if check_inverse(matrix, result1):
        print("검산 성공")
    else:
        print("검산 실패")

if result2 is not None:
    print("\n[가우스-조던 방법 검산]")
    if check_inverse(matrix, result2):
        print("검산 성공")
    else:
        print("검산 실패")
         
