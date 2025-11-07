import sys
import pytest
from unittest.mock import patch
from stask import cli

@pytest.mark.skipif(sys.platform != "win32", reason="windows only")
@patch('stask.stask.Job')
def test_cli_create(mock_job):
    with patch.object(sys, 'argv', ['stask', 'create', '-n', 'test_task', '-c', 'notepad.exe', '-s', 'DAILY', '-a', '10:00']):
        cli.main()
        mock_job.assert_called_with('test_task')
        mock_job.return_value.do.assert_called_with('notepad.exe')
        mock_job.return_value.at.assert_called_with('10:00')
        mock_job.return_value.daily.assert_called_once()
        mock_job.return_value.post.assert_called_once()

@pytest.mark.skipif(sys.platform != "win32", reason="windows only")
@patch('stask.stask.Job')
def test_cli_delete(mock_job):
    with patch.object(sys, 'argv', ['stask', 'delete', '-n', 'test_task']):
        cli.main()
        mock_job.assert_called_with('test_task')
        mock_job.return_value.delete.assert_called_once()

@pytest.mark.skipif(sys.platform != "win32", reason="windows only")
@patch('stask.stask.Job')
def test_cli_list(mock_job):
    with patch.object(sys, 'argv', ['stask', 'list', '-n', 'test_task']):
        cli.main()
        mock_job.assert_called_with('test_task')
        mock_job.return_value.list.assert_called_once()
