import datetime
import os
import django
from django.utils import timezone
from loguru import logger


@logger.catch
def main() -> None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    django.setup()

    from scripts.google_sheet import google_sheet_to_db
    time = timezone.now()
    google_sheet_to_db()
    # while True:
    #     if time + datetime.timedelta(minutes=1) < timezone.now():
    #         try:
    #             get_info()
    #         except Exception as e:
    #             logger.error(e)
    #         time = timezone.now()


if __name__ == "__main__":
    main()
