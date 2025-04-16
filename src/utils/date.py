from datetime import datetime

def now(format : str) -> str:
    current_datetime = datetime.now() 
    formatted_datetime = current_datetime.strftime(format=format)
    return formatted_datetime