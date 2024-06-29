from datetime import datetime


def get_time():
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d_%H-%M")
    return formatted_now.strip()
