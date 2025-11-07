import sys
import pytest
from stask import stask as st


def test_job():
    job = st.Job("say_say")
    job.do("say hello").at("08:00").daily()
    assert job.cmdline == "say hello"
    assert job.task_sch == "DAILY"


@pytest.mark.skipif(sys.platform != "win32", reason="windows only")
def test_process_executable():
    str = "https://large-type.com/#Take%20a%20Break"
    ret_list = st._process_executable(str)

    assert str in ret_list


@pytest.mark.skipif(sys.platform != "win32", reason="windows only")
def test_simple():
    job = st.Job("test")
    job.do("say hello").post()
    assert job.task_sch == "ONCE"
    assert job._isposted
    job.delete()
