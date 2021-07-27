from utility import read_input, generate_testcase
import random
import time
import math


def first_solution(words, first_letters):
    solution = list(set(''.join(words)))
    for _ in range(10 - len(solution)):
        solution.append("_")
    return other_solution(solution, first_letters)


def word_value(word, solution):
    val = 0
    for letter in word:
        val = val * 10 + letter_value(letter, solution)
    return val


def letter_value(letter, solution):
    for val in range(len(solution)):
        if letter == solution[val]:
            return val


def calculate(vals, signs):
    if signs[1] == '*':
        left = 1
        right = vals[-1]
        for i in range(len(vals) - 1):
            left *= vals[i]
        return left - right
    signs = list(map(lambda sign: 1 if sign == '+' else -
                 1 if sign == '-' else 1, signs))
    sign_vals = [signs[i] * vals[i] for i in range(len(vals))]
    return sum(sign_vals[:-1]) - sign_vals[-1]


def score(solution, words, signs):
    vals = [word_value(word, solution) for word in words]
    return abs(calculate(vals, signs))


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
    return other


def get_solution(solution, words):
    vals = [str(word_value(word, solution)) for word in words]
    # return ("%s = %s" % (' '.join(vals[:-1]), vals[-1]))
    # return ("%s = %s" % (' '.join(vals[:-1]), vals[-1])) + '\n' + ''.join(sorted(list(set(''.join(words))))) + '\n' + str(word_value(sorted(list(set(''.join(words)))), solution))
    # return ''.join(sorted(list(set(''.join(words))))) + '\n' + str(word_value(sorted(list(set(''.join(words)))), solution))
    return str(word_value(sorted(list(set(''.join(words)))), solution))


def solve_utl(try_time, max_time, duration, words, signs):
    first_letters = set([word[0] for word in words])
    best_solution = first_solution(words, first_letters)
    best_score = score(best_solution, words, signs)
    start = time.time()
    end = time.time()
    while best_score != 0 and end - start < duration:
        other_sol = other_solution(best_solution, first_letters)
        other_score = score(other_sol, words, signs)
        if other_score < best_score or random.randint(1, 100) == 1:
            best_score = other_score
            best_solution = other_sol
        end = time.time()
    if best_score != 0:
        if try_time < max_time:
            return solve_utl(try_time + 1, max_time, duration, words, signs)
        return 'NO SOLUTION'
    else:
        return get_solution(best_solution, words)


def solve(words, signs):
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
    print(solve_utl(1, max_each_time, duration, words, signs))


if __name__ == '__main__':
    # generate_testcase(3, 4, '+')
    for inp in read_input():
        solve(*inp)
