# pyschtasks

[![PyPI](https://img.shields.io/pypi/v/pyschtasks.svg)](https://pypi.org/project/pyschtasks/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/pyschtasks?include_prereleases&label=changelog)](https://github.com/sukhbinder/pyschtasks/releases)
[![Tests](https://github.com/sukhbinder/pyschtasks/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/pyschtasks/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/pyschtasks/blob/master/LICENSE)



A simplified api to call/schedule tasks in windows using `schtasks`

# Install
`pip install pyschtasks`

# Usage

Here's how to schedule a a task to run a command:

```python
import stask

# Schedule a one time job for 6:30 pm today
job = stask.Job("test_task")
job.do("calc.exe").at("6:30pm").post()

# Schedule a job to run daily at 8:00 AM
job = stask.Job("daily_task")
job.do("notepad.exe").at("8am").daily().post()

# Schedule a job for every 10 minutes
job = stask.Job("every_10_min")
job.do("explorer.exe").every(10).minute().post()

# Delete a scheduled task
job = stask.Job("test_task")
job.delete()

# Run a scheduled task
job = stask.Job("daily_task")
job.run()

# List a scheduled task
job = stask.Job("daily_task")
job.list()
```

# CLI Usage

You can also use `pyschtasks` from the command line:

## Create a task

```bash
stask create -n my_task -c "notepad.exe" -s DAILY -a "09:00"
```

## Delete a task

```bash
stask delete -n my_task
```

## List a task

```bash
stask list -n my_task
```
