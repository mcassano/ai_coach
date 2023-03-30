import os
from datetime import datetime

import pytz
import requests


class ResultPoster:
    @staticmethod
    def http_post(api_key, exercise, target_reps, target_seconds, result):
        hostname = os.getenv('AI_COACH_WEB_HOSTNAME')
        if not hostname:
            # If we didn't configure a hostname then try localhost
            hostname = 'http://localhost:8000'

        if result:
            # we have an api_key, a hostname and a result, let's go!
            url = f'{hostname}/exercise-sets/'
            datetime_utc = datetime.now(pytz.utc)
            time_str = datetime_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
            exercise_set = {'exercise_performed': {'name': exercise.name},
                            'datetime_performed': time_str,
                            'num_reps': int(result.rep_count),
                            'num_target_reps': int(target_reps),
                            'duration_seconds': int(result.right_form_seconds)
                            if result.right_form_seconds is not None else 0,
                            'duration_target_seconds': int(target_seconds)
                            if target_seconds is not None else 0}
            print(f'POST: {exercise_set}')

            response = requests.post(
                url,
                json=exercise_set,
                headers={'Authorization': f'Api-Key {api_key}'}
            )
            print(f'Response: ({response.status_code}) {response.text}')
