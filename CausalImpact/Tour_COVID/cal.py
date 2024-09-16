def calculate():
    # 사용자로부터 숫자와 연산자를 입력받음
    num1 = float(input("첫 번째 숫자를 입력하세요: "))
    operator = input("연산자를 입력하세요(+, -, *, /): ")
    num2 = float(input("두 번째 숫자를 입력하세요: "))

    # 연산자에 따라 적절한 연산 수행
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        if num2 == 0:
            return "0으로 나눌 수 없습니다!"
        result = num1 / num2
    else:
        return "잘못된 연산자입니다!"

    return f"결과: {result}"

# 계산기 실행
print(calculate())
