from __future__ import print_function

import datetime
import os.path
from typing import Union

import requests
import xml.etree.ElementTree as ET
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger

from google_sheets.supplies.models import Supply


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1iuup5YG3dUID5KpTC8h0RTaULH2UeOQGs0MuQdq_08M'
SAMPLE_RANGE_NAME = 'A2:E'


def get_data_from_google_sheet() -> list:
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    values = []
    token_file = settings.ROOT_DIR + 'token.json'
    credentials_file = settings.ROOT_DIR + 'credentials.json'
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
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
            value["date"] = datetime.datetime.strptime(row[3], "%d.%m.%Y")
            return value
        except Exception as e:
            logger.debug(f"Date is not valid")


def get_rate() -> float:
    date = datetime.datetime.now().date().strftime("%d/%m/%Y")
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        for child in root:
            if child[1].text == "USD":
                return float(child[4].text.replace(",", "."))


def google_sheet_to_db() -> None:
    values = get_data_from_google_sheet()
    for row in values:
        valid_row = get_valid_row(row)
        if valid_row:
            rate = get_rate()
            valid_row.update({"cost_rub": valid_row["cost"] * rate})
            number = valid_row.pop("number")
            Supply.objects.update_or_create(number=number, defaults=valid_row)


