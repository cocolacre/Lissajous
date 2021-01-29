import sys
import os
import PyQt5.QtWidgets as qt
from PyQt5 import uic, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAggBase as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import json

from lissajousgen import LissajousGenerator, lissajous_figure


# Настройки фигуры по умолчанию
default_settings = {
    "freq_x": 2,
    "freq_y": 3,
    "color": "midnightblue",
    "width": 2
}


# Цвета для matplotlib
with open("mpl.json", mode="r", encoding="utf-8") as f:
    mpl_color_dict = json.load(f)


class LissajousWindow(qt.QMainWindow):
    def __init__(self):
        super(LissajousWindow, self).__init__()

        # Загружаем интерфейс из файла
        uic.loadUi("main_window.ui", self)

        # Ставим версию и иконку
        with open("version.txt", "r") as f:
            version = f.readline()
        self.setWindowTitle("Генератор фигур Лиссажу. Версия {}. CC BY-SA 4.0 Ivanov".format(
            version
        ))
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "icon.bmp"))

        # Создаём холст matplotlib
        self._fig = plt.figure(figsize=(4, 3), dpi=72)
        # Добавляем на холст matplotlib область для построения графиков.
        # В общем случае таких областей на холсте может быть несколько
        # Аргументы add_subplot() в данном случае:
        # ширина сетки, высота сетки, номер графика в сетке
        self._ax = self._fig.add_subplot(1, 1, 1)

        # Создаём qt-виджет холста для встраивания холста
        # matplotlib fig в окно Qt.
        self._fc = FigureCanvas(self._fig)
        # Связываем созданный холст c окном
        self._fc.setParent(self)
        # Настраиваем размер и положение холста
        self._fc.resize(400, 300)
        self._fc.move(20, 20)

        # Первичное построение фигуры
        self.plot_lissajous_figure()

        self.resize(650, 300)

        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_button_click_handler)

    def plot_button_click_handler(self):
        """
        Обработчик нажатия на кнопку применения настроек
        """
        # Получаем данные из текстовых полей
        settings = {}

        settings["freq_x"] = float(self.freq_x_lineedit.text())
        settings["freq_y"] = float(self.freq_y_lineedit.text())
        settings["color"] = mpl_color_dict[self.color_combobox.currentText()]
        settings["width"] = int(self.width_combobox.currentText())

        # Перестраиваем график
        self.plot_lissajous_figure(settings)

    def plot_lissajous_figure(self, settings=default_settings):
        """
        Обновление фигуры
        """
        # Удаляем устаревшие данные с графика
        for line in self._ax.lines:
            line.remove()

        # Генерируем сигнал для построения
        self.generator = LissajousGenerator()
        figure = self.generator.generate_figure(settings["freq_x"],
                                                settings["freq_y"])

        # Строим график
        self._ax.plot(figure.x_arr, figure.y_arr,
                      color=settings["color"], linewidth=settings["width"])

        plt.axis("off")

        # Нужно, чтобы все элементы не выходили за пределы холста
        plt.tight_layout()

        # Обновляем холст в окне
        self._fc.draw()

    def save_button_click_handler(self):
        """
        Обработчик нажатия на кнопку сохранения настроек
        """
        file_path, _ = qt.QFileDialog.getSaveFileName(self, "Сохранение изображения", "C:\\",
                                                            "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if file_path == "":
            return

        #raise NotImplementedError("Тут всего одной строчки не хватает.")
        self._fig.savefig(file_path)


if __name__ == "__main__":
    # Инициализируем приложение Qt
    app = qt.QApplication(sys.argv)

    # Создаём и настраиваем главное окно
    main_window = LissajousWindow()

    # Показываем окно
    main_window.show()

    # Запуск приложения
    # На этой строке выполнение основной программы блокируется
    # до тех пор, пока пользователь не закроет окно.
    # Вся дальнейшая работа должна вестись либо в отдельных потоках,
    # либо в обработчиках событий Qt.
    sys.exit(app.exec_())
