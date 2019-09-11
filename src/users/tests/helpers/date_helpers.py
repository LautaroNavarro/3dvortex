import mock
from pytz import utc
from datetime import datetime
from django.test import TestCase
from users.helpers.date_helpers import get_current_utc_datetime


class TestDateHelpers(TestCase):

    @mock.patch('users.helpers.date_helpers.datetime')
    def test_get_current_utc_datetime(self, mock_datetime):
        mock_datetime.now.return_value = datetime(1998, 12, 29)
        get_current_utc_datetime()
        self.assertTrue(mock_datetime.now.called)
        self.assertEqual(len(mock_datetime.now.call_args[0]), 1)
        self.assertEqual(mock_datetime.now.call_args[0][0], utc)
