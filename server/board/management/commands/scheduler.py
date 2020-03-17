from django.core.management.base import BaseCommand, CommandError
from board.models import Scenario


class Command(BaseCommand):
    help = 'Help me, please'

    def handle(self, *args, **options):
        for scenario in Scenario.objects.all().filter(is_running=True):
            self.stdout.write('%s' % scenario.name)
            for sc_action in scenario.scenarioaction_set.all():
                self.stdout.write(' %s %s: %s' % ('+' if sc_action.is_executed else '-', sc_action.node.name, sc_action.action.getName()))
