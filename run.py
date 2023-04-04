import os

import django
from loguru import logger


@logger.catch
def main() -> None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    django.setup()

    from scripts.google_sheet import google_sheet_to_db
    from scripts.google_sheet import check_dates

    while True:
        try:
            google_sheet_to_db()
            check_dates()
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    main()
