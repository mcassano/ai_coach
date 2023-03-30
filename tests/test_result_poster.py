import os
import unittest
from unittest import mock

import responses
from src.result_poster import ResultPoster


class TestResultPoster(unittest.TestCase):

    def setUp(self):
        responses.add(responses.POST, 'http://aicoach.ai/exercise-sets/',
                      json={'success': 'true'}, status=201)

    @responses.activate
    @mock.patch.dict(os.environ, {'AI_COACH_WEB_HOSTNAME': 'http://aicoach.ai'})
    def test_api_keys_not_set(self):
        with self.assertRaises(Exception) as context:
            ResultPoster.http_post(None, 'Push-up', 10, 30, 10, 30)

        self.assertTrue('api_key is required' in str(context.exception))

    @responses.activate
    @mock.patch.dict(os.environ, {'AI_COACH_WEB_HOSTNAME': 'http://aicoach.ai'})
    def test_api_keys_exist_with_good_params(self):
        ResultPoster.http_post('a123', 'Push-up', 10, 30, 10, 30)
        self.assertEqual(1, len(responses.calls))


if __name__ == '__main__':
    unittest.main()
