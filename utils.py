from exceptions import (
    NegativeTitlesError,
    InvalidYearCupError,
    ImpossibleTitlesError
    )
from datetime import datetime


def data_processing(dict_team):
    date_object = datetime.strptime(dict_team["first_cup"], "%Y-%m-%d")
    quantity_cups = int((2022 - date_object.year) / 4)

    if dict_team["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")

    if (date_object.year - 1930) % 4 != 0 or date_object.year < 1930:
        raise InvalidYearCupError("there was no world cup this year")

    if dict_team["titles"] > quantity_cups:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
