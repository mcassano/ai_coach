import os
from datetime import datetime

import pytz
import requests


class ResultPoster:
    @staticmethod
    def http_post(api_key: str,
                  exercise_name: str,
                  target_reps: int,
                  target_seconds: int,
                  rep_count: int,
                  duration: int):
        if not api_key:
            raise ValueError('api_key is required')

        hostname = os.getenv('AI_COACH_WEB_HOSTNAME')
        if not hostname:
            # If we didn't configure a hostname then try localhost
            hostname = 'http://localhost:8000'

        url = f'{hostname}/exercise-sets/'
        datetime_utc = datetime.now(pytz.utc)
        time_str = datetime_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
        exercise_set = {'exercise_performed': {'name': exercise_name},
                        'datetime_performed': time_str,
                        'num_reps': rep_count,
                        'num_target_reps': target_reps,
                        'duration_seconds': duration
                        if duration is not None else 0,
                        'duration_target_seconds': target_seconds
                        if target_seconds is not None else 0}
        print(f'POST: {exercise_set}')

        response = requests.post(
            url,
            json=exercise_set,
            headers={'Authorization': f'Api-Key {api_key}'}
        )
        print(f'Response: ({response.status_code}) {response.text}')
