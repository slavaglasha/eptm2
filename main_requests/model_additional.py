from django.contrib.auth.models import User

from work3.settings import DATETIME_INPUT_FORMATS
from django.utils import timezone

from work_profiles.models import Profile
from .models import MainRequest
from departures.models import Departure
from places.models import  Places



class MainRequestAddition:
    main_request = {}

    def __init__(self, main__request):
        self.main_request =main__request




    def to_dict_add(self):

        if isinstance(self.main_request, MainRequest):
            result = self.main_request.to_dict
            departures = Departure.objects.filter(main_request__pk=self.main_request.pk)
            deps = []

            for dep in departures:

                users_str = ', '.join([(k.user.get_full_name()) for k in dep.execute_users.all()])

                print('' if dep.start_datetime== None else dep.start_datetime.strftime(DATETIME_INPUT_FORMATS[0]))

                dep_json = {"start": '' if dep.start_datetime== None else timezone.localtime(dep.start_datetime).strftime(DATETIME_INPUT_FORMATS[0]),
                            "end": '' if dep.end_datetime== None else  timezone.localtime(dep.end_datetime).strftime(DATETIME_INPUT_FORMATS[0]),
                            "users": users_str}
                deps.append(dep_json)

            result['departures'] = deps
            return result
        else:
            return None

