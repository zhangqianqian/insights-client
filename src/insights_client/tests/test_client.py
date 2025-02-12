from sys import stderr, stdout
from unittest import mock
from unittest.mock import patch
import insights_client
import pytest


# Test config load error
@patch('os.getuid', return_value=0)
@patch('insights.client.InsightsConfig.load_all', side_effect = ValueError('mocked error'))
def test_load_config_error(os_uid, insightsConfig):
    with pytest.raises(SystemExit) as sys_exit:
        insights_client._main()
    assert sys_exit.value.code != 0


# test keyboardinterrupt handler
@patch('os.getuid', return_value = 0)
@patch('insights.client.InsightsConfig.load_all', side_effect = KeyboardInterrupt)
def test_keyboard_interrupt(os_uid, client):
    with pytest.raises(SystemExit) as sys_exit:
        insights_client._main()
    assert sys_exit.value.code != 0

#check run phase error 100 handler
@patch('os.getuid', return_value = 0)
@patch('insights.client.phase.v1.get_phases')
@patch('insights.client.InsightsClient')
@patch('insights_client.sorted_eggs', return_value = "/var/lib/insights/newest.egg")
@patch('insights_client.subprocess.Popen')
@patch('insights_client.enumerate', return_value = [("1", "egg")])
@patch('insights_client.os.path.isfile', return_value = True)
def test_phase_error_100(isfile, enumerate, mock_subprocess, sorted_eggs, client, p, os_uid):
    with pytest.raises(SystemExit) as sys_exit:
        mock_subprocess.return_value.returncode= 100
        mock_subprocess.return_value.communicate.return_value = ('output', 'error')
        insights_client.run_phase(p, client, sorted_eggs)
    assert sys_exit.value.code == 0