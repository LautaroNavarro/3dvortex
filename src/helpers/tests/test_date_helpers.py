import mock
from pytz import utc
from datetime import datetime
from helpers.date_helpers import get_current_utc_datetime


class TestDateHelpers():

    @mock.patch('helpers.date_helpers.datetime')
    def test_get_current_utc_datetime(self, mock_datetime):
        mock_datetime.now.return_value = datetime(1998, 12, 29)
        get_current_utc_datetime()
        assert mock_datetime.now.called is True
        assert len(mock_datetime.now.call_args[0]) == 1
        assert mock_datetime.now.call_args[0][0] == utc
