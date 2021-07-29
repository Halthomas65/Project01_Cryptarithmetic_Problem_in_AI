from utility import read_input, generate_testcase
import random
import time
import math

# e.g. words = ['abc', 'bcd', 'htf'] => first_letters = ['a', 'b', 'h']


def first_solution(words, first_letters):
    # init solution
    solution = list(set(''.join(words)))
    for _ in range(10 - len(solution)):
        solution.append("_")
    # get valid solution if it was not, e.g. return ['a', 'b', '_', 'c', 'd', 'h', '_','t', 'f', '_']
    return other_solution(solution, first_letters)

# e.g. word = 'abc', solution = ['a', 'b', '_', 'c', 'd', 'h', '_','t', 'f', '_']


def word_value(word, solution):
    val = 0
    for letter in word:
        val = val * 10 + letter_value(letter, solution)
    # from word and solution, calculate word_value, e.g. val = 123
    return val

# e.g. letter = 'a', solution = ['a', 'b', '_', 'c', 'd', 'h', '_','t', 'f', '_']


def letter_value(letter, solution):
    for val in range(len(solution)):
        if letter == solution[val]:
            # return position of letter in solution
            # above case val = 0
            return val


def calculate(vals, signs):
    # if all in signs are just '*'
    # it must be multiplication
    if signs[1] == '*':
        left = 1
        right = vals[-1]
        for i in range(len(vals) - 1):
            left *= vals[i]
        return left - right
    # if not, other calculation
    # change every sign in signs to integer
    # if '+', change to 1, if '-', change to -1
    # e.g. signs before: ['+', '-', '+'] => signs after: [1, -1, 1]
    signs = list(map(lambda sign: 1 if sign == '+' else -
                 1 if sign == '-' else 1, signs))
    # calculate the actual value, combine value and its sign
    # e.g. vals = [123, 456, 789], signs = [1, -1, 1] => sign_vals = [123, -456, 789]
    sign_vals = [signs[i] * vals[i] for i in range(len(vals))]
    # left side - right side
    return sum(sign_vals[:-1]) - sign_vals[-1]


def score(solution, words, signs):
    # create the values from words
    vals = [word_value(word, solution) for word in words]
    # abs because we just need the difference
    return abs(calculate(vals, signs))

#


def other_solution(solution, first_letters):
    # swap two random positions in the solution
    other = solution
    i = random.randint(0, 9)
    j = random.randint(0, 9)
    other[i], other[j] = other[j], other[i]
    # swap till valid solution
    # the first letters can't be zero
    while other[0] in first_letters:
        other[i], other[j] = other[j], other[i]
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        other[i], other[j] = other[j], other[i]
    return other


def get_solution(solution, words):
    # convert value from integer to string
    vals = [str(word_value(word, solution)) for word in words]
    # for debugging
    # return ("%s = %s" % (' '.join(vals[:-1]), vals[-1]))
    # return ("%s = %s" % (' '.join(vals[:-1]), vals[-1])) + '\n' + ''.join(sorted(list(set(''.join(words))))) + '\n' + str(word_value(sorted(list(set(''.join(words)))), solution))
    # return ''.join(sorted(list(set(''.join(words))))) + '\n' + str(word_value(sorted(list(set(''.join(words)))), solution))
    # final format
    return str(word_value(sorted(list(set(''.join(words)))), solution))

# try_time(int): current number of reruns of the function solve_utl
# max_time(int): maximum number of reruns of the function solve_utl
# duration(int): running time of function solve_utl each time
# e.g. words = ['abc', 'bcd', 'htf']
# e.g. signs = ['+', '-', '+']


def solve_utl(try_time, max_time, duration, words, signs):
    # e.g. first_letters = ['a', 'b', 'h']
    first_letters = set([word[0] for word in words])
    # e.g. best_solution = ['d', 'a', 'c', 'b', 'h', 't', 'f', '_', '_', '_']
    best_solution = first_solution(words, first_letters)
    # e.g. best_score = 45 (just example, not accurate)
    best_score = score(best_solution, words, signs)
    # start and end to calculate time to stop when overtime (duration)
    start = time.time()
    end = time.time()
    # best_score == 0 => solution found
    while best_score != 0 and end - start < duration:
        other_sol = other_solution(best_solution, first_letters)
        other_score = score(other_sol, words, signs)
        if other_score < best_score or random.randint(1, 100) == 1:
            best_score = other_score
            best_solution = other_sol
        end = time.time()
    # check solution found or overtime and try again or NO SOLUTION
    if best_score != 0:
        if try_time < max_time:
            # overtime and try again
            return solve_utl(try_time + 1, max_time, duration, words, signs)
        # NO SOLUTION
        return 'NO SOLUTION'
    else:
        # solution found
        return get_solution(best_solution, words)


def solve(words, signs):
    # default parameters
    # 10 minutes
    max_time = 600
    # 30 seconds each solve_utl
    duration = 30
    # 20 times
    max_each_time = int(max_time / duration)
    # default above parameters when large number of letter in word
    cnt = 0
    for word in words:
        cnt += len(word)
    average = cnt / len(words)
    if average > duration:
        duration = math.ceil(average)
        max_each_time = math.ceil(max_time / duration)
    # try_time starts at 1
    print(solve_utl(1, max_each_time, duration, words, signs))


if __name__ == '__main__':
    # for each testcase
    for inp in read_input('input.txt'):
        # solve it
        solve(*inp)
