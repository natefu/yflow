import uuid

from datetime import datetime


def generate() -> str:
    date_part = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = str(uuid.uuid1()).split('-', 1)[0].upper()

    return f'{date_part}{random_part}'
