import json

import time



def mac(pattern, filter_data):
    score = 0.0

    size = len(pattern)

    for i in range(size):
        for j in range(size):
            score += pattern[i][j] * filter_data[i][j]

    return score


def measure_performance(size, repeat=100000, trials=5):
    pattern = [[1 for _ in range(size)] for _ in range(size)]
    filter_data = [[1 for _ in range(size)] for _ in range(size)]

    # 워밍업
    mac(pattern, filter_data)

    total_times = []

    for _ in range(trials):
        start_time = time.perf_counter()

        for _ in range(repeat):
            mac(pattern, filter_data)

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        average_time = (elapsed_time / repeat) * 1000
        print("전체 측정 시간:", elapsed_time, "초")

        total_times.append(average_time)

    final_average = sum(total_times) / trials

    print("행렬 크기:", size, "x", size)
    print("MAC 연산 횟수:", size * size)
    print("반복 횟수:", repeat)
    print("측정 횟수:", trials)
    print("평균 실행 시간:", final_average, "ms")
    print("검증용 MAC 점수:", mac(pattern, filter_data))



def normalize_label(label):
    if label == "+" or label == "cross":
        return "Cross"
    elif label == "x":
        return "X"

    return label

def test_json_patterns(data):
    print("\n===== JSON 자동 테스트 =====")

    epsilon = 1e-9

    total = 0
    passed = 0
    failed = 0
    failed_cases = []

    for key, value in data["patterns"].items():
        total += 1

        size = int(key.split("_")[1])

        pattern = value["input"]
        expected = normalize_label(value["expected"])

        filters = data["filters"][f"size_{size}"]

        score_cross = mac(pattern, filters["cross"])
        score_x = mac(pattern, filters["x"])

        if abs(score_cross - score_x) < epsilon:
            predicted = "UNDECIDED"
        elif score_cross > score_x:
            predicted = "Cross"
        else:
            predicted = "X"

        if predicted == expected:
            result = "PASS"
            passed += 1
        else:
            result = "FAIL"
            failed += 1
            failed_cases.append((key, predicted, expected))

        print("\n패턴 이름:", key)
        print("행렬 크기:", size, "x", size)
        print("Cross 점수:", score_cross)
        print("X 점수:", score_x)
        print("예측 라벨:", predicted)
        print("정답 라벨:", expected)
        print("테스트 결과:", result)

        if result == "FAIL":
            if predicted == "UNDECIDED":
                print("실패 사유: 두 필터의 점수가 같아 판정할 수 없습니다.")
            else:
                print("실패 사유: 예측 라벨과 정답 라벨이 다릅니다.")

    print("\n===== 테스트 통계 =====")
    print("전체 테스트:", total)
    print("통과:", passed)
    print("실패:", failed)

    accuracy = 0.0

    if total > 0:
        accuracy = (passed / total) * 100

    print("통과율:", accuracy, "%")

    print("\n===== 실패 케이스 목록 =====")

    if failed_cases:
        for key, predicted, expected in failed_cases:
            print("패턴:", key)
            print("예측:", predicted)
            print("정답:", expected)
    else:
        print("실패한 케이스가 없습니다.")

# 십자가 패턴
pattern = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

# 십자가 필터
cross_filter = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

# X 필터
x_filter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]



with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def validate_matrix(matrix, size):
    # 행렬의 전체 행 개수 확인
    if len(matrix) != size:
        return False

    # 각 행의 열 개수와 숫자 여부 확인
    for row in matrix:
        if len(row) != size:
            return False

        for value in row:
            if not isinstance(value, (int, float)):
                return False

    return True

def validate_filters(data):
    print("\n===== 필터 데이터 검증 =====")

    for size_key, filters in data["filters"].items():
        size = int(size_key.split("_")[1])

        for filter_name, matrix in filters.items():
            if validate_matrix(matrix, size):
                print(size_key, filter_name, ": 정상")
            else:
                print(size_key, filter_name, ": 오류")

print("JSON 파일 로드 성공")
print("필터 목록:", list(data["filters"].keys()))
print("패턴 개수:", len(data["patterns"]))

def validate_patterns(data):
    print("\n===== 패턴 데이터 검증 =====")

    for key, value in data["patterns"].items():
        size = int(key.split("_")[1])

        matrix = value["input"]
        expected = value["expected"]

        matrix_valid = validate_matrix(matrix, size)
        label_valid = expected in ["x", "+"]

        if matrix_valid and label_valid:
            print(key, ": 정상")
        else:
            print(key, ": 오류")

            if not matrix_valid:
                print("  - 행렬 크기 또는 숫자 데이터 오류")

            if not label_valid:
                print("  - 정답 라벨 오류")

# JSON 패턴 목록 확인

# JSON 패턴 목록 확인 및 크기 추출
print("\n===== JSON 테스트 케이스 =====")

for key, value in data["patterns"].items():

    size = int(key.split("_")[1])

    print("패턴 이름:", key)
    print("행렬 크기:", size, "x", size)
    print("정답 라벨:", value["expected"])

def input_matrix(name):
    matrix = []

    print(f"\n{name} 입력 (3줄, 숫자 3개씩)")

    for i in range(3):
        while True:
            try:
                row = input(f"{i + 1}번째 줄: ").split()

                if len(row) != 3:
                    print("입력 형식 오류: 숫자 3개를 입력하세요.")
                    continue

                row = [int(x) for x in row]

                matrix.append(row)
                break

            except ValueError:
                print("숫자만 입력하세요. 다시 입력해주세요.")

    return matrix
# 2. MAC 연산 함수


# 3. 사용자 입력
filter_a = input_matrix("필터 A")
filter_b = input_matrix("필터 B")
pattern = input_matrix("패턴")


# 4. MAC 연산
score_a = mac(pattern, filter_a)
score_b = mac(pattern, filter_b)

# 5. 결과 판정
print("\n===== MAC 연산 결과 =====")
print("A 점수:", score_a)
print("B 점수:", score_b)

# 6. 결과 출력
epsilon = 1e-9

if abs(score_a - score_b) < epsilon:
    print("판정 결과: UNDECIDED")
elif score_a > score_b:
    print("판정 결과: 필터 A와 더 유사합니다.")
else:
    print("판정 결과: 필터 B와 더 유사합니다.")





validate_filters(data)
validate_patterns(data)
test_json_patterns(data)

print("\n===== MAC 성능 측정 =====")

measure_performance(3)
measure_performance(5)
measure_performance(13)
measure_performance(25)