import random
import string
import re


def num_to_string(number, digit_assign):
    for digit in digit_assign:
        number = number.replace(digit, digit_assign[digit])
    return number


def generate_testcase(mi, ma, sign):
    tc = ''
    for i in range(10):
        # tong so tu
        word_size = random.randint(mi, ma)
        numbers = []
        for j in range(word_size):
            # so chu cai moi tu
            letter_size = random.randint(mi, ma)
            numbers.append(random.randint(
                10 ** (letter_size - 1), 10 ** letter_size - 1))
        if sign == '+':
            numbers.append(sum(numbers))
        elif sign == '-':
            letter_size = random.randint(mi, ma)
            numbers.append(random.randint(
                10 ** (letter_size - 1), 10 ** letter_size - 1))
            numbers[0] = sum(numbers[1:])
        numbers = list(map(lambda x: str(x), numbers))
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
        tc += sign.join(numbers[:-1]) + '=' + numbers[-1] + '\n'
    open('input.txt', 'w').write(tc[:-1])


def read_input():
    raw_inps = open('input.txt', 'r').read().split('\n')
    symbols = set({'+', '-', '*', '=', ')', '('})
    inps = []
    for line in raw_inps:
        pre_sign_pos = -1
        cur_sign_pos = 0
        is_sign_change = False
        signs = []
        inp = []
        first_sign = line[0]
        if first_sign == '(':
            first_sign = line[1]
        if first_sign == '-':
            signs.append(first_sign)
        else:
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
        if line[pre_sign_pos] != '=':
            signs.append(line[pre_sign_pos])
        else:
            signs.append('+')
        inp.append(line[pre_sign_pos + 1:])
        inps.append((inp, signs))
    return inps


if __name__ == '__main__':
    print(read_input())
