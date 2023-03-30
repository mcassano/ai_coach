import os
import unittest
from unittest import mock

import responses
from src.annotation_result import AnnotationResult
from src.exercise import Exercise
from src.result_poster import ResultPoster


class TestResultPoster(unittest.TestCase):

    def setUp(self):
        responses.add(responses.POST, 'http://aicoach.ai/exercise-sets/',
                      json={'success': 'true'}, status=201)
        self.exercise = Exercise.exercise('Push-up')
        self.result = AnnotationResult(
            None,
            None,
            10,
            10,
            1,
            None,
            None,
            30,
            0,
            None,
            True,
            None,
            2)

    @responses.activate
    @mock.patch.dict(os.environ, {'AI_COACH_WEB_HOSTNAME': 'http://aicoach.ai'})
    def test_api_keys_exist_no_results(self):
        ResultPoster.http_post('a123', self.exercise, 1, 1, None)
        self.assertEqual(0, len(responses.calls))

    @responses.activate
    @mock.patch.dict(os.environ, {'AI_COACH_WEB_HOSTNAME': ''})
    def test_api_keys_not_exist_no_results(self):
        ResultPoster.http_post('a123', self.exercise, 1, 1, None)
        self.assertEqual(0, len(responses.calls))

    @responses.activate
    @mock.patch.dict(os.environ, {'AI_COACH_WEB_HOSTNAME': 'http://aicoach.ai'})
    def test_api_keys_exist_with_results(self):
        ResultPoster.http_post('a123', self.exercise, 1, 1, self.result)
        self.assertEqual(1, len(responses.calls))


if __name__ == '__main__':
    unittest.main()
