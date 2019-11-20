import dicts as d
import os
import re

END_NAME_FILE = '.hack'

NONE_STR = ''

START_NUM = 2

NUM_OF_BITS = 15

AT_BIT = '0'

REGEX = "([ADM0]*)((=[A-Z\d/+/-/!/|/&]*)|(;[A-Z]*))"
AT_VAL_R = "@[a-zA-Z0-9]*"


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

def main(file):
    pattern1 = re.compile(REGEX)
    at_val = re.compile(AT_VAL_R)
    file = open(file, 'r')
    name = os.path.basename(file)
    parse_file = open(str(name) + END_NAME_FILE, 'w')
    line = file.readline()
    while line:
        p_line = parse_line(line, pattern1, at_val)
        parse_file.write(p_line)
        line = file.readline()
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
