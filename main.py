import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import PyQt5.QtWidgets as qt
from PyQt5 import uic, QtGui
import numpy as np
import json

from lissajousgen import LissajousGenerator, lissajous_figure

matplotlib.use("Agg")

# Настройки фигуры по умолчанию
default_settings = {
    "freq_x": 1,
    "freq_y": 3,
    "phase_shift": 0.25,
    "resolution": 200,
    "color": "midnightblue",
    "width": 2,
}


# Цвета для matplotlib.
with open("mpl.json", mode="r", encoding="utf-8") as f:
    mpl_color_dict = json.load(f)


class LissajousWindow(qt.QMainWindow):
    def __init__(self):
        super(LissajousWindow, self).__init__()

        # Загружаем интерфейс из файла
        uic.loadUi("main_window.ui", self)

        # Ставим версию и иконку
        # TODO: одной строкой (version=open(...).readlines()[0])
        with open("version.txt", "r") as f:
            version = f.readline()
        win_title = "Генератор фигур Лиссажу. Версия {}. CC BY-SA 4.0 Ivanov"
        self.setWindowTitle(win_title.format(version))
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "icon.bmp"))
        # Устанавливаем размер фигуры и файла-изображения по умолчанию.
        # TODO: убрать лишнее.
        self.image_file_inches = 4
        self.dpi = 100
        self.desired_image_width = self.image_file_inches * self.dpi
        self.default_inches = 4
        # Создаём холст matplotlib, ширина равна высоте.
        self._fig = plt.figure(figsize=(self.default_inches,
                                        self.default_inches),
                               dpi=self.dpi)
        # Добавляем на холст matplotlib область для построения графиков.
        # В общем случае таких областей на холсте может быть несколько
        # Аргументы add_subplot() в данном случае:
        # ширина сетки, высота сетки, номер графика в сетке
        self._ax = self._fig.add_subplot(1, 1, 1)
        # Центрируем фигуру Лиссажу на холсте (в linux версии)
        self._fig.axes[0].get_xaxis().set_visible(False)
        self._fig.axes[0].get_yaxis().set_visible(False)
        self._ax.set_axis_off()
        # Создаём qt-виджет холста для встраивания холста
        # matplotlib fig в окно Qt.
        self._fc = FigureCanvas(self._fig)
        # Связываем созданный холст c окном
        self._fc.setParent(self)

        # Настраиваем размер и положение холста
        self._fc.resize(400, 400)
        self._fc.move(20, 20)
        # Первичное построение фигуры
        self.plot_lissajous_figure()
        self.resize(650, 440)
        
        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_button_click_handler)

    def plot_button_click_handler(self):
        """
        Обработчик нажатия на кнопку применения настроек
        """
        # Получаем данные из текстовых полей интерфейса.
        settings = {}
        settings["freq_x"] = float(self.freq_x_lineedit.text())
        settings["freq_y"] = float(self.freq_y_lineedit.text())
        settings["phase_shift"] = float(self.phase_shift_lineedit.text())
        settings["resolution"] = int(self.resolution_lineedit.text())
        # TODO: переименовать 'resolution' в 'num_points' или другое.
        settings["color"] = mpl_color_dict[self.color_combobox.currentText()]
        settings["width"] = int(self.width_combobox.currentText())
        # TODO: обработка некорректных введенных значений.

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
        self.generator = LissajousGenerator(settings["resolution"])
        # TODO: переименовать переменную figure (чтобы не путать с plt.figure)
        figure = self.generator.generate_figure(settings["freq_x"],
                                                settings["freq_y"],
                                                settings["phase_shift"])

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
        file_path, _ = qt.QFileDialog.getSaveFileName(
                    self,
                    "Сохранение изображения",
                    "",
                    "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if file_path == "":
            return

        # raise NotImplementedError("Тут всего одной строчки не хватает.")
        # (?..)

        # Сохраняем изображение с указанным в текстовом поле
        # разрешением.
        self.desired_image_width = int(self.image_size_lineedit.text())
        figure = plt.gcf()
        # Временно меняем размер фигуры (вместо копирования объекта)
        figure.set_size_inches(self.desired_image_width / self.dpi,
                               self.desired_image_width / self.dpi)
        plt.savefig(file_path, dpi=self.dpi)
        # Меняем размер фигуры обратно.
        figure.set_size_inches(self.default_inches, self.default_inches)
        # TODO: либо сохранять измененную копию объекта-фигуры, либо иначе.

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
