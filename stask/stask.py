import subprocess
import os
import shlex
import shutil
import tempfile
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta
from dateutil.parser import parse

VALID_STATUS = ("MINUTE", "HOURLY", "DAILY", "WEEKLY",
                "MONTHLY", "ONCE", "ONSTART", "ONLOGON", "ONIDLE")


def _get_time_2min():
    now = datetime.now()+timedelta(minutes=2)
    time = now.strftime("%H:%M")
    return time


def _process_executable(executable, folder=os.getcwd()):

    if not executable:
        return None

    if os.path.exists(os.path.dirname(executable)):
        executable_sh = shutil.which(executable)
        exe_shex = [executable_sh]
    else:
        exe_shex = shlex.split(executable)
        executable_sh = shutil.which(exe_shex[0])

    if not executable_sh:
        # if not empty or None
        if folder:
            exe_with_path = os.path.join(folder, exe_shex[0])
            if os.path.exists(exe_with_path):
                executable_sh = exe_with_path
            else:
                executable_sh = executable
    exe_shex[0] = executable_sh
    return exe_shex


def _create(cmdline, task_name="test_task", task_sch="ONCE", task_st="13:00", idletime=7, add_setting=""):
    # schtasks /create /tn test_task /sc DAILY /st 12:50 /tr "C:\windows\system32\calc.exe"

    task_exe_list = _process_executable(cmdline)
    task_exe = " ".join(task_exe_list)

    task_upper = task_sch.upper()

    if task_upper.startswith("ON") and task_upper != "ONCE":
        if task_upper in ["ONIDLE"]:
            cmd = ["schtasks", "/create", "/tn", task_name, "/sc",
                   task_sch, "/tr", task_exe, "/F", "/I", str(idletime)]
        else:
            cmd = ["schtasks", "/create", "/tn", task_name,
                   "/sc", task_sch, "/tr", task_exe, "/F"]
    else:
        cmd = ["schtasks", "/create", "/tn", task_name, "/sc",
               task_sch, "/st", task_st, "/tr", task_exe, "/F"]

    if len(add_setting) != 0:
        add_setting_list = add_setting.split(" ")
        cmd = cmd + add_setting_list
    print(cmd)
    iret = subprocess.Popen(cmd)
    return iret


def _delete(task_name: str):
    # schtasks /Delete /TN test_task3 /F
    # task_name = "test_task"
    cmd = ["schtasks", "/Delete", "/TN", task_name, "/F"]
    iret = subprocess.Popen(cmd)
    return iret


def _tasklist(task_name: str):
    cmd = ["schtasks", "/Query", "/TN", task_name, "/V", "/FO", "LIST"]
    iret = subprocess.Popen(cmd)
    return iret


def _runtask(task_name: str):
    cmd = ["schtasks", "/run", "/tn", task_name, "/I"]
    iret = subprocess.Popen(cmd)
    return iret


def _update_task_power_settings(task_name: str):
    xml_file = os.path.join(tempfile.gettempdir(), task_name + ".xml")
    cmd_export = ["schtasks", "/Query", "/TN", task_name, "/XML", "ONE"]

    with open(xml_file, "w") as f:
        subprocess.run(cmd_export, stdout=f, check=True)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespace = "{http://schemas.microsoft.com/windows/2004/02/mit/task}"
    settings = root.find(f"{namespace}Settings")

    disallow_start = settings.find(f"{namespace}DisallowStartIfOnBatteries")
    if disallow_start is not None:
        disallow_start.text = "false"

    stop_if_going = settings.find(f"{namespace}StopIfGoingOnBatteries")
    if stop_if_going is not None:
        stop_if_going.text = "false"

    tree.write(xml_file)

    cmd_update = ["schtasks", "/Create", "/TN", task_name, "/XML", xml_file, "/F"]
    subprocess.run(cmd_update, capture_output=True, check=True)
    os.remove(xml_file)


# schtasks /Query /TN test_task /V /FO LIST


class Job:
    """
    A simplified api to call/schedule tasks in windows using ``schtasks``

    Example:

    # Schedule a one time job for 6:30 pm today
    job = st.Job("test")
    job.do("say hello").at("6:30pm").post()

    # Schedule job to say hello daily as 8:00
    job = Job("say_say")
    job.do("say hello").at("8am").daily().post()

    

    """
    def __init__(self, name):
        self.name = name
        self.cmdline = ""
        self.task_sch = "ONCE"
        self.task_time = _get_time_2min()
        self.idletime = 1
        self.modifier_str = ""
        self._isposted = False
        self.allow_on_battery = True

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return "{0} runs at {1} {2} with {3}".format(self.name, self.task_time, self.task_sch, self.cmdline)

    def do(self, cmdline: str):
        """
        The task to perform wih schedule task.

        Example:

        job = Job("say_say")
        job.do("say hello").at("08:00").daily()


        """
        assert len(cmdline.strip()) != 0, "Invalid commandline"
        self.cmdline = cmdline
        return self

    def at(self, timestr):
        validtime = parse(timestr).strftime("%H:%M")
        self.task_time = validtime
        return self

    def once(self):
        self.task_sch = VALID_STATUS[5]
        return self

    def daily(self):
        self.task_sch = VALID_STATUS[2]
        return self

    def weekly(self):
        self.task_sch = VALID_STATUS[3]
        return self

    def monthly(self):
        self.task_sch = VALID_STATUS[4]
        return self

    def onidle(self, idletime=1):
        """
        Schedules a schtask onidle

        Example:

        # schedule job if system idle for 10 mins
        job.onidle(10)

        """
        assert idletime >= 1 and idletime < 999, "Idletime should be in range 1-999"
        self.idletime = idletime
        self.task_sch = VALID_STATUS[8]
        return self

    def post(self):
        """
        Schedules the job
        """
        iret = _create(self.cmdline,
                      task_name=self.name,
                      task_sch=self.task_sch,
                      task_st=self.task_time,
                      idletime=self.idletime,
                      add_setting=self.modifier_str)

        if self.allow_on_battery:
            _update_task_power_settings(self.name)

        self._isposted = True
        return self

    def run_on_ac_only(self):
        self.allow_on_battery = False
        return self

    def delete(self):
        """
        Deletes a schtask
        """
        iret = _delete(self.name)
        return iret.returncode

    def list(self):
        """
        List the job
        """
        iret = _tasklist(self.name)
        return iret.returncode

    def run(self):
        """
        Runs a scheduled job
        """
        iret = _runtask(self.name)
        return iret.returncode

    def minute(self):
        self.task_sch = VALID_STATUS[0]
        return self

    def hour(self):
        self.task_sch = VALID_STATUS[1]
        return self

    def day(self):
        self.task_sch = VALID_STATUS[2]
        return self

    def week(self):
        self.task_sch = VALID_STATUS[3]
        return self

    def month(self):
        self.task_sch = VALID_STATUS[4]
        return self

    def every(self, num: int):
        """
        Schedule tasks for every unit of time.

        Example:

        # Schedule job for every minnute
        job.every(10).minute()

        # Schedule job for every 5 hours
        job.every(5).hour()

        # Schedule job for every 10 day
        job.every(10).day()

        # Schedule job for every 2 week
        job.every(2).week()

        """
        # default minute if not provided
        self.task_sch = VALID_STATUS[0]
        self.modifier_str = "/MO {}".format(num)
        return self
