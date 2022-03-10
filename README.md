# numprog-scripts
Scripts for performing some tasks related to numerical programming with pretty ASCII printing of the table.

Usage: Edit the points in `interpolation.py` and run the python file.

## Newton Interpolation

Input: sample points

Output: calculation table & interpolation polynomial

```pyhon
interpolate_newton([(0, 1), (2, -2), (4, 3)])
```

```sh
  x_i  | i\k ||  0   |       1        |       2        |
------------------------------------------------------
       |     ||      | -2 - 1         | 5/2 + 3/2      |
   0   |  0  ||  1   | ------ = -3/2  | --------- = 1  |
       |     ||      | 2 - 0          |   4 - 0        |
---------------------------------------------------------
       |     ||      | 3 + 2          |
   2   |  1  ||  -2  | ----- = 5/2    |
       |     ||      | 4 - 2          |
----------------------------------------
       |     ||      |
   4   |  2  ||  3   |
       |     ||      |
-----------------------
Polynomial:
p(x) = 1 + -3/2(x - 0) + 1(x - 0)(x - 2)
```

## Aitken-Neville Interpolation

Input: sample points & point for evaluation

Output: calculation table, interpolation polynomial & evaluated value

```python
interpolate_aitken_neville([(0, 3), (1, 0), (2, 1)], 0.5)
```

```sh
  x_i  | i\k ||  0  |              1                |                2                  |
---------------------------------------------------------------------------------------
       |     ||     |     1/2 - 0                   |       1/2 - 0                     |
   0   |  0  ||  3  | 3 + ------- * (0 - 3) = 3/2   | 3/2 + ------- * (-1/2 - 3/2) = 1  |
       |     ||     |      1 - 0                    |        2 - 0                      |
------------------------------------------------------------------------------------------
       |     ||     |     1/2 - 1                   |
   1   |  1  ||  0  | 0 + ------- * (1 - 0) = -1/2  |
       |     ||     |      2 - 1                    |
------------------------------------------------------
       |     ||     |
   2   |  2  ||  1  |
       |     ||     |
----------------------
Polynomial:
p(x) =
      1/2 - 0
3/2 + ------- * (-1/2 - 3/2) = 1
       2 - 0
```

## Romberg Integration
**WIP**
