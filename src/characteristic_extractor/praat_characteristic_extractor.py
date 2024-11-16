import parselmouth
import statistics

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from i_characteristic_extractor import ICharacteristicExtractor
from characteristic import Characteristic

class PraatCharacteristicExtractor(ICharacteristicExtractor):
    """Извлекатель характеристик аудиофайла. Работает с библиотекой parselmouth (Praat).
    Основная часть скриптов была взята тут https://github.com/drfeinberg/PraatScripts
    """    

    __UNIT = 'Hertz'
    __F0MIN = 20
    __F0MAX = 500

    def __init__(self, file_path: str):
        self.__sound = parselmouth.Sound(file_path)
        self.__pitch = None
        self.__point_process = None

        self.__f1 = None
        self.__f2 = None
        self.__f3 = None
        self.__f4 = None

    def get_f0(self) -> dict[Characteristic: float]:
        """Variations of fundamental frequency, vibration rate of vocal folds."""
        if not self.__pitch:
            self.__make_pitch()

        f0 = parselmouth.praat.call(self.__pitch, "Get mean", 0, 0, self.__UNIT)
        return {Characteristic.F0: f0}

    def get_jitter_ppq5(self) -> dict[Characteristic: float]:
        """Five-point period perturbation quotient, the average absolute difference between a period 
        and the average of it and its four closest neighbors, divided by the average period."""
        if not self.__point_process:
            self.__make_point_process()

        ppq5_jitter = parselmouth.praat.call(self.__point_process, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)

        return {Characteristic.JITTER_PPQ5: ppq5_jitter}

    def get_shimmer_local(self) -> dict[Characteristic: float]:
        """Average absolute difference between the amplitudes of consecutive periods, divided by the average amplitude."""
        if not self.__point_process:
            self.__make_point_process()

        local_shimmer =  parselmouth.praat.call([self.__sound, self.__point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        return {Characteristic.SHIMMER_LOCAL: local_shimmer}

    def get_nhr(self) -> dict[Characteristic: float]:
        """Noise-to-harmonics ratio, the amplitude of noise relative to tonal components."""
        pass
        #TODO Если надо, реализовать. По идее, тоже самое, что и HNR.

    def get_hnr(self) -> dict[Characteristic: float]:
        """Harmonics-to-noise ratio, the amplitude of tonal relative to noise components."""
        harmonicity = parselmouth.praat.call(self.__sound, "To Harmonicity (cc)", 0.01, self.__F0MIN, 0.1, 1.0)
        hnr = parselmouth.praat.call(harmonicity, "Get mean", 0, 0)
        return {Characteristic.HNR: hnr}

    def get_no_pauses(self) -> dict[Characteristic: float]:
        """The number of all pauses compared to total time duration, after removing silence period not lasting more than 60 ms."""
        pass

    def get_intensity_SD(self) -> dict[Characteristic: float]:
        """Variations of average squared amplitude within a predefined time segment (“energy”) after removing silence period exceeding 60 ms."""
        pass

    def get_f1(self) -> dict[Characteristic: float]:
        """Formant f1"""        
        if not self.__f1:
            self.__extract_formants()
        
        return {Characteristic.F1: self.__f1}

    def get_f2(self) -> dict[Characteristic: float]:
        """Formant f2"""
        if not self.__f2:
            self.__extract_formants()
        
        return {Characteristic.F2: self.__f2}

    def get_f3(self) -> dict[Characteristic: float]:
        """Formant f3"""
        if not self.__f3:
            self.__extract_formants()
        
        return {Characteristic.F3: self.__f3}

    def get_f4(self) -> dict[Characteristic: float]:
        """Formant f4"""
        if not self.__f4:
            self.__extract_formants()
        
        return {Characteristic.F4: self.__f4}

    def __make_point_process(self):     
        self.__point_process = parselmouth.praat.call(self.__sound, "To PointProcess (periodic, cc)", self.__F0MIN, self.__F0MAX)

    def __make_pitch(self):
        self.__pitch = parselmouth.praat.call(self.__sound, "To Pitch", 0.0, self.__F0MIN, self.__F0MAX)

    def __extract_formants(self):
        self.__sound = parselmouth.Sound(self.__sound) # read the sound
        pitch = parselmouth.praat.call(self.__sound, "To Pitch (cc)", 0, self.__F0MIN, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, self.__F0MAX)
        pointProcess = parselmouth.praat.call(self.__sound, "To PointProcess (periodic, cc)", self.__F0MIN, self.__F0MAX)
        
        formants = parselmouth.praat.call(self.__sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
        numPoints = parselmouth.praat.call(pointProcess, "Get number of points")

        f1_list = []
        f2_list = []
        f3_list = []
        f4_list = []
        
        # Measure formants only at glottal pulses
        for point in range(0, numPoints):
            point += 1
            t = parselmouth.praat.call(pointProcess, "Get time from index", point)
            f1 = parselmouth.praat.call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
            f2 = parselmouth.praat.call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
            f3 = parselmouth.praat.call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
            f4 = parselmouth.praat.call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
            f1_list.append(f1)
            f2_list.append(f2)
            f3_list.append(f3)
            f4_list.append(f4)
        
        f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
        f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']
        f3_list = [f3 for f3 in f3_list if str(f3) != 'nan']
        f4_list = [f4 for f4 in f4_list if str(f4) != 'nan']
        
        # calculate mean formants across pulses
        f1_mean = statistics.mean(f1_list)
        f2_mean = statistics.mean(f2_list)
        f3_mean = statistics.mean(f3_list)
        f4_mean = statistics.mean(f4_list)
        
        # calculate median formants across pulses, this is what is used in all subsequent calcualtions
        # you can use mean if you want, just edit the code in the boxes below to replace median with mean
        f1_median = statistics.median(f1_list)
        f2_median = statistics.median(f2_list)
        f3_median = statistics.median(f3_list)
        f4_median = statistics.median(f4_list)
        
        self.__f1 = f1_median
        self.__f2 = f2_median
        self.__f3 = f3_median
        self.__f4 = f4_median

        #return f1_mean, f2_mean, f3_mean, f4_mean, f1_median, f2_median, f3_median, f4_median