from crontab import CronTab
from django.http.response import Http404
from calculator.models import UserSettings

def clear_crons(user):
    try:
        cron = CronTab(user=user.username)
        cron.remove_all(comment=user.username)
        cron.write()
    except OSError:
        print("User not admin status. Cannot auto-run bot in cron tab")
        raise Http404


def make_crons(user):
    user_settings_obj = UserSettings.objects.get(user=user)
    settings_dict = dict(user_settings_obj.__dict__.items())
    if settings_dict['bot_frequency'] == 'Every hour':
        cron = CronTab(user=user.username)
        job = cron.new(command=f'export PATH="/Users/garrettlesher/github_repos/rentalpropcalculator/env/bin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/Apple/usr/bin:/Applications/Postgres.app/Contents/Versions/latest/bin" && PWD="/Users/garrettlesher/github_repos/rentalpropcalculator" && cd /Users/garrettlesher/github_repos/rentalpropcalculator && python manage.py bot_scheduler {user.username} >> cronjob.log 2>&1', comment=user.username)
        job.every(1).hours()
        cron.write()
    
    elif settings_dict['bot_frequency'] == 'Every 6 hours':
        cron = CronTab(user=user.username)
        job = cron.new(command=f'export PATH="/Users/garrettlesher/github_repos/rentalpropcalculator/env/bin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/Apple/usr/bin:/Applications/Postgres.app/Contents/Versions/latest/bin" && PWD="/Users/garrettlesher/github_repos/rentalpropcalculator" && cd /Users/garrettlesher/github_repos/rentalpropcalculator && python manage.py bot_scheduler {user.username} >> cronjob.log 2>&1', comment=user.username)
        job.every(6).hours()
        cron.write()

    elif settings_dict['bot_frequency'] == '2x/day':
        cron = CronTab(user=user.username)
        job = cron.new(command=f'export PATH="/Users/garrettlesher/github_repos/rentalpropcalculator/env/bin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/Apple/usr/bin:/Applications/Postgres.app/Contents/Versions/latest/bin" && PWD="/Users/garrettlesher/github_repos/rentalpropcalculator" && cd /Users/garrettlesher/github_repos/rentalpropcalculator && python manage.py bot_scheduler {user.username} >> cronjob.log 2>&1', comment=user.username)
        job.every(12).hours()
        cron.write()

    elif settings_dict['bot_frequency'] == '1x/day':
        cron = CronTab(user=user.username)
        job = cron.new(command=f'export PATH="/Users/garrettlesher/github_repos/rentalpropcalculator/env/bin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/Apple/usr/bin:/Applications/Postgres.app/Contents/Versions/latest/bin" && PWD="/Users/garrettlesher/github_repos/rentalpropcalculator" && cd /Users/garrettlesher/github_repos/rentalpropcalculator && python manage.py bot_scheduler {user.username} >> cronjob.log 2>&1', comment=user.username)
        job.hour.on(17)
        job.minute.on(0)
        cron.write()

    elif settings_dict['bot_frequency'] == 'Every other day':
        cron = CronTab(user=user.username)
        job = cron.new(command=f'export PATH="/Users/garrettlesher/github_repos/rentalpropcalculator/env/bin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/Apple/usr/bin:/Applications/Postgres.app/Contents/Versions/latest/bin" && PWD="/Users/garrettlesher/github_repos/rentalpropcalculator" && cd /Users/garrettlesher/github_repos/rentalpropcalculator && python manage.py bot_scheduler {user.username} >> cronjob.log 2>&1', comment=user.username)
        job.day.every(2)
        job.hour.on(17)
        job.minute.on(0)
        cron.write()

    elif settings_dict['bot_frequency'] == '1x/week':
        cron = CronTab(user=user.username)
        job = cron.new(command=f'export PATH="/Users/garrettlesher/github_repos/rentalpropcalculator/env/bin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/Apple/usr/bin:/Applications/Postgres.app/Contents/Versions/latest/bin" && PWD="/Users/garrettlesher/github_repos/rentalpropcalculator" && cd /Users/garrettlesher/github_repos/rentalpropcalculator && python manage.py bot_scheduler {user.username} >> cronjob.log 2>&1', comment=user.username)
        job.hour.on(17)
        job.minute.on(0)
        job.dow.on('MON')
        cron.write()

    elif settings_dict['bot_frequency'] == '1x/month':
        cron = CronTab(user=user.username)
        job = cron.new(command=f'export PATH="/Users/garrettlesher/github_repos/rentalpropcalculator/env/bin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/Apple/usr/bin:/Applications/Postgres.app/Contents/Versions/latest/bin" && PWD="/Users/garrettlesher/github_repos/rentalpropcalculator" && cd /Users/garrettlesher/github_repos/rentalpropcalculator && python manage.py bot_scheduler {user.username} >> cronjob.log 2>&1', comment=user.username)
        job.every(1).months()
        job.hour.on(17)
        cron.write()

    else:
        cron = CronTab(user=user.username)
        cron.remove_all()
        cron.write()

