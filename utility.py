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

# take in a string line and the index of the opening bracket "("
# replace the bracket line with no bracket
def removeBrackets(line, i):
    if line[i-1] == "-":    # remove bracket for

        signs = set({'+', '-', '(', ')'})
        e = i
        while line[e] != ')':
            e += 1    

            f = 0
            # find the sign
            while line[f] not in signs:
                f += 1

            # change sign after found
            if line[f] == "+":
                line[f] = "-"
            elif line[f] == "-":
                line[f] = "+"
            elif line[f] == "(":    # remove brackets inside current one
                removeBrackets(line, f)
            
            if e <= f:
                e = f
        
    j = i
    while line[j] != ')':
        j += 1    
    sub = line[i:j]
    new_sub = sub.replace("(","")
    new_sub = new_sub.replace(")","")
    line = line[:i] + new_sub + line[j:]
    # return line

def read_input():
    raw_inputs = open('input.txt', 'r').read().split('\n')
    signs = set({'+', '-', 'x'})
    inputs = []
    sign_set = []
    for line in raw_inputs:
        i = 0
        while line[i] not in signs:
            if line[i] == "(":
                removeBrackets(line,i)
            i += 1

        for c in line:
            if c in signs:
                sign_set.append(c)

        inputs.append((re.split(r'[-+=]', line), sign_set))
    return inputs
