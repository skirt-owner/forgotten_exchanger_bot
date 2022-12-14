import requests

from io import BytesIO
import matplotlib.pyplot as plt

from bot.config import SYMBOLS

plt.ioff()


async def get_currency(_from_: str, _to_: str) -> tuple:
    url = f"https://api.exchangerate.host/convert?from={_from_}&to={_to_}"
    response = requests.get(url)
    data = response.json()
    return data["date"], data["result"]


async def get_historical_currency(_from_: str, _to_: str, _date_: str) -> float:
    url = f"https://api.exchangerate.host/{_date_}?base={_from_}&symbols={_to_}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][_to_]


async def get_stat_image(_from_: str, _to_: str, start_date: str, end_date: str) -> BytesIO:
    url = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}%base={_from_}%symbols={_to_}"
    response = requests.get(url)
    data = response.json()
    dates = list(data["rates"].keys())
    rates = [i[_to_] for i in list(data["rates"].values())]
    return generate_currency_image(dates, rates, _from_, _to_)


def generate_currency_image(dates: list[str], rates: list[float], _from_: str, _to_: str) -> BytesIO:
    plt.figure(tight_layout=True)
    plt.plot(dates, rates, "o-r", label=f"{_from_}{_to_}")
    plt.xticks([])
    plt.yticks([])
    plt.xlabel('Dates')
    plt.ylabel('Rates')
    plt.legend()
    image_data = BytesIO()
    plt.savefig(image_data, format="png", bbox_inches='tight', dpi=100)
    return image_data


async def calculate_currency(_from_: str, _to_: str, amount: str) -> tuple:
    url = f"https://api.exchangerate.host/convert?from={_from_}&to={_to_}&amount={amount}"
    response = requests.get(url)
    data = response.json()
    return data["date"], data["result"]


def get_symbol_full_name(symbol: str) -> str:
    return SYMBOLS[symbol]["description"]
