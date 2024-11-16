import parselmouth

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from i_characteristic_executor import ICharacteristicExecutor
from characteristic import Characteristic

class PraatCharacteristicExecutor(ICharacteristicExecutor):

    __UNIT = 'Hertz'
    __F0MIN = 20
    __F0MAX = 500

    def __init__(self, file_path: str):
        self.__sound = parselmouth.Sound(file_path)
        self.__pitch = None
        self.__point_process = None

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

    def __make_point_process(self):
        self.__point_process = parselmouth.praat.call(self.__sound, "To PointProcess (periodic, cc)", self.__F0MIN, self.__F0MAX)

    def __make_pitch(self):
        self.__pitch = parselmouth.praat.call(self.__sound, "To Pitch", 0.0, self.__F0MIN, self.__F0MAX)