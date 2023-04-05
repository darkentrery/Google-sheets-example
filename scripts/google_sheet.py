from __future__ import print_function

import datetime
from typing import Union

import requests
import xml.etree.ElementTree as ET
from django.conf import settings
from django.utils import timezone
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger

from google_sheets.supplies.models import Supply
from scripts.bot import send_notification

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1iuup5YG3dUID5KpTC8h0RTaULH2UeOQGs0MuQdq_08M'
SAMPLE_RANGE_NAME = 'A2:E'


def get_data_from_google_sheet() -> list:
    values = []
    token_file = settings.ROOT_DIR + 'servicetoken.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(token_file, SCOPES)

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
    except HttpError as err:
        print(err)

    return values


def get_valid_row(row: list) -> Union[dict, None]:
    if len(row) == 4:
        try:
            value = {}
            value["number"] = int(row[0])
            value["order"] = int(row[1])
            value["cost"] = float(row[2])
            value["date"] = datetime.datetime.strptime(row[3], "%d.%m.%Y").date()
            return value
        except Exception as e:
            logger.debug(f"Date is not valid")


def get_rate_usd() -> float:
    date = datetime.datetime.now().date().strftime("%d/%m/%Y")
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        for child in root:
            if child[1].text == "USD":
                return float(child[4].text.replace(",", "."))


def get_send_status(number: int, valid_row: dict) -> bool:
    is_send = False
    if Supply.objects.filter(number=number).exists():
        obj = Supply.objects.filter(number=number).first()
        if obj.order == valid_row["order"] and obj.cost == valid_row["cost"] and obj.date == valid_row["date"] and obj.is_send:
            is_send = True
    return is_send


def google_sheet_to_db() -> None:
    values = get_data_from_google_sheet()
    for row in values:
        valid_row = get_valid_row(row)
        if valid_row:
            rate = get_rate_usd()
            valid_row.update({"cost_rub": valid_row["cost"] * rate})
            number = valid_row.pop("number")
            valid_row.update({"is_send": get_send_status(number, valid_row)})
            Supply.objects.update_or_create(number=number, defaults=valid_row)


def check_dates() -> None:
    now = timezone.now().date()
    for supply in Supply.objects.all():
        if supply.date < now and not supply.is_send:
            supply.is_send = True
            supply.save()
            send_notification(f"Закончился срок доставки у заказа №{supply.number}")
