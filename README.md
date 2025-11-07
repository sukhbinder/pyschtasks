# pyschtasks
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
