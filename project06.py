import dicts as d
import os
import re

END_NAME_FILE = '.hack'

NONE_STR = ''

START_NUM = 2

NUM_OF_BITS = 15

AT_BIT = '0'

SYMBOL = '@\w*'

COMMENT = '\/\/.*'

REGEX = "([ADM0]*)((=[A-Z\d+-/!/|/&]*)|(;[A-Z]*))"
AT_VAL_R = "@[a-zA-Z0-9]*"
VAR = '\(\w*\)'


def parse_line(line, pattern, at_val):
    """
    A function that gets line and parse it with regex
    :param line:
    :param pattern:
    :param at_val:
    :return:
    """
    if re.findall(at_val, line):
        result = at_val.match(line)
        con_l = convert_at_val(result)
    elif re.findall(pattern, line):
        result = pattern.match(line)
        dest = result.group(1)
        comp = result.group(3)
        jump = result.group(4)
        con_l = convert_instruction(dest, comp, jump)
    else:
        con_l = None
    return con_l


def remove_invalid_syntax(line):
    com = re.compile(COMMENT)
    result = com.match(line)
    if result is not None:
        s, e = result.span()
        line = line[:s]
    line = line.replace("\n", "")
    line = line.replace(" ", "")
    return line


def convert_at_val(exp):
    """
    convert the at value instruction to bits
    :param exp: the expration to convert
    :return: the instruction in bits
    """
    res = AT_BIT
    x = exp.group()
    x = bin(int(x[1:]))[START_NUM:]
    x_len = len(x)
    res = res + (AT_BIT * (NUM_OF_BITS - x_len)) + str(x)
    return res

def convert_instruction(dest, comp, jump):
    """
    A function that cinvert instruction line to bits
    :param dest: the destination instruction part
    :param comp: the comperation instruction part
    :param jump: the jump instruction part
    :return: the instruction in bits
    """
    res = '111'
    if jump is None:
        jump = NONE_STR
    elif jump[0] == ';':
        jump = jump[1:]
    if comp is None:
        comp = dest
        dest = NONE_STR
    if comp[0] == '=':
        comp = comp[1:]
    res = res + d.comp[comp] + d.dest[dest] + d.jump[jump]
    return res

def first_loop(f):
    var = re.compile(VAR)
    for i in range(len(f)):
        result = var.match(f[i])
        if result is not None:
            new_line = '@' + str(i+1)
            s = result.string
            new_key = s[1: len(s) - 1]
            d.symbols[new_key] = new_line
            f[i] = new_line
    return f

def second_loop(f):
    counter = 16
    s = re.compile(SYMBOL)
    for i in range(len(f)):
        result = s.match(f[i])
        if result is not None:
            res = result.string[1:]
            if res in d.symbols.keys():
                f[i] = '@' + str(d.symbols[res])
            else:
                new_key = res
                new_val = '@' + str(counter)
                counter += 1
                d.symbols[new_key] = new_val
                f[i] = new_val
    return f


def main(path):
    pattern1 = re.compile(REGEX)
    at_val = re.compile(AT_VAL_R)
    file = open(path, 'r')
    name = os.path.basename(path)
    name = name.replace(".asm", ".hack")
    parse_file = open(path + END_NAME_FILE, 'w')
    line = file.readline()
    f = []
    while line:
        l = remove_invalid_syntax(line)
        if l != '':
            f.append(l)
        line = file.readline()
    f = first_loop(f)
    f = second_loop(f)
    for l in f:
        if l is None:
            continue
        p_line = parse_line(l, pattern1, at_val)
        if p_line is not None:
            parse_file.write(p_line)
            parse_file.write("\n")
    file.close()
    parse_file.close()

# pattern1 = re.compile(REGEX)
# at_val = re.compile(AT_VAL_R)
# print(parse_line('@3', pattern1, at_val))

    # get file relative or not
    # open file.hack
    #read the file - if the line if empty delete. mybe parse the line? comments
    # write the atribute in the new file
    #colse files
main("Max.asm")