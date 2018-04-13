import json
from datetime import datetime
import main_requests.models as mod

class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, mod.MainRequest):
            return o.to_dict

