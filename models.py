from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models
import time


from django.db.models.fields import CharField, DateField, TextField, FloatField
from django.db.models.fields.related import ForeignKey, ManyToManyField

class User(AbstractUser):
    team = models.TextField()

    def get_prs(self):
        prs = {}
        for result in self.results.all():
            if not result.event in prs:
                prs[result.event] = result
            else:
                if result.event.unit == 'Feet--Inches':
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
    """A team represents a single athletic team like NAHS track"""
    name = CharField(max_length=100)
    coaches = ManyToManyField(User, related_name="teams_coached")


class Event(models.Model):
    name = CharField(max_length=100)

    unit_choices = [
        ('Feet--Inches', 'Feet--Inches'),
        ('Minutes--Seconds', 'Minutes--Seconds'),
    ]
    unit = CharField(max_length=100, default='Minutes--Seconds')

    def __str__(self):
        return self.name
admin.site.register(Event)




class Meet(models.Model):
    date = DateField()
    description = TextField()

    def __str__(self):
        return f"{self.description}: {self.date}"

    def javascript_time(self):
        return int(time.mktime(self.date.timetuple()))

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

    def formatted_result(self):
        if self.event.unit == "Feet--Inches":
            feet, inches = divmod(self.result, 12)
            return f"{int(feet):02}'{inches:05.2f}"
        elif self.event.unit == 'Minutes--Seconds':
            minutes, seconds = divmod(self.result, 60)
            return f"{int(minutes):02}:{seconds:05.2f}"
        else:
            return f"{self.result}"

