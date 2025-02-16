import sys
import math
import os.path
import csv

import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from menu import Ui_MainWindow as Menu_ui
from calculator import Ui_Form as Calculator_ui
from polynoms import Ui_widget as Polynoms_ui
from graphics import Ui_Form as Graphics_ui
from test import Ui_Form as Test_ui


class Menu(QMainWindow, Menu_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_to_calculator.clicked.connect(self.calculator_func)
        self.button_to_graphics.clicked.connect(self.graphics_func)
        self.button_to_polynoms.clicked.connect(self.polynoms_func)
        self.button_to_test.clicked.connect(self.test_func)

    def calculator_func(self):
        self.calculator_form = Calculator(self)
        self.calculator_form.show()
        self.hide()

    def graphics_func(self):
        self.graphics_form = Graphics(self)
        self.graphics_form.show()
        self.hide()

    def polynoms_func(self):
        self.equations_form = Polynoms(self)
        self.equations_form.show()
        self.hide()

    def test_func(self):
        self.test_form = Test(self)
        self.test_form.show()
        self.hide()


class Calculator(QWidget, Calculator_ui):
    def __init__(self, *args):
        super().__init__()
        self.flag = 0
        self.main = args[0]
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculator')

        self.numbers = [self.b_0, self.b_1, self.b_2, self.b_3,
                        self.b_4, self.b_5, self.b_6, self.b_7, self.b_8, self.b_9]
        for i in range(0, 10):
            self.numbers[i].clicked.connect(self.run)
        self.operations = [self.div, self.multiply, self.minus, self.plus]
        for button in self.operations:
            button.clicked.connect(self.run)

        self.exit_button.clicked.connect(self.go_back)
        self.dot.clicked.connect(self.run)
        self.eq.clicked.connect(self.result)
        self.unar.clicked.connect(self.sign)
        self.part_clear.clicked.connect(self.last_clear)
        self.every_clear.clicked.connect(self.all_clear)
        self.b_factorial.clicked.connect(self.factorial)
        self.b_power.clicked.connect(self.power)
        self.b_sqrt.clicked.connect(self.root)
        self.b_logarithm.clicked.connect(self.logarithm)

    def go_back(self):
        self.main.show()
        self.hide()

    def run(self):
        if self.sender() in self.operations:
            self.flag = 1
        if self.flag == 0:
            number = self.calcul.text()
            number += self.sender().text()
            self.calcul.setText(number)
        elif self.flag == 2:
            self.calcul.setText(self.sender().text())
            self.flag = 0
        elif self.flag == 3:
            self.calcul.setText(str(float(self.calcul.text()[:-1]) ** int(self.sender().text())))
        else:
            number = self.calcul.text()
            oper = self.sender().text()
            self.upper.setText(number + oper)
            self.flag = 2

    def result(self):
        expression = self.upper.text() + self.calcul.text()
        self.upper.setText('')
        if '/' in expression and expression[-1] == '0':
            self.calcul.setText('ERROR')
        else:
            res = str(eval(expression))
            self.calcul.setText(res)

    def sign(self):
        number = self.calcul.text()
        if number[0] != '-':
            number = '-' + number
        else:
            number = number[1:]
        self.calcul.setText(number)

    def last_clear(self):
        self.calcul.setText('0')
        self.flag = 2

    def all_clear(self):
        self.calcul.setText('')
        self.upper.setText('')
        self.flag = 0

    def factorial(self):
        try:
            number = math.factorial(float(self.calcul.text()))
            self.calcul.setText(str(number))
        except ValueError:
            self.calcul.setText('ERROR')

    def power(self):
        self.flag = 3
        self.calcul.setText(self.calcul.text() + '^')

    def root(self):
        try:
            self.calcul.setText(str(float(math.sqrt(float(self.calcul.text())))))
        except ValueError:
            self.calcul.setText('ERROR')

    def logarithm(self):
        number = math.log1p(float(self.calcul.text()))
        self.calcul.setText(str(number))


class Graphics(QWidget, Graphics_ui):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.main = args[0]
        self.initUi()

    def initUi(self):
        self.setWindowTitle('Graphics')
        self.draw_button.clicked.connect(self.draw_graphic)
        self.exit_button.clicked.connect(self.go_back)

    def go_back(self):
        self.main.show()
        self.hide()

    def draw_graphic(self):
        func = self.func_input.text()
        for el in [self.red, self.green, self.blue]:
            if el.isChecked():
                colour = el.text()[0].lower()
        try:
            func = ''.join([_ for _ in func if _ != ' '])
            func = func.replace('^', '**')
            if any([True for sym in func if sym in '=!@#$%&_"№:?`~' or
                                            sym in 'scotqweryupdfghjklzvbnmйцукенгшщзфывапролджэячсмитьбюхё']):
                raise ValueError
            self.widget.clear()
            self.widget.plot([i for i in range(-100, 100)],
                             [eval(func.replace('x', str(x))) for x in range(-100, 100)], pen=colour)
        except ValueError:
            self.error_messenger.setText('Неверно введена функция')


class Polynoms(QWidget, Polynoms_ui):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.power = 0
        self.main = args[0]
        self.power_2 = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Polynom calculator')
        self.power_input_button.clicked.connect(self.polynom_input)
        self.line_edits = [self.le0, self.le1, self.le2, self.le3, self.le4]
        self.labels = [self.l0, self.l1, self.l2, self.l3, self.l4]
        self.line_edits_2 = [self.le0_2, self.le1_2, self.le2_2, self.le3_2, self.le4_2]
        self.labels_2 = [self.l0_2, self.l1_2, self.l2_2, self.l3_2, self.l4_2]

        self.exit_button.clicked.connect(self.go_back)
        self.roots_button.clicked.connect(self.find_roots)
        self.derivative_button.clicked.connect(self.derivative)
        self.polynom_value_button.clicked.connect(self.polynom_value)
        self.start_over_button.clicked.connect(self.start_over)
        self.power_polynom_button.clicked.connect(self.power_polynom)
        self.add_polynom_button.clicked.connect(self.add_polynom)
        self.sum_polynom_button.clicked.connect(self.sum_polynom)
        self.substraction_polynom_button.clicked.connect(self.substraction_polynom)
        self.multiplication_polynom_button.clicked.connect(self.multiplication_polynom)
        self.compare_button.clicked.connect(self.compare)
        self.start_over()

    def go_back(self):
        self.main.show()
        self.hide()

    def polynom_input(self):
        self.power, ok_pressed = QInputDialog.getInt(self, "Степень многочлена",
                                                     "Введите степень многочлена:", 1, 1, 4, 1)
        self.power = int(self.power)
        for i in range(self.power + 1):
            self.line_edits[i].show()
            self.labels[i].show()
        self.roots_button.show()
        self.derivative_button.show()
        self.polynom_value_button.show()
        self.power_polynom_button.show()
        self.add_polynom_button.show()

    def power_polynom(self):
        n, ok_pressed = QInputDialog.getInt(self, 'Возвести в степень',
                                                 "Введите натуральную степень многочлена:", 1, 1, 6, 1)
        if ok_pressed:
            try:
                coeffs = [float(self.line_edits[i].text()) for i in range(self.power + 1)][::-1]
                polynom = Polynom(coeffs)
                if float(int(n)) != float(n):
                    raise ValueError
                result = polynom.__pow__(n)
                self.polynom_power_output.show()
                self.polynom_power_output.setText(result.__str__())
            except ValueError:
                self.error_message.setText('WRONG COEFFICIENTS OR POWER TYPE')

    def find_roots(self):
        try:
            coeffs = [float(self.line_edits[i].text()) for i in range(self.power + 1)][::-1]
            polynom = Solver(Polynom(coeffs))
            roots = list(map(str, polynom.find_roots()))
            self.roots_output.show()
            if roots:
                self.roots_output.setPlainText('\n'.join(roots))
            else:
                self.roots_output.setPlainText('This equation has no real solutions')
        except ValueError:
            self.error_message.setText('WRONG COEFFICIENTS TYPE')

    def derivative(self):
        try:
            coeffs = [float(self.line_edits[i].text()) for i in range(self.power + 1)][::-1]
            polynom = Polynom(coeffs)
            derivative = polynom.derivative().__str__()
            self.derivative_output.show()
            self.derivative_output.setText(derivative)
        except ValueError:
            self.error_message.setText('WRONG COEFFICIENTS TYPE')

    def polynom_value(self):
        try:
            coeffs = [float(self.line_edits[i].text()) for i in range(self.power + 1)][::-1]
            x, ok_pressed = QInputDialog.getText(self, "Значение полинома", "Введите значение Х")
            if ok_pressed:
                polynom = Polynom(coeffs)
                result = polynom.value(float(x))
                self.result.show()
                self.result.setText(str(result))
        except ValueError:
            self.error_message.setText('WRONG COEFFICIENTS OR X VALUE TYPE')

    def add_polynom(self):
        self.power_2, ok_pressed = QInputDialog.getInt(self, "Степень многочлена",
                                                     "Введите степень многочлена:", 1, 1, 4, 1)
        self.power_2 = int(self.power_2)
        for i in range(len(self.line_edits_2)):
            self.line_edits_2[i].hide()
            self.labels_2[i].hide()
        for i in range(self.power_2 + 1):
            self.line_edits_2[i].show()
            self.labels_2[i].show()
        self.sum_polynom_button.show()
        self.multiplication_polynom_button.show()
        self.substraction_polynom_button.show()
        self.compare_button.show()

    def sum_polynom(self):
        try:
            coeffs = [float(self.line_edits[i].text()) for i in range(self.power + 1)][::-1]
            coeffs_2 = [float(self.line_edits_2[i].text()) for i in range(self.power_2 + 1)][::-1]
            if len(coeffs) > len(coeffs_2):
                coeffs_2 = [0] * (len(coeffs) - len(coeffs_2)) + coeffs_2
            else:
                coeffs = [0] * (len(coeffs_2) - len(coeffs)) + coeffs
            polynom_1, polynom_2 = Polynom(coeffs), Polynom(coeffs_2)
            result = polynom_1 + polynom_2
            self.sum_polynom_output.show()
            self.sum_polynom_output.setText(result.__str__())
        except ValueError:
            self.error_message.setText('WRONG COEFFICIENTS TYPE')

    def substraction_polynom(self):
        try:
            coeffs = [float(self.line_edits[i].text()) for i in range(self.power + 1)][::-1]
            coeffs_2 = [float(self.line_edits_2[i].text()) for i in range(self.power_2 + 1)][::-1]
            if len(coeffs) > len(coeffs_2):
                coeffs_2 = [0] * (len(coeffs) - len(coeffs_2)) + coeffs_2
            else:
                coeffs = [0] * (len(coeffs_2) - len(coeffs)) + coeffs
            polynom_1, polynom_2 = Polynom(coeffs), Polynom(coeffs_2)
            result = polynom_1 - polynom_2
            self.substraction_polynom_output.show()
            self.substraction_polynom_output.setText(result.__str__())
        except ValueError:
            self.error_message.setText('WRONG COEFFICIENTS TYPE')

    def multiplication_polynom(self):
        try:
            coeffs = [float(self.line_edits[i].text()) for i in range(self.power + 1)][::-1]
            coeffs_2 = [float(self.line_edits_2[i].text()) for i in range(self.power_2 + 1)][::-1]
            polynom_1, polynom_2 = Polynom(coeffs), Polynom(coeffs_2)
            result = polynom_1 * polynom_2
            self.multiplication_polynom_output.show()
            self.multiplication_polynom_output.setText(result.__str__())
        except ValueError:
            self.error_message.setText('WRONG COEFFICIENTS TYPE')

    def compare(self):
        try:
            coeffs = [float(self.line_edits[i].text()) for i in range(self.power + 1)][::-1]
            coeffs_2 = [float(self.line_edits_2[i].text()) for i in range(self.power_2 + 1)][::-1]
            polynom_1, polynom_2 = Polynom(coeffs), Polynom(coeffs_2)
            self.compare_output.show()
            if polynom_1 == polynom_2:
                self.compare_output.setText('polynom_1 = polynom_2')
            else:
                self.compare_output.setText('polynom_1 != polynom_2')
        except ValueError:
            self.error_message.setText('WRONG COEFFICIENTS TYPE')

    def start_over(self):
        for i in range(len(self.line_edits)):
            self.line_edits[i].hide()
            self.line_edits[i].setText('')
            self.labels[i].hide()
            self.line_edits_2[i].hide()
            self.line_edits_2[i].setText('')
            self.labels_2[i].hide()
        self.error_message.setText('')
        self.roots_button.hide()
        self.derivative_button.hide()
        self.polynom_value_button.hide()
        self.roots_output.hide()
        self.derivative_output.hide()
        self.result.hide()
        self.power_polynom_button.hide()
        self.polynom_power_output.hide()
        self.add_polynom_button.hide()
        self.sum_polynom_button.hide()
        self.substraction_polynom_button.hide()
        self.multiplication_polynom_button.hide()
        self.substraction_polynom_output.hide()
        self.sum_polynom_output.hide()
        self.multiplication_polynom_output.hide()
        self.compare_button.hide()
        self.compare_output.hide()


class Polynom:
    def __init__(self, coeffs=[]):
        self.power = len(coeffs) - 1
        self.coeffs = coeffs
        self.remains = []

    def __str__(self):
        st, smth = '', ''
        for i in range(self.power + 1):
            st += f'+ {self.coeffs[i]}x^{self.power - i} '
        if self.remains:
            smth = ' + ('
            for i in range(len(self.remains[0])):
                smth += f'{self.remains[0][i]}x^{len(self.remains[0]) - 1 - i} + '
            smth = smth[:-2] + ') / '
            for i in range(len(self.remains[1])):
                smth += f'{self.remains[1][i]}x^{len(self.remains[1]) - 1 - i} + '
            smth = smth[:-2]
        return st[2:-1] + smth

    def __eq__(self, obj):  # == True если коэффициенты равны и степени равны
        if type(self) != type(obj):
            return False
        if self.coeffs == obj.coeffs:
            return True
        return False

    def __ne__(self, obj):  # != True если коэффициенты не равны или степени не равны
        if type(self) == type(obj):
            return not (self == obj)

    def __neg__(self):  # возвращает многочлен с противоположными коэффициентами, унарный минус
        coeffs = list(map(lambda x: -x, self.coeffs))
        res = Polynom(coeffs)
        return res

    def __add__(self, obj):
        res = Polynom()
        if type(1) == type(obj):
            obj = Polynom([obj])
        coeffs1, coeffs2 = self.coeffs, obj.coeffs
        if len(self.coeffs) > len(obj.coeffs):
            coeffs2 = [0] * (len(self.coeffs) - len(obj.coeffs)) + obj.coeffs
        elif len(self.coeffs) < len(obj.coeffs):
            coeffs1 = [0] * (len(obj.coeffs) - len(self.coeffs)) + self.coeffs
        res.coeffs = [x + y for x, y in zip(coeffs1, coeffs2)]
        res.power = len(res.coeffs) - 1
        return res

    def __sub__(self, obj):
        res = Polynom()
        if type(1) == type(obj):
            obj = Polynom([obj])
        coeffs1, coeffs2 = self.coeffs, obj.coeffs
        if len(self.coeffs) > len(obj.coeffs):
            coeffs2 = [0] * (len(self.coeffs) - len(obj.coeffs)) + obj.coeffs
        elif len(self.coeffs) < len(obj.coeffs):
            coeffs1 = [0] * (len(obj.coeffs) - len(self.coeffs)) + self.coeffs
        res.coeffs = [x - y for x, y in zip(coeffs1, coeffs2)]
        res.power = len(res.coeffs) - 1
        return res

    def __mul__(self, obj):
        if type(obj) == type(1):
            obj = Polynom([obj])
        res = Polynom([0] * (len(self.coeffs) + len(obj.coeffs) - 1))
        for i, num1 in enumerate(self.coeffs):
            for j, num2 in enumerate(obj.coeffs):
                res.coeffs[i + j] += num1 * num2
        return res

    def __truediv__(self, obj):
        if type(self) == type(obj):
            delimoe, delitel = self.coeffs, obj.coeffs
            res = Polynom()
            remains = []
            while delimoe:
                for j in delimoe:
                    if len(remains) != len(delitel):
                        remains.append(j)
                delimoe = delimoe[len(remains):]
                mnojitel = remains[0] / delitel[0]
                res.coeffs += [mnojitel]
                temp_delimoe = list(map(lambda x: x * mnojitel, delitel))
                remains = [x[0] - x[1] for x in list(zip(remains, temp_delimoe))]
                for i in remains:
                    if i == 0:
                        remains.remove(i)
            res.power = len(res.coeffs) - 1
            res.remains = [remains, delitel]
        elif type(obj) == type(1):
            coeffs = list(map(lambda x: x / obj, self.coeffs))
            res = Polynom(coeffs)
        return res

    def __pow__(self, obj):
        res = Polynom(self.coeffs)
        for i in range(obj - 1):
            res *= self
        res.power = len(res.coeffs) - 1
        return res

    def derivative(self):  # подсчет производной
        if isinstance(self, Polynom):
            lst = [0] * len(self.coeffs)
            for i in range(len(self.coeffs)):
                lst[i] = self.coeffs[i] * (self.power - i)
            res = Polynom(lst[:-1])
            res.power = self.power - 1
        else:
            res = 0
        return res

    def value(self, arg):  # возвращает значение многочлена
        res = 0
        for i in range(self.power + 1):
            res += float(arg ** (self.power - i) * self.coeffs[i])
        return res


class Solver:
    def __init__(self, polynom):
        self.polynom = polynom
        self.derivative = polynom.derivative()
        self.shturm = self.method_shturma()

    def find_roots(self):
        boarder1, boarder2 = self.boarders()
        n = self.n_roots(boarder1, boarder2)
        small_boarders = self.locate_roots(boarder1, boarder2)
        roots = []
        for segment in small_boarders:
            root = self.find_root(segment[0], segment[1])
            roots.append(root)
        return roots

    def method_shturma(self):  # вычисляет ряд Штурма
        lst = [self.polynom]
        previous = self.polynom
        deri = previous.derivative()
        while True:
            lst += [deri]
            if len(deri.coeffs) == 1:
                break
            new_deri = -previous / deri
            previous = deri
            deri = Polynom(new_deri.remains[0])
        if lst[-1].coeffs == [0.0]:
            lst = lst[:-1]
        return lst

    def w(self, c):  # вычисляет количество изменений знака по ряду Штурма
        res = 0
        if self.shturm[0].value(c) > 0:
            sign = 1
        else:
            sign = -1
        for i in self.shturm:
            if i.value(c) * sign < 0:
                res += 1
                sign = -sign
        return res

    def boarders(self):  # границы отрезка со всеми корнями
        k = max([abs(i) for i in self.polynom.coeffs]) / self.polynom.coeffs[0]
        k += 1
        return (min(-k, k), max(-k, k))

    def n_roots(self, a, b):  # количество корней на отрезке
        n = abs(self.w(a) - self.w(b))
        return n

    def locate_roots(self, a, b):  # список отрезков, на каждом из которых находится по одному корню
        if self.n_roots(a, b) == 1:
            return [(a, b)]
        if self.n_roots(a, b) == 0:
            return []
        c = (a + b) / 2
        return self.locate_roots(a, c) + self.locate_roots(c, b)

    def find_root(self, a, b, eps=0.001):  # находит корень на заданном отрезке
        if abs(b - a) < eps:
            return (b + a) / 2
        c = (a + b) / 2
        if self.polynom.value(a) * self.polynom.value(c) > 0:
            a = c
        elif self.polynom.value(b) * self.polynom.value(c) > 0:
            b = c
        return self.find_root(a, b)


class Test(QWidget, Test_ui):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.score = 0
        self.main = args[0]
        self.name = ''
        self.initUi()

    def go_back(self):
        self.main.show()
        self.hide()

    def initUi(self):
        self.setWindowTitle('Testing your knowledge')

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Results.db")
        self.con = sqlite3.connect(db_path)

        self.pick_icon_button.clicked.connect(self.pick_icon)
        self.pick_name_button.clicked.connect(self.pick_name)
        self.save_result_button.clicked.connect(self.save_result)
        self.save_result_button.setEnabled(False)
        self.view_all_results_button.clicked.connect(self.view_all_results)
        self.export_button.clicked.connect(self.export_to_csv)
        self.exit_button.clicked.connect(self.go_back)

    def export_to_csv(self):
        cursor = self.con.cursor()
        data = cursor.execute("""SELECT * FROM Result""").fetchall()
        with open('scores.csv', 'w') as output_f:
            f = csv.writer(output_f, delimiter=';')
            headers = ['ID', 'SCORE', 'USER_NAME']
            f.writerow(headers)
            for line in data:
                f.writerow(line)


    def view_all_results(self):
        cursor = self.con.cursor()
        result = cursor.execute("SELECT * FROM Result").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cursor.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def save_result(self):
        if self.correct_1_1.isChecked():
            self.score += 1
        if self.correct_1_2.isChecked():
            self.score += 1
        if self.correct_2.isChecked():
            self.score += 1
        if self.correct_3.isChecked():
            self.score += 1
        self.label_result.setText(str(self.score))
        cursor = self.con.cursor()
        cursor.execute("INSERT INTO Result (score, user_name) VALUES"
                       " (?, ?)", (self.score, self.name))
        self.con.commit()

    def pick_icon(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.pixmap = QPixmap(fname)
        self.label_icon.setPixmap(self.pixmap)

    def pick_name(self):
        name, ok_pressed = QInputDialog.getText(self, "Введите имя", "Ваше имя?")
        if ok_pressed:
            self.name = name
            self.label_name.setText(name)
            self.save_result_button.setText('Save your results')
            self.save_result_button.setEnabled(True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())