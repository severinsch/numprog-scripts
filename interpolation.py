
from fractions import Fraction
from typing import Union
from utils import print_table, Cell, ValueCell, NewtonCalcCell, AitkenNevilleCalcCell, RombergTSCell, RombergCell


def interpolate_newton(points: [(Union[float, Fraction], Union[float, Fraction])]):
    points = list(map(lambda p: (Fraction(p[0]).limit_denominator(10000), Fraction(p[1]).limit_denominator(10000)),
                      points))

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


def interpolate_aitken_neville(points: [(Union[float, Fraction], Union[float, Fraction])], x: float):
    points = list(map(lambda p: (Fraction(p[0]).limit_denominator(10000),Fraction(p[1]).limit_denominator(10000)),
                      points))
    x = Fraction(x)

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


# def calculate_romberg_f(f, a, b, h):
#     table: [[Cell]] = [[Cell() for _ in range(a,b+1,h)] for _ in range(a,b+1,h``)]
#
#     for i in range(a,b+1,h):
#         table[0][i] = RombergTSCell(f, h, a, b)
#
#     for column in range(1, len(points)):
#         for row in range(len(points) - column - 1, -1, -1):
#
# def calculate_romberg_points():

# interpolate_aitken_neville([(0, 3), (1, 0), (2, 1)], 0.5)
interpolate_newton([(-2, 1), (0, -2), (2, 3)])
