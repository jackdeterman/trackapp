import time
import math 

from pprint import pprint

from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models
from django.db.models.fields import CharField, DateField, TextField, FloatField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from .milestones import EVENT_MILESTONES

class User(AbstractUser):
    team = models.ManyToManyField("Team", related_name="team_members")

    def get_prs(self):
        prs = {}
        for result in self.results.all():
            if not result.event in prs:
                prs[result.event] = result
            else:
                if result.event.unit == 'inches':
                    if result.result > prs[result.event].result:
                        prs[result.event] = result
                else:
                    if result.result < prs[result.event].result:
                        prs[result.event] = result
        return prs

    def __str__(self):
        return f"{self.username} ({self.id})"
admin.site.register(User)



class Team(models.Model):
    """A team represents a single athletic team like NAHS Boys track"""
    name = CharField(max_length=100)
    coaches = ManyToManyField(User, related_name="teams_coached")
    athletes = ManyToManyField('User', related_name="teams")

    def __str__(self):
        return f"{self.name}"

admin.site.register(Team)


class Event(models.Model):
    name = CharField(max_length=100)

    unit_choices = [
        ('inches', 'Inches'),
        ('seconds', 'Seconds'),
    ]
    unit = CharField(max_length=100, default='seconds')

    def __str__(self):
        return self.name
admin.site.register(Event)


class Meet(models.Model):
    date = DateField()
    description = TextField()
    team = ForeignKey('Team', on_delete=models.CASCADE)
    season = ForeignKey('Season', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description}: {self.date}"

    def javascript_time(self):
        return int(time.mktime(self.date.timetuple()))
admin.site.register(Meet)


class Result(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='results')
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE, related_name='results')
    result = FloatField()
    method_choices = [
        ('NA', 'NA'),
        ('Hand', 'Hand'),
        ('FAT','FAT')
    ]
    method = CharField(max_length=100, default='NA')
    personal_rank = models.IntegerField(default=-1)
    milestones = TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.result}"

    @property
    def formatted_result(self):
        if self.event.unit == "inches":
            feet, inches = divmod(self.result, 12)
            return f"{int(feet):02}'{inches:05.2f}"
        elif self.event.unit == 'seconds':
            minutes, seconds = divmod(self.result, 60)
            return f"{int(minutes):02}:{seconds:05.2f}"
        else:
            return f"{self.result}"

    @property
    def milestone_num(self):
        """Use dictionary to lookup which milestone we are at if any"""
        milestones = EVENT_MILESTONES.get(self.event.name)
        if not milestones:
            return None
        for x, milestone in enumerate(milestones):
            if self.event.unit == "inches":
                if self.result >= milestone:
                    return x
            elif self.event.unit == 'seconds':
                if self.result < milestone:
                    return x
        return None

    def get_milestone_value(self, milestone_num):
        return EVENT_MILESTONES[self.event.name][milestone_num]
admin.site.register(Result)


def calculate_result_stats(user):
    results_by_event = {}
    for result in user.results.all().order_by('result'):
        results_by_event.setdefault(result.event, []).append(result)

    for event, results in results_by_event.items():
        if event.unit == 'inches':
            reverse = True
        else:
            reverse = False

        # Order by performance and figure out ranking
        for rank, result in enumerate(
            sorted(results, key=lambda x: x.result, reverse=reverse)):

            if rank == 0:
                result.milestones = 'Personal Best!'
            else:
                result.milestones = ''
            result.personal_rank = rank+1
            result.save()


        last_milestone_num = None
        for result in sorted(results, key=lambda x: x.meet.date):
            milestone_num = result.milestone_num
            if milestone_num is None:
                continue
            if (last_milestone_num is None) or (milestone_num < last_milestone_num):
                last_milestone_num = milestone_num
                milestone_result = Result(result=result.get_milestone_value(milestone_num), event=event)
                milestone_msg = f"Broke {milestone_result.formatted_result}."
                if len(result.milestones):
                    result.milestones += f" {milestone_msg}"
                else:
                    result.milestones = milestone_msg
                result.save()

    

class Goal(models.Model):
    user = models.ForeignKey(User, related_name="goals", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="goals_created", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="event_goals", on_delete=models.CASCADE)
    season = models.ForeignKey("Season", related_name="season_goals", null=True, on_delete=models.CASCADE)
    meet = models.ForeignKey(Meet, related_name="meet_goals", null=True, on_delete=models.CASCADE)
    value = FloatField()

class QualifyingLevel(models.Model):
    description = CharField(max_length=255)
    event = models.ForeignKey(Event, related_name="qualifying_levels", on_delete=models.CASCADE)
    season = models.ForeignKey("Season", related_name="qualifying_levels", null=True, on_delete=models.CASCADE)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    gender = models.CharField(default='male', max_length=255, choices=GENDER_CHOICES)
    value = FloatField()

    @property
    def formatted_value(self):
        if self.event.unit == "inches":
            feet, inches = divmod(self.value, 12)
            return f"{int(feet):02}'{inches:05.2f}"
        elif self.event.unit == 'seconds':
            minutes, seconds = divmod(self.value, 60)
            return f"{int(minutes):02}:{seconds:05.2f}"
        else:
            return f"{self.value}"


class Season(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
            return f"{self.name}"

admin.site.register(Season)