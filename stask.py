import subprocess
import os
import shlex
import shutil

from datetime import datetime, timedelta
from dateutil.parser import parse

VALID_STATUS = ( "MINUTE", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "ONCE", "ONSTART", "ONLOGON", "ONIDLE")

def get_time_2min():
    now = datetime.now()+timedelta(minutes=2)
    time = now.strftime("%H:%M")
    return time


class Job:
    def __init__(self, name):
        self.name = name
        self.cmdline = ""
        self.task_sch = "ONCE"
        self.task_time = get_time_2min()
        self.idletime = 1
    
    def __str__(self):
        return "{0} runs at {1} {2} with {3}".format(self.name, self.task_time, self.task_sch, self.cmdline )
    
    def do(self, cmdline: str):
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
        assert idletime >=1 and idletime < 999, "Idletime should be in range 1-999"
        self.idletime = idletime
        return self

    def post(self):
        iret = create(self.cmdline, 
                      task_name=self.name,
                      task_sch=self.task_sch,
                      task_st=self.task_time,
                      idletime=self.idletime)
        return iret.returncode





def process_executable(executable, folder=os.getcwd()):

    if not executable:
        return None

    if os.path.dirname(executable):
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
    exe_shex[0] = executable_sh
    return exe_shex


def create(cmdline, task_name = "test_task", task_sch = "ONCE", task_st = "13:00", idletime=7):
    # schtasks /create /tn test_task /sc DAILY /st 12:50 /tr "C:\windows\system32\calc.exe"
    
    task_exe_list = process_executable(cmdline)
    task_exe = " ".join(task_exe_list)

    task_upper = task_sch.upper()
    if task_upper.startswith("ON"):
        if task_upper in ["ONIDLE"]:
            cmd = ["schtasks" , "/create", "/tn", task_name, "/sc", task_sch , "/tr" , task_exe , "/F", "/I", str(idletime)]
        else:
            cmd = ["schtasks" , "/create", "/tn", task_name, "/sc", task_sch , "/tr" , task_exe , "/F"]
    else:
        cmd = ["schtasks" , "/create", "/tn", task_name, "/sc", task_sch , "/st", task_st, "/tr" , task_exe , "/F"]
    
    iret = subprocess.Popen(cmd)
    return iret

def delete():
    # schtasks /Delete /TN test_task3 /F
    task_name = "test_task"
    cmd  = ["scdtasks", "/Delete", "/TN", task_name, "/F"]
    iret = subprocess.Popen(cmd)
    return iret

# schtasks /Query /TN test_task /V /FO LIST
