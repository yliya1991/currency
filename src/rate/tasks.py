from bs4 import BeautifulSoup

from celery import shared_task

from rate import model_choices as mch
from rate.utils import to_decimal

import requests
import requests as req

from rate.models import Rate # noqa


@shared_task
def parse_privatbank():
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    response = requests.get(url)
    currency_type_mapper = {
        'USD': mch.SOURCE_TYPE_USD,
        'EUR': mch.SOURCE_TYPE_EUR,
        'RUR': mch.SOURCE_TYPE_RUR,
    }
    for item in response.json():

        if item['ccy'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['ccy']]

        amount = to_decimal(item['buy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        amount = to_decimal(item['sale'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_monobank():
    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)
    currency_type_mapper = {
        840: mch.SOURCE_TYPE_USD,
        978: mch.SOURCE_TYPE_EUR,
        643: mch.SOURCE_TYPE_RUR,
    }

    for item in response.json():
        if item['currencyCodeA'] not in currency_type_mapper:
            continue
        if item['currencyCodeB'] == 980:
            currency_type = currency_type_mapper[item['currencyCodeA']]

        amount = to_decimal(item['rateBuy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        amount = to_decimal(item['rateSell'])
        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_vkurse():
    url = "http://vkurse.dp.ua/course.json"
    response = requests.get(url).json()

    currency_type_mapper = {
        'Dollar': mch.SOURCE_TYPE_USD,
        'Euro': mch.SOURCE_TYPE_EUR,
        'Rub': mch.SOURCE_TYPE_RUR,
    }

    for item in response:
        if item not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item]

        amount = to_decimal(response[item]['buy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        # sale
        amount = to_decimal(response[item]['sale'])
        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_bestrate():
    from rate.models import Rate

    resp = req.get("https://obmen.dp.ua/")
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = soup.find_all('div', attrs={'class': 'currencies__block-num'})
    rate_list = []
    for result in results:
        rate = result.text
        rate_list.append(rate)

    amount = rate_list[0]
    last = Rate.objects.filter(
        source=mch.SOURCE_OBMENNIKUA,
        currency_type=1,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_OBMENNIKUA,
            currency_type=1,
            type=2,
        )

    amount = rate_list[1]
    last = Rate.objects.filter(
        source=mch.SOURCE_OBMENNIKUA,
        currency_type=1,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_OBMENNIKUA,
            currency_type=1,
            type=1,
        )

    amount = rate_list[2]
    last = Rate.objects.filter(
        source=mch.SOURCE_OBMENNIKUA,
        currency_type=2,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_OBMENNIKUA,
            currency_type=2,
            type=1,
        )

    amount = rate_list[3]
    last = Rate.objects.filter(
        source=mch.SOURCE_OBMENNIKUA,
        currency_type=2,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_OBMENNIKUA,
            currency_type=2,
            type=2,
        )


@shared_task
def parse_alfabank():
    resp = req.get("https://alfabank.ua/currency-exchange?refId=MainpageExchangerate")
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = soup.find_all('div', attrs={'class': 'currency-item-number'})
    rate_list = []
    for result in results:
        name = result.text
        rate_list.append(name)

    amount = rate_list[0]
    last = Rate.objects.filter(
        source=mch.SOURCE_ALFABANK,
        currency_type=1,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_ALFABANK,
            currency_type=1,
            type=2,
        )

    # USD_sale
    amount = rate_list[1]
    last = Rate.objects.filter(
        source=mch.SOURCE_ALFABANK,
        currency_type=1,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_ALFABANK,
            currency_type=1,
            type=1,
        )

    amount = rate_list[2]
    last = Rate.objects.filter(
        source=mch.SOURCE_ALFABANK,
        currency_type=2,
        type=2,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_ALFABANK,
            currency_type=2,
            type=2,
        )

    amount = rate_list[1]
    last = Rate.objects.filter(
        source=mch.SOURCE_ALFABANK,
        currency_type=2,
        type=1,
    ).last()

    if last is None or last.amount != amount:
        Rate.objects.create(
            amount=amount,
            source=mch.SOURCE_ALFABANK,
            currency_type=2,
            type=1,
        )


@shared_task()
def parse_tascombank():
    url = 'https://tascombank.ua/api/currencies'
    response = requests.get(url)
    list_exchanges = [exch for exch in response.json()[0] if exch.get('kurs_type') == 'exchange']
    currency_type_mapper = {
        'USD': mch.SOURCE_TYPE_USD,
        'EUR': mch.SOURCE_TYPE_EUR,
        'RUB': mch.SOURCE_TYPE_RUR,
    }

    for item in list_exchanges:
        if item['short_name'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['short_name']]

        # buy
        amount = to_decimal(item['kurs_buy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_TASKOMBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_TASKOMBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        amount = to_decimal(item['kurs_sale'])
        last = Rate.objects.filter(
            source=mch.SOURCE_TASKOMBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()

        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_TASKOMBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse():
    parse_monobank.delay()
    parse_privatbank.delay()
    parse_vkurse.delay()
    parse_bestrate.delay()
    parse_alfabank.delay()
    parse_tascombank.delay()
