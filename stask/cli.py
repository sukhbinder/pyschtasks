import argparse
from stask import stask as st

def main():
    parser = argparse.ArgumentParser(description="A simplified api to call/schedule tasks in windows using schtasks")
    subparsers = parser.add_subparsers(dest='command')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new scheduled task')
    create_parser.add_argument('-n', '--name', required=True, help='Name of the task')
    create_parser.add_argument('-c', '--cmd', required=True, help='Command to execute')
    create_parser.add_argument('-s', '--schedule', default='ONCE', choices=['ONCE', 'DAILY', 'WEEKLY', 'MONTHLY', 'ONIDLE'], help='Schedule of the task')
    create_parser.add_argument('-a', '--at', help='Time to run the task (e.g., 14:30)')
    create_parser.add_argument('-e', '--every', type=int, help='Run every N minutes/hours/days/weeks/months')
    create_parser.add_argument('--ac-only', action='store_true', help='Run the task only when the system is on AC power')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a scheduled task')
    delete_parser.add_argument('-n', '--name', required=True, help='Name of the task')

    # List command
    list_parser = subparsers.add_parser('list', help='List a scheduled task')
    list_parser.add_argument('-n', '--name', required=True, help='Name of the task')

    args = parser.parse_args()

    if args.command == 'create':
        job = st.Job(args.name)
        job.do(args.cmd)
        if args.at:
            job.at(args.at)

        if args.ac_only:
            job.run_on_ac_only()

        if args.schedule == 'DAILY':
            job.daily()
        elif args.schedule == 'WEEKLY':
            job.weekly()
        elif args.schedule == 'MONTHLY':
            job.monthly()
        elif args.schedule == 'ONIDLE':
            job.onidle()
        else:
            job.once()

        if args.every:
            job.every(args.every)
            if args.schedule == 'HOURLY':
                job.hour()
            elif args.schedule == 'DAILY':
                job.day()
            elif args.schedule == 'WEEKLY':
                job.week()
            elif args.schedule == 'MONTHLY':
                job.month()
            else:
                job.minute()

        job.post()

    elif args.command == 'delete':
        job = st.Job(args.name)
        job.delete()

    elif args.command == 'list':
        job = st.Job(args.name)
        job.list()

if __name__ == '__main__':
    main()
