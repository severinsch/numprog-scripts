import math
from fractions import Fraction


class Cell:
    # value: int
    # numerator: str
    # line: str
    # denominator: str

    def __init__(self):
        self.value = 0
        self.numerator = ''
        self.line = ''
        self.denominator = ''
        self.empty = True

    def __str__(self):
        return "\n".join([self.numerator, self.line, self.denominator])


class ValueCell(Cell):

    def __init__(self, value):
        super().__init__()
        self.value = value

        self.numerator = ' '
        self.denominator = ' '
        self.line = str(self.value)
        self.empty = False


class NewtonCalcCell(Cell):
    # c1 = c_i+1,k-1
    # c2 = c_i,k-1
    # x1 = x_i+k
    # x2 = x_i
    def __init__(self, c1, c2, x1, x2):
        super().__init__()
        self.c1 = c1
        self.c2 = c2
        self.x1 = x1
        self.x2 = x2
        self.value = Fraction((c1 - c2), (x1 - x2))
        self.empty = False

        numerator = f"{self.c1} {'-' if self.c2 >= 0 else '+'} {abs(self.c2)}"
        denominator = f"{self.x1} {'-' if self.x2 >= 0 else '+'} {abs(self.x2)}"

        if len(numerator) < len(denominator):
            numerator = f'{numerator:^{len(denominator)}}'
        elif len(denominator) < len(numerator):
            denominator = f'{denominator:^{len(numerator)}}'

        self.numerator = numerator
        self.denominator = denominator
        self.line = max(len(numerator), len(denominator)) * '-' + f' = {self.value}'


class AitkenNevilleCalcCell(Cell):

    def __init__(self, p1, p2, x1, x2, x):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.x1 = x1
        self.x2 = x2
        self.x = x
        self.value = p1 + Fraction((x - x1), (x2 - x1)) * (p2 - p1)
        self.empty = False

        numerator = f"{self.x} {'-' if self.x1 >= 0 else '+'} {abs(self.x1)}"
        denominator = f"{self.x2} {'-' if self.x1 >= 0 else '+'} {abs(self.x1)}"

        if len(numerator) < len(denominator):
            numerator = f'{numerator:^{len(denominator)}}'
        elif len(denominator) < len(numerator):
            denominator = f'{denominator:^{len(numerator)}}'
        line = max(len(numerator), len(denominator)) * '-'
        first_part = f'{p1} + '
        last_part = f' * ({p2} - {p1})'
        self.numerator = len(first_part) * ' ' + numerator + len(last_part) * ' '
        self.denominator = len(first_part) * ' ' + denominator + len(last_part) * ' '
        self.line = first_part + line + last_part + f' = {self.value}'


class RombergTSCell(Cell):

    def __init__(self, f, h, a, b):
        super().__init__()
        self.f = f
        self.h = h
        self.a = a
        self.b = b

        self.numerator = ''
        self.denominator = ''
        self.line = str(h) + '*( '

        val = 0
        val_str = ''
        for i in range(a, b+1, h):
            if i == a:
                val += f(i)/2
                val_str += f'f({i})/2 + '
            if i == b:
                val += f(i)/2
                val_str += f'f({i})/2 )'
            val += f(i)
            val_str += f'f({i})'

        val *= h
        self.value = Fraction(val).limit_denominator(10000)
        self.line = val_str + f' = {self.value}'


class RombergCell(Cell):

    def __init__(self, Qlinks, Qlinksoben, hganzlinksoben, hlinks):
        super().__init__()
        self.Qlinks = Qlinks
        self.Qlinksoben = Qlinksoben
        self.hganzlinksoben = hganzlinksoben
        self.hlinks = hlinks

        self.value = Qlinks + Fraction((Qlinks-Qlinksoben), (hganzlinksoben/hlinks)**2 - 1).limit_denominator(1000000)
        numerator = f'{Qlinks} - {Qlinksoben}'
        denominator = f'({hganzlinksoben}/{hlinks}² -1'

        if len(numerator) < len(denominator):
            numerator = f'{numerator:^{len(denominator)}}'
        elif len(denominator) < len(numerator):
            denominator = f'{denominator:^{len(numerator)}}'

        line = max(len(numerator), len(denominator)) * '-'
        first_part = f'{Qlinks} + '
        self.numerator = len(first_part) * ' ' + numerator
        self.denominator = len(first_part) * ' ' + denominator
        self.line = first_part + line + f' = {self.value}'


def print_table(table: [[Cell]], points: [(int, int)], aitken: bool):
    max_widths: [int] = list(map(lambda a: len(max(a, key=lambda c: len(c.line)).line) + 2, table))
    # all cell widths,      start,           all |
    line_length = sum(max_widths) + len('x_i | i\\k |') + len(table) * 3
    result = '  x_i  | i\\k || ' + ''.join([f'{str(i):^{max_widths[i]}} |' for i in range((len(table)))]) + '\n'
    result += '-' * line_length + '\n'
    for row_part in range(4 * len(table)):
        row = math.floor(row_part / 4)

        match row_part % 4:
            case 0:
                result += f'       |     || '
            case 1:
                spaces = 7 - len(str(points[row][0]))
                result += (spaces//2)*' ' + f'{points[row][0]}' + (spaces//2)*' ' + f'|  {row}  || '
            case 2:
                result += f'       |     || '
            case 3:
                result += 14 * '-'

        for column in range(len(table)):
            cell = table[column][row]
            if not (isinstance(cell, ValueCell) or
                    isinstance(cell, NewtonCalcCell) or
                    isinstance(cell, AitkenNevilleCalcCell)) or cell.empty:
                result += (max_widths[column] + 3) * ' ' if row_part % 4 != 3 else '-'
            else:
                match row_part % 4:
                    case 0:
                        result += f' {cell.numerator}' + (max_widths[column] - len(cell.numerator)) * ' ' + '|'
                    case 1:
                        result += f' {cell.line}' + (max_widths[column] - len(cell.line)) * ' ' + '|'
                    case 2:
                        result += f' {cell.denominator}' + (max_widths[column] - len(cell.denominator)) * ' ' + '|'
                    case 3:
                        result += (max_widths[column] + 3) * '-'
        result += '\n'

    result += 'Polynomial:\n'
    if aitken:
        result += 'p(x) =\n' + str(table[len(table)-1][0])
    else:
        polynomial_parts = []
        for i in range(len(table)):
            part = ''
            part += f'{table[i][0].value}'
            for j in range(0, i):
                part += f'(x - {points[j][0]})'
            polynomial_parts.append(part)
        result += 'p(x) = ' + ' + '.join(polynomial_parts)
    print(result)
