from work3.settings import DATETIME_INPUT_FORMATS
from django.utils import timezone
#from departures.models import Departure



class DepartureInfo:
    def __init__(self, Id):
        self.main_request_id = Id

    def getCountOpenDeparture(self):
        if self.main_request_id is not None:
             return 0
        else:
            return -1
