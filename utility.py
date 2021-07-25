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
    raw_inputs = open('input.txt', 'r').read().split('\n')
    signs = set({'+', '-', 'x'})
    inputs = []
    for line in raw_inputs:
        i = 0
        while line[i] not in signs:
            i += 1
        inputs.append((re.split(r'[-+=]', line), line[i]))
    return inputs
