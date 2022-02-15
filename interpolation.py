import math


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

    def __str__(self):
        return "\n".join([self.numerator, self.line, self.denominator])


class ValueCell(Cell):

    def __init__(self, value):
        super().__init__()
        self.value = value

        self.numerator = ' '
        self.denominator = ' '
        self.line = str(self.value)


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
        self.value = (c1 - c2) / (x1 - x2)

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
        self.value = p1 + ((x - x1) / (x2 - x1)) * (p2 - p1)

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


def print_table(table: [[Cell]], points: [(int, int)], aitken: bool):
    max_widths: [int] = list(map(lambda a: len(max(a, key=lambda c: len(c.line)).line) + 2, table))
    # all cell widths,      start,           all |
    line_length = sum(max_widths) + len('x_i | i\\k |') + len(table) * 3
    result = ' x_i | i\\k | ' + ''.join([f'{str(i):^{max_widths[i]}} |' for i in range((len(table)))]) + '\n'
    result += '-' * line_length + '\n'
    for row_part in range(4 * len(table)):
        row = math.floor(row_part / 4)

        match row_part % 4:
            case 0:
                result += f'     |     | '
            case 1:
                result += f'  {points[row][0]}  |  {row}  | '
            case 2:
                result += f'     |     | '
            case 3:
                result += 13 * '-'

        for column in range(len(table)):
            cell = table[column][row]
            if not (isinstance(cell, ValueCell) or isinstance(cell, NewtonCalcCell) or isinstance(cell, AitkenNevilleCalcCell)):
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


def interpolate_newton(points: [(float, float)]):
    xs = list(map(lambda p: p[0], points))

    table: [[Cell]] = [[Cell() for _ in range(len(points))] for _ in range(len(points))]

    for i in range(len(points)):
        table[0][i] = ValueCell(points[i][1])

    for column in range(1, len(points)):
        for row in range(len(points) - column - 1, -1, -1):
            c1 = table[column - 1][row + 1].value
            c2 = table[column - 1][row].value
            x1 = xs[row + column]
            x2 = xs[row]
            table[column][row] = NewtonCalcCell(c1, c2, x1, x2)

    print_table(table, points, False)


def interpolate_aitken_neville(points: [(float, float)], x: float):
    xs = list(map(lambda p: p[0], points))

    table: [[Cell]] = [[Cell() for _ in range(len(points))] for _ in range(len(points))]

    for i in range(len(points)):
        table[0][i] = ValueCell(points[i][1])

    for column in range(1, len(points)):
        for row in range(len(points) - column - 1, -1, -1):
            p1 = table[column - 1][row].value
            p2 = table[column - 1][row + 1].value
            x1 = xs[row]
            x2 = xs[row + column]
            table[column][row] = AitkenNevilleCalcCell(p1, p2, x1, x2, x)

    print_table(table, points, True)


# interpolate_aitken_neville([(0, 3), (1, 0), (2, 1)], 0.5)
interpolate_newton([(0, 3), (1, 0), (2, 1)])
