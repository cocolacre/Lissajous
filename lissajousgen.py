import numpy as np
import time


class lissajous_figure:
    """
    Фигуры Лиссажу.
    Задаётся набором точек с координатами x и y.
    (?..) TODO: переработать модуль.
    """
    def __init__(self, x_array, y_array):
        self.x_arr=x_array
        self.y_arr=y_array


class LissajousGenerator:
    """
    Генерирует фигуры Лиссажу с заданными параметрами
    """
    def __init__(self, resolution=200):
        # TODO: убрать default значение.
        # TODO: переименовать 'resolution' в 'num_points' или другое.
        self.set_resolution(resolution)
        
    def set_resolution(self, resolution):
        """
        resolution определяет количество точек в кривой
        TODO: либо доделать property, либо убрать underscore синтаксис.
        """
        self._resolution = resolution

    def generate_figure(self, freq_x, freq_y,phase_shift):
        """
        Генерирует фигуру (массивы x и y координат точек) с заданными частотами.
        """
        t_array = np.linspace(0, 2 * np.pi, self._resolution)
        x_array = np.sin(freq_x * t_array + phase_shift * np.pi)
        y_array = np.sin(freq_y * t_array)
        return lissajous_figure(x_array, y_array)
