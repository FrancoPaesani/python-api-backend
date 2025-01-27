from decimal import Decimal


class VitalSignsInfo:
    caution_level: int

    def __init__(self):
        self.set_caution_level()

    def set_caution_level(self):
        raise NotImplementedError()


class TemperatureInfo(VitalSignsInfo):
    temperature: Decimal

    def __init__(self, temperature: Decimal):
        self.temperature = temperature
        super().__init__()

    def set_caution_level(self):
        match self.temperature:
            case _ if self.temperature <= Decimal(35):
                self.caution_level = 3
            case _ if self.temperature < Decimal(36) and self.temperature > Decimal(35):
                self.caution_level = 2
            case _ if self.temperature >= Decimal(36) and self.temperature < Decimal(
                37.5
            ):
                self.caution_level = 0
            case _ if self.temperature >= Decimal(37.5) and self.temperature < Decimal(
                39.5
            ):
                self.caution_level = 1
            case _ if self.temperature >= Decimal(39.5) and self.temperature < Decimal(
                41
            ):
                self.caution_level = 2
            case _ if self.temperature >= Decimal(41):
                self.caution_level = 3


class PressureInfo(VitalSignsInfo):
    systolic: Decimal
    diastolic: Decimal

    def __init__(self, systolic: Decimal, diastolic: Decimal):
        self.systolic = systolic
        self.diastolyc = diastolic
        super().__init__()

    def set_caution_level(self):
        if self.systolic < Decimal(120) and self.diastolyc < Decimal(80):
            self.caution_level = 0
        if (Decimal(120) <= self.systolic <= Decimal(129)) and (
            self.diastolyc <= Decimal(80)
        ):
            self.caution_level = 1
        if (Decimal(130) <= self.systolic <= Decimal(139)) and (
            Decimal(80) <= self.diastolyc <= Decimal(89)
        ):
            self.caution_level = 2
        if (Decimal(140) <= self.systolic) or (Decimal(90) <= self.diastolyc):
            self.caution_level = 3
        if (Decimal(180) <= self.systolic) or (Decimal(120) <= self.diastolyc):
            self.caution_level = 4


class PulseRateInfo(VitalSignsInfo):
    pulse_rate: Decimal

    def __init__(self, pulse_rate: Decimal, age_in_months: int):
        self.pulse_rate = pulse_rate
        self.age_in_months = age_in_months
        years, months = divmod(age_in_months, 12)
        self.age_in_years = years
        super().__init__()

    def set_caution_level(self):
        self.caution_level = 0

        if self.age_in_months <= 1 and (
            self.pulse_rate < Decimal(120) or self.pulse_rate > Decimal(160)
        ):
            self.caution_level = 2
        if 1 < self.age_in_months <= 12 and (
            self.pulse_rate < Decimal(80) or self.pulse_rate > Decimal(140)
        ):
            self.caution_level = 2

        if 1 < self.age_in_years <= 2 and (
            self.pulse_rate < Decimal(80) or self.pulse_rate > Decimal(130)
        ):
            self.caution_level = 2
        if 2 < self.age_in_years <= 6 and (
            self.pulse_rate < Decimal(75) or self.pulse_rate > Decimal(120)
        ):
            self.caution_level = 2
        if 6 < self.age_in_years <= 12 and (
            self.pulse_rate < Decimal(75) or self.pulse_rate > Decimal(110)
        ):
            self.caution_level = 2
        if 12 < self.age_in_years and (
            self.pulse_rate < Decimal(60) or self.pulse_rate > Decimal(110)
        ):
            self.caution_level = 2


class RespirationRateInfo(VitalSignsInfo):
    respiration_rate: Decimal

    def __init__(self, respiration_rate: Decimal, age_in_years: int):
        self.age = age_in_years
        self.respiration_rate = respiration_rate
        super().__init__()

    def set_caution_level(self):
        self.caution_level = 0

        if self.age < 2 and (
            self.respiration_rate < Decimal(30) or self.respiration_rate > Decimal(40)
        ):
            self.caution_level = 2
        if 2 <= self.age < 6 and (
            self.respiration_rate < Decimal(20) or self.respiration_rate > Decimal(40)
        ):
            self.caution_level = 2
        if 6 <= self.age < 11 and (
            self.respiration_rate < Decimal(15) or self.respiration_rate > Decimal(25)
        ):
            self.caution_level = 2
        if 11 <= self.age < 18 and (
            self.respiration_rate < Decimal(15) or self.respiration_rate > Decimal(20)
        ):
            self.caution_level = 2
        if 18 <= self.age < 70 and (
            self.respiration_rate < Decimal(12) or self.respiration_rate > Decimal(20)
        ):
            self.caution_level = 2
        if 70 <= self.age and (
            self.respiration_rate < Decimal(15) or self.respiration_rate > Decimal(20)
        ):
            self.caution_level = 2
