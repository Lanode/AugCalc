from math_ast import MathAST
from calculator import calculate
from utils import *

class Quadrature:
    """Базовые определения для квадратурных формул"""
    __sum = 0.0
    __nseg = 1  # число отрезков разбиения
    __ncalls = 0 # считает число вызовов интегрируемой функции
    __var: str

    def __restart(func, x0, x1, nseg0, reset_calls = True):
        """Обнуление всех счётчиков и аккумуляторов.
           Возвращает интеграл методом трапеций на начальном разбиении"""
        if reset_calls:
            Quadrature.__ncalls = 0
        Quadrature.__nseg = nseg0
        # вычисление суммы для метода трапеций с начальным числом отрезков разбиения nseg0
        Quadrature.__sum = 0.5 * (calculate(func, **{Quadrature.__var: x0}) + calculate(func, **{Quadrature.__var: x1}))
        dx = 1.0 * (x1 - x0) / nseg0
        for i in range(1, nseg0):
            Quadrature.__sum += calculate(func, **{Quadrature.__var: x0 + i * dx})

        Quadrature.__ncalls += 1 + nseg0
        return Quadrature.__sum * dx

    def __double_nseg(func, x0, x1):
        """Вдвое измельчает разбиение.
           Возвращает интеграл методом трапеций на новом разбиении"""
        nseg = Quadrature.__nseg
        dx = (x1 - x0) / nseg
        x = x0 + 0.5 * dx
        i = 0
        AddedSum = 0.0
        for i in range(nseg):
            AddedSum += calculate(func, **{Quadrature.__var: x + i * dx})

        Quadrature.__sum += AddedSum
        Quadrature.__nseg *= 2
        Quadrature.__ncalls += nseg
        return Quadrature.__sum * 0.5 * dx

    def trapezoid(func: MathAST, var: str, x0: float, x1: float, rtol = 1e-10, nseg0 = 1) -> float:
        """Интегрирование методом трапеций с заданной точностью.
           rtol - относительная точность,
           nseg0 - число отрезков начального разбиения"""
        Quadrature.__var = var
        ans = Quadrature.__restart(func, x0, x1, nseg0)
        old_ans = 0.0
        err_est = max(1, abs(ans))
        while (err_est > abs(rtol * ans)):
            old_ans = ans
            ans = Quadrature.__double_nseg(func, x0, x1)
            err_est = abs(old_ans - ans)

        return ans

    def simpson(func: MathAST, var: str, x0: float, x1: float, rtol = 1.0e-10, nseg0 = 1) -> float:
        """Интегрирование методом парабол с заданной точностью.
           rtol - относительная точность,
           nseg0 - число отрезков начального разбиения"""
        Quadrature.__var = var
        old_trapez_sum = Quadrature.__restart(func, x0, x1, nseg0)
        new_trapez_sum = Quadrature.__double_nseg(func, x0, x1)
        ans = (4 * new_trapez_sum - old_trapez_sum) / 3
        old_ans = 0.0
        err_est = max(1, abs(ans))
        while (err_est > abs(rtol * ans)):
            old_ans = ans
            old_trapez_sum = new_trapez_sum
            new_trapez_sum = Quadrature.__double_nseg(func, x0, x1)
            ans = (4 * new_trapez_sum - old_trapez_sum) / 3
            err_est = abs(old_ans - ans)

        #print("Total function calls: " + str(Quadrature.__ncalls))
        return ans

def detect_vars_and_simp(f: MathAST, x0: float, x1: float) -> MathAST:
    v = detect_vars(f)
    if len(v) > 1:
        raise Exception('Integral error: function have 2 or more variables')
    if len(v) == 1:
        return Quadrature.simpson(f, v[0].name, x0, x1)
    else:
        return Quadrature.simpson(f, '', x0, x1)
