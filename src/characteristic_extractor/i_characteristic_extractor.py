from abc import ABC, abstractmethod

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from characteristic import Characteristic

class ICharacteristicExtractor(ABC):
    """Интерфейс для извлекателя характеристик.
    """    
    @abstractmethod
    def get_f0_mean(self) -> dict[Characteristic: float]:
        """Variations of fundamental frequency, vibration rate of vocal folds."""
        pass

    @abstractmethod
    def get_f0_stdev(self) -> dict[Characteristic: float]:
        #TODO Описание
        pass

    @abstractmethod
    def get_f0_min(self) -> dict[Characteristic: float]:
        #TODO Описание
        pass

    @abstractmethod
    def get_f0_max(self) -> dict[Characteristic: float]:
        #TODO Описание
        pass

    @abstractmethod
    def get_f0_range(self) -> dict[Characteristic: float]:
        #TODO Описание
        pass

    @abstractmethod
    def get_jitter_ppq5(self) -> dict[Characteristic: float]:
        """Five-point period perturbation quotient, the average absolute difference between a period 
        and the average of it and its four closest neighbors, divided by the average period."""
        pass

    @abstractmethod
    def get_shimmer_local(self) -> dict[Characteristic: float]:
        """Average absolute difference between the amplitudes of consecutive periods, divided by the average amplitude."""
        pass

    @abstractmethod
    def get_nhr(self) -> dict[Characteristic: float]:
        """Noise-to-harmonics ratio, the amplitude of noise relative to tonal components."""
        pass

    @abstractmethod
    def get_hnr(self) -> dict[Characteristic: float]:
        """Harmonics-to-noise ratio, the amplitude of tonal relative to noise components."""
        pass

    @abstractmethod
    def get_no_pauses(self) -> dict[Characteristic: float]:
        """The number of all pauses compared to total time duration, after removing silence period not lasting more than 60 ms."""
        pass

    @abstractmethod
    def get_intensity_SD(self) -> dict[Characteristic: float]:
        """Variations of average squared amplitude within a predefined time segment (“energy”) after removing silence period exceeding 60 ms."""
        pass

    @abstractmethod
    def get_f1(self) -> dict[Characteristic: float]:
        """Formant f1"""        
        pass

    @abstractmethod
    def get_f2(self) -> dict[Characteristic: float]:
        """Formant f2"""
        pass

    @abstractmethod
    def get_f3(self) -> dict[Characteristic: float]:
        """Formant f3"""
        pass

    @abstractmethod
    def get_f4(self) -> dict[Characteristic: float]:
        """Formant f4"""
        pass
