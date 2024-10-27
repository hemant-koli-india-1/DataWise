import re
from datetime import datetime


def correct_mongo_query(llm_query: str) -> str:
    """
    Corrects MongoDB query syntax by converting ISODate strings to proper datetime objects
    for use with PyMongo.

    Args:
        llm_query (str): The MongoDB query string to correct

    Returns:
        str: Corrected query string with proper datetime formatting
    """

    def convert_date_format(match):
        date_str = match.group(1).strip('"\'')
        try:
            if 'T' in date_str:
                dt = datetime.fromisoformat(date_str)
            else:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
            return (f'datetime.fromisofo'
                    f'rmat("{dt.isoformat()}")')
        except ValueError:
            return match.group(0)

    # Convert ISODate strings to datetime objects
    corrected_query = re.sub(r'ISODate\((.*?)\)', convert_date_format, llm_query)
    return corrected_query