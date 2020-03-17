from django.db import models
import requests
from datetime import datetime, timedelta, date
import time


class Action(models.Model):
    name = models.CharField(max_length=64, blank=True)
    route = models.CharField(max_length=64)
    params = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.getName()

    def getName(self):
        return self.name if self.name else self.route


class Node(models.Model):
    name = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(protocol='IPv4')
    is_active = models.BooleanField()
    actions = models.ManyToManyField(Action)

    def __str__(self):
        return self.name


class WeekDay(models.Model):
    day = models.CharField(max_length=8)


class Scenario(models.Model):
    TYPE_ONE_TIME = 0
    TYPE_DELAYED = 1
    TYPE_EVERYDAY = 2
    TYPE_WORKDAYS = 3
    TYPE_WEEKEND = 4
    TYPES = [
        (TYPE_ONE_TIME, 'One Time'),
        (TYPE_DELAYED, 'Delayed'),
        (TYPE_EVERYDAY, 'Everyday'),
        (TYPE_WORKDAYS, 'Workdays'),
        (TYPE_WEEKEND, 'Weekend'),
        (TYPE_WEEKEND, 'Day Of Week'),
    ]

    is_running = models.BooleanField(default=False)
    name = models.CharField(max_length=64)
    type = models.IntegerField(choices=TYPES, default=TYPE_ONE_TIME)
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def reset_actions(self):
        for sc_action in self.scenarioaction_set:
            sc_action.is_executed = 0
            sc_action.save()

    def run(self):
        self.is_running = 1
        self.start_time = datetime.now()
        self.save()

        self.reset_actions()

        for sc_action in self.scenarioaction_set:
            sc_action.can_run() and sc_action.run()

    def stop(self):
        self.is_running = 1
        self.save()
        self.reset_actions()


class ScenarioAction(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    scenario = models.ForeignKey(Scenario, on_delete=models.DO_NOTHING)
    node = models.ForeignKey(Node, on_delete=models.DO_NOTHING)
    action = models.ForeignKey(Action, on_delete=models.DO_NOTHING)
    is_executed = models.BooleanField(default=0)
    at_day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, blank=True)
    at_time = models.TimeField(default=None, blank=True)

    def scenario_name(self):
        return self.scenario.name

    def run(self):
        self.is_executed = 1
        self.save()
        return requests.get('http://' + self.node.ip + '/' + self.action.route).content

    def can_run(self):
        if self.is_executed:
            return False

        # Run immediate
        if self.scenario.type == Scenario.TYPE_ONE_TIME:
            return True
        elif self.scenario.type == Scenario.TYPE_DELAYED:
            # Run immediate
            if not self.at_time:
                return True
            # Run with very short delay
            if self.can_run_after_several_seconds():
                return True
            else:
                return self.can_run_after()
        # Skip specific days, if is set
        elif self.scenario.type == Scenario.TYPE_WEEKEND:
            if not self.is_weekend():
                return False
        elif self.scenario.type == Scenario.TYPE_WORKDAYS:
            if self.is_weekend():
                return False
        # Check time
        if self.scenario.type in [Scenario.TYPE_EVERYDAY, Scenario.TYPE_WEEKEND, Scenario.TYPE_WORKDAYS]:
            return self.is_desired_time()

    # def get_time(self):
    #     return datetime.strptime(self.at_time, '%H:%M:%S').time()

    def can_run_after_several_seconds(self):
        after_time = self.at_time
        if after_time.hour == 0 and after_time.minute == 0 and after_time.second > 0:
            time.sleep(after_time.second)
            return True
        else:
            return False

    def can_run_after(self):
        after_time = self.at_time
        delta_after = timedelta(hours=after_time.hour, minutes=after_time.minute, seconds=after_time.second)
        return (datetime.now() - (self.scenario.start_time + delta_after)).total_seconds() >= 0

    def is_desired_time(self):
        return (datetime.now() - datetime.combine(date.today(), self.at_time)).total_seconds() >= 0

    def is_weekend(self):
        return self.at_day in [5, 6]

    def is_weekday(self):
        return self.at_day is not None and not self.is_weekend()
