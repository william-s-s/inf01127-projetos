from datetime import datetime
import pytz

utc = pytz.UTC

# Convert django datetime input to string to be used in URL and vice versa
# https://stackoverflow.com/questions/70768547/how-to-pass-date-and-id-through-url-in-django
class DateConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}'

    @staticmethod
    def to_utc(value):
        value = value.replace(tzinfo=utc)
        return value
    
    @staticmethod
    def to_python(value):
        datetm = datetime.strptime(value, '%Y-%m-%dT%H-%M')
        datetm = datetm.replace(tzinfo=utc)
        return datetm
    
    @staticmethod
    def to_url(value):
        return value.strftime('%Y-%m-%dT%H-%M')
