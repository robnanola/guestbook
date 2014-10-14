import unicodedata
import re

def slugify(value):
    """

    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip()
    return re.sub('[-\s]+', '-', value)


def unslugify(value):
    return value.replace('-', ' ').replace('_', ' ')