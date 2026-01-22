import sys
import pytest
from stask import stask as st
import os

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def test_job():
    job = st.Job("notepad")
    job.do("notepad.exe").at("08:00").daily()
    assert job.cmdline == "notepad.exe"
    assert job.task_sch == "DAILY"


@pytest.mark.skipif(sys.platform != "win32", reason="windows only")
def test_process_executable():
    str = "https://large-type.com/#Take%20a%20Break"
    ret_list = st._process_executable(str)

    assert str in ret_list

@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in Github Actions.")
@pytest.mark.skipif(sys.platform != "win32", reason="windows only")
def test_simple():
    job = st.Job("test")
    job.do("python --version").post()
    assert job.task_sch == "ONCE"
    assert job._isposted
    job.delete()
