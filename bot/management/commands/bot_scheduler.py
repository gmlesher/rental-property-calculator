from django.contrib.auth.models import User
from calculator.models import UserSettings
from django.core.management.base import BaseCommand

from bot.utils import bot_scheduler

class Command(BaseCommand):
    help = 'Create bot scheduler for user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Indicates the user to be associated with certain bot schedule')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        user = User.objects.get(username=username)
        user_settings_obj = UserSettings.objects.get(user=user.pk)
        settings_dict = dict(user_settings_obj.__dict__.items())
        if settings_dict['bot_frequency']:
            self.stdout.write("Running bot: " + str(settings_dict['bot_frequency']))
            bot_scheduler(user)
        