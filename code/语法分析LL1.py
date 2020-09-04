"""
 文法：
    E->E+T | T
    T->T*F | F
    F->(E)|i
 消除左递归：
    E->TH       (H代替E')
    H->+TH|e    (e替代空)
    T->FY       (Y代替T')
    Y->*FY|e
    F->(E)|i
 非终结符：
    E，H，T，Y，F
 终结符:
    i,+,*,(,),#
"""

import re
from prettytable import PrettyTable
table = PrettyTable(["步骤", "分析栈", "当前入栈", "剩余输入串", "所用产生式"])

# 构造预测分析表
dists = {
    ('E', 'i'): 'TH', ('E', '('): 'TH', ('H', '+'): '+TH',
    ('H', ')'): 'e', ('H', '#'): 'e', ('T', 'i'): 'FY',
    ('T', '('): 'FY', ('Y', '+'): 'e', ('Y', '*'): '*FY',
    ('Y', ')'): 'e', ('Y', '#'): 'e', ('F', 'i'): 'i',
    ('F', '('): '(E)',
}

# 构造终结符集合
Vt = ('i', '+', '*', '(', ')')

# 构造非终结符集合
Vh = ('E', 'H', 'T', 'Y', 'F')


# 总控程序
def main(sentence):
    '''总控程序，用于进程文法的判断'''
    # 用列表模拟栈
    stack = []
    location = 0
    # 将#号入栈
    stack.append(sentence[location])

    # 将文法开始符入栈
    stack.append('E')
    # 将输入串第一个字符读进a中
    location += 1
    input_bottom = sentence[location]

    count = 1  # 计算步骤
    table.add_row([count, ''.join(stack),
                   input_bottom, sentence[location:], ''])
    stack_top = ''
    cell = ''
    while True:
        count += 1
        stack_top = stack.pop()
        if stack_top in Vt:  # 栈顶是终结符
            if stack_top == sentence[location]:  # 该字符匹配，输入串向后挪一位
                location += 1
                input_bottom = sentence[location]
            else:  # 否则错误
                raise Exception("未知字符错误")
            table.add_row([count, ''.join(stack), input_bottom,
                           sentence[location:], ''])
        else:
            if stack_top == '#' and stack_top == input_bottom:  # 栈顶是结束符且当前输入字符也是结束符，分析结束
                break
            elif (stack_top, input_bottom) in dists.keys():  # M[x,a]是产生式
                cell = dists[(stack_top, input_bottom)]
                for i in range(len(cell) - 1, -1, -1):  # 倒序入栈
                    if cell[i] != 'e':
                        stack.append(cell[i])
            else:
                raise Exception("未知错误")
            expr = stack_top + '->' + cell
            table.add_row([count, ''.join(stack), input_bottom,
                           sentence[location:], expr])


if __name__ == '__main__':
    sentence = '#i+i*i#'
    main(sentence)
    # 设置左对齐
    for key in table.align.keys():
        table.align[key] = 'l'
    print(table)
