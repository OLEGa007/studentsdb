from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from students.models.students import Student
from students.models.groups import Group


class Command(BaseCommand):
    args = '<model_name model_name ...>'
    help = "Prints to console number of student related objects database."
    models = (('student', Student), ('group', Group), ('user', User))

    def add_arguments(self, parser):
        parser.add_argument('count_item')

    def handle(self, *args, **options):
        for name, model in self.models:
            if name in options['count_item']:
                self.stdout.write('Number of %s in database is: %d' %
                                  (name, model.objects.count()))
