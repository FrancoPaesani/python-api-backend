from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from faker import Faker

from utils.date_utils import diff_in_months, diff_in_years
from domain.vital_signs_info import (
    PressureInfo,
    PulseRateInfo,
    RespirationRateInfo,
    TemperatureInfo,
)

fake = Faker()


def test_correct_temperature():
    temperature_info = TemperatureInfo(temperature=Decimal(37.4))

    assert temperature_info.caution_level == 0


def test_hypothermia_temperature():
    temperature_info = TemperatureInfo(temperature=Decimal(34))

    assert temperature_info.caution_level == 3


def test_hyperthermia_temperature():
    temperature_info = TemperatureInfo(temperature=Decimal(41))

    assert temperature_info.caution_level == 3


def test_high_fever_temperature():
    temperature_info = TemperatureInfo(temperature=Decimal(39.7))

    assert temperature_info.caution_level == 2


def test_fever_temperature():
    temperature_info = TemperatureInfo(temperature=Decimal(38))

    assert temperature_info.caution_level == 1


def test_correct_pressure():
    pressure_info = PressureInfo(systolic=110, diastolic=75)

    assert pressure_info.caution_level == 0


def test_high_pressure():
    pressure_info = PressureInfo(systolic=130, diastolic=80)

    assert pressure_info.caution_level == 2


def test_correct_pulse_rate():
    birth_date = datetime.now() - relativedelta(months=3)
    age_in_months = diff_in_months(birth_date, datetime.now())

    pulse_rate_info = PulseRateInfo(pulse_rate=90, age_in_months=age_in_months)

    assert pulse_rate_info.caution_level == 0


def test_incorrect_pulse_rate():
    birth_date = datetime.now() - relativedelta(months=3)
    age_in_months = diff_in_months(birth_date, datetime.now())

    pulse_rate_info = PulseRateInfo(pulse_rate=79, age_in_months=age_in_months)

    assert pulse_rate_info.caution_level == 2


def test_correct_respiration_rate():
    birth_date = datetime.now() - relativedelta(months=14)
    age_in_years = diff_in_years(birth_date, datetime.now())

    respiration_rate_info = RespirationRateInfo(
        respiration_rate=35, age_in_years=age_in_years
    )

    assert respiration_rate_info.caution_level == 0


def test_incorrect_respiration_rate():
    birth_date = datetime.now() - relativedelta(years=4)
    age_in_years = diff_in_years(birth_date, datetime.now())

    respiration_rate_info = RespirationRateInfo(
        respiration_rate=18, age_in_years=age_in_years
    )

    assert respiration_rate_info.caution_level == 2
