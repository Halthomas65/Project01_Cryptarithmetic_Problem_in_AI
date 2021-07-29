import random
import string
import re
import argparse


def num_to_string(number, digit_assign):
    for digit in digit_assign:
        number = number.replace(digit, digit_assign[digit])
    return number

# create testcases into 'into_file' file
# max_testcase: numbers testcase
# max_letter: maximum number of letter per word
# max_word: maximum number of word per testcase
# sign: '+'/'-' for testcase just include plus/subtract for level 1 and 2
#       'both' for testcase include both plus, subtract, bracket for level 3
#       '*' for testcase just include multipy for level 4,


def generate_testcase(max_testcase, max_letter, max_word, sign):
    tc = ''
    for i in range(max_testcase):
        word_size = random.randint(3, max_word)
        numbers = []
        for j in range(word_size - 1):
            letter_size = random.randint(3, max_letter)
            numbers.append(random.randint(
                10 ** (letter_size - 1), 10 ** letter_size - 1))
        if sign == '+':
            numbers.append(sum(numbers))
        elif sign == '-':
            letter_size = random.randint(3, max_letter)
            numbers.append(random.randint(
                10 ** (letter_size - 1), 10 ** letter_size - 1))
            numbers[0] = sum(numbers[1:])
        elif sign == '*':
            prod = 1
            for number in numbers:
                prod *= number
            numbers.append(prod)
        signs = []
        if sign == 'both':
            right = 0
            for i in range(len(numbers)):
                if random.choice([True, False]):
                    signs.append('+')
                    right += numbers[i]
                else:
                    signs.append('-')
                    right -= numbers[i]
            numbers.append(right)
            if right >= 0:
                signs.append('+')
            else:
                signs.append('-')
        numbers = list(map(lambda x: str(abs(x)), numbers))
        digits = set(''.join(numbers))
        digit_assign = {}
        letter_assign = {}
        for digit in digits:
            letter = random.choice(string.ascii_lowercase)
            while letter_assign.get(letter) != None:
                letter = random.choice(string.ascii_lowercase)
            digit_assign[digit] = letter
            letter_assign[letter] = digit
        numbers = list(map(lambda x: num_to_string(x, digit_assign), numbers))
        if sign != 'both':
            tc += sign.join(numbers[:-1]) + '=' + numbers[-1] + '\n'
        else:
            t = ''
            close_pos = -1
            while close_pos < len(numbers) - 3:
                if len(numbers) == 3:
                    if random.choice([True, False]):
                        open_pos = random.randint(
                            close_pos + 1, len(numbers) - 3)
                    else:
                        t += ('' if signs[0] ==
                              '+' else signs[0]) + numbers[0] + signs[1] + numbers[1]
                        close_pos += 1
                    continue
                else:
                    open_pos = random.randint(close_pos + 1, len(numbers) - 3)
                open_sign = signs[open_pos]
                if open_pos == 0 and signs[0] == '+':
                    open_sign = ''
                for i in range(close_pos + 1, open_pos):
                    t += ('' if i == 0 and signs[i] ==
                          '+' else signs[i]) + numbers[i]
                t += open_sign + '(' + numbers[open_pos]
                close_pos = open_pos + \
                    random.randint(1, len(numbers) - 2 - open_pos)
                for i in range(open_pos + 1, close_pos):
                    t += signs[i] + numbers[i]
                t += signs[close_pos] + numbers[close_pos] + ')'
            t += '=' + (signs[-1] if signs[-1] == '-' else '') + numbers[-1]
            tc += t + '\n'
    return tc[:-1]


def read_input(filename='input.txt'):
    raw_inps = open(filename, 'r').read().strip().split('\n')
    symbols = set({'+', '-', '*', '=', ')', '('})
    inps = []
    for line in raw_inps:
        pre_sign_pos = -1
        cur_sign_pos = 0
        is_sign_change = False
        signs = []
        inp = []
        if (line[0] in string.ascii_letters or line[0] == '(') and line[1] in string.ascii_letters:
            signs.append('+')
        for i in range(len(line)):
            c = line[i]
            if c == '(' and i > 0 and line[i - 1] == '-':
                is_sign_change = True
            elif c == ')':
                is_sign_change = False
            if c in symbols:
                cur_sign_pos = i
                if pre_sign_pos + 1 < cur_sign_pos:
                    inp.append(line[pre_sign_pos + 1: cur_sign_pos])
                pre_sign_pos = cur_sign_pos
                if c != '=' and c != '(' and c != ')':
                    sign = c
                    if is_sign_change and c != '*':
                        sign = '-' if c == '+' else '+'
                    signs.append(sign)
        if line[pre_sign_pos] == '=':
            signs.append('+')
        inp.append(line[pre_sign_pos + 1:])
        inps.append((inp, signs))
    return inps


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--range', type=str, help='range', default='3,5')
    args = parser.parse_args()
    opers = ['+', '-', 'both', '*']
    rge = list(map(lambda x: int(x), args.range.split(',')))
    rge[0] = 3 if rge[0] < 3 else rge[0]
    rge[1] = 4 if rge[1] < 4 else rge[1]
    all_tc = []
    for oper in opers:
        all_tc.append(generate_testcase(random.randint(
            *rge), random.randint(*rge), random.randint(*rge), oper))

    into_file = 'input.txt'
    open(into_file, 'w').write('\n'.join(all_tc))
