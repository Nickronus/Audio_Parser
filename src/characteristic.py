from enum import Enum

class Characteristic(Enum):
    """Характеристики аудиофайла.
    """    
    FILEPATH = 0
    """Путь к файлу.
    """    
    F0_MEAN = 1
    """Среднее значение основной частоты (F0).
    """
    F0_STDEV = 2
    """Стандартное отклонение основной частоты (F0).
    """
    F0_MIN = 3
    """Минимальная основная частота (F0)
    """
    F0_MAX = 4
    """Максимальная основная частота (F0).
    """
    F0_RANGE = 5
    """Диапазон основной частоты (разница между f0_max и f0_min).
    """
    JITTER_PPQ5 = 6
    """Пятиточечный  коэффициент  возмущения  периода,  средняя  абсолютная  разница  между  периодом  и
    среднее  значение  этого  значения  и  его  четырех  ближайших  соседей,  деленное  на  средний  период.
    """    
    SHIMMER_LOCAL = 7
    """Средняя  абсолютная  разность  между  амплитудами  последовательных  периодов,  деленная  на
    средняя  амплитуда.
    """    
    NHR = 8
    """Отношение  шума  к  гармоникам,  амплитуда  шума  относительно  тональных  составляющих.
    """    
    HNR = 9
    """ Отношение  гармоник  к  шуму,  амплитуда  тональных  компонентов  относительно  шумовых.
    """    
    NO_PAUSES = 10
    """Количество  всех  пауз  по  сравнению  с  общей  продолжительностью  времени  после  удаления  периодов  тишины,  не  превышающих  
    60  мс.
    """    
    INTENSITY_SD = 11
    """ Изменения  среднего  квадрата  амплитуды  в  пределах  заданного  временного  отрезка  («энергии»)  после
    удаление  периода  тишины,  превышающего  60  мс
    """    
    F1 = 12
    """Форманта f1.
    """    
    F2 = 13
    """Форманта f2.
    """   
    F3 = 14
    """Форманта f3.
    """   
    F4 = 15
    """Форманта f4.
    """   