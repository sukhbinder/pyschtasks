import os
import sys
import pytest
from stask import stask as st

is_windows = sys.platform == "win32"


@pytest.mark.skipif(not is_windows, reason="schtasks is only available on Windows")
def test_xml():
    xml_file = "test_task.xml"
    job = st.Job("test_xml_task")
    job.do("calc.exe").post()

    assert job.to_xml(xml_file) == 0
    assert os.path.exists(xml_file)

    new_job_name = "test_xml_task_from_file"
    new_job = st.Job(new_job_name)
    assert new_job.from_xml(xml_file) == 0

    # A simple way to check if it exists is to try to delete it.
    delete_status = new_job.delete()
    assert delete_status == 0

    # Cleanup
    job.delete()
    os.remove(xml_file)


def test_job():
    job = st.Job("say_say")
    job.do("say hello").at("08:00").daily()
    assert job.cmdline == "say hello"
    assert job.task_sch == "DAILY"


def test_process_executable():
    str_ = "https://large-type.com/#Take%20a%20Break"
    ret_list = st._process_executable(str_)

    assert str_ in ret_list


@pytest.mark.skipif(not is_windows, reason="schtasks is only available on Windows")
def test_simple():
    job = st.Job("test")
    job.do("say hello").post()
    assert job.task_sch == "ONCE"
    assert job._isposted
    job.delete()
