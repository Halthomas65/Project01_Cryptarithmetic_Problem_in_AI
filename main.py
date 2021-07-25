from utility import read_input, generate_testcase
import random
import time
import sys
import math
import enum


def first_solution(words):
    solution = list(set(''.join(words)))
    for _ in range(10 - len(solution)):
        solution.append("_")
    return solution


def word_value(word, solution):
    val = 0
    for letter in word:
        val = val * 10 + letter_value(letter, solution)
    return val


def letter_value(letter, solution):
    for val in range(len(solution)):
        if letter == solution[val]:
            return val


def calculate(vals, sign):
    calculator = {
        "+": lambda x: sum(x[:-1]) - x[-1],
        "-": lambda x: x[0] - sum(x[1:-1]) - x[-1],
        # "x" : ,
        # "both" :
    }
    return calculator.get(sign)(vals) if calculator.get(sign) != None else 0


def score(solution, words, sign):
    vals = [word_value(word, solution) for word in words]
    # TODO: read this
    # level 3 viết hàm tính toán chổ này lại, không đơn thuần chỉ là hàm SUM nữa
    # HINT: lưu lại mảng dấu từ lúc read input, viết hàm sau đó thêm vào both ở calculator trong hàm calculate
    # tương tự cho level 4
    # HINT: nhân hai số thì tương tự như cộng trừ hai số thôi
    return abs(calculate(vals, sign))


def other_solution(solution, first_letters):
    other = solution
    i = random.randint(0, 9)
    j = random.randint(0, 9)
    other[i], other[j] = other[j], other[i]
    while other[0] in first_letters:
        other[i], other[j] = other[j], other[i]
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        other[i], other[j] = other[j], other[i]
    if other[0] in first_letters:
        print('error\n')
    return other


def get_solution(solution, words):
    # def get_solution(solution, words, sign):
    vals = [str(word_value(word, solution)) for word in words]
    # return ("%s = %s" % (sign.join(vals[:-1]), vals[-1]))
    # return ("%s = %s" % (sign.join(vals[:-1]), vals[-1])) + '\n' + ''.join(sorted(list(set(''.join(words))))) + '\n' + str(word_value(sorted(list(set(''.join(words)))), solution))
    # return ''.join(sorted(list(set(''.join(words))))) + '\n' + str(word_value(sorted(list(set(''.join(words)))), solution))
    return str(word_value(sorted(list(set(''.join(words)))), solution))


def solve_utl(try_time, max_time, duration, words, sign):
    first_letters = set([word[0] for word in words])
    best_solution = first_solution(words)
    best_score = score(best_solution, words, sign)
    start = time.time()
    end = time.time()
    while best_score != 0 and end - start < duration:
        other_sol = other_solution(best_solution, first_letters)
        other_score = score(other_sol, words, sign)
        if other_score < best_score or random.randint(1, 100) == 1:
            best_score = other_score
            best_solution = other_sol
        end = time.time()
    if best_score != 0:
        if try_time < max_time:
            return solve_utl(try_time + 1, max_time, duration, words, sign)
        return 'NO SOLUTION'
    else:
        # return get_solution(best_solution, words) + '\n' + str(try_time) + ' - ' + str(end - start)
        # return get_solution(best_solution, words, sign)
        return get_solution(best_solution, words)


def solve(words, sign):
    max_time = 300
    duration = 30
    max_each_time = int(max_time / duration)
    cnt = 0
    for word in words:
        cnt += len(word)
    average = cnt / len(words)
    if average > duration:
        duration = math.ceil(average)
        max_each_time = math.ceil(max_time / duration)
    print(solve_utl(1, max_each_time, duration, words, sign))


if __name__ == '__main__':
    # generate_testcase(3, 4, '+')
    # generate_testcase(3, 4, '-')
    for inp in read_input():
        solve(inp[0], inp[1])
