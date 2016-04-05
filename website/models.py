from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=100)
    dedication = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    tenor = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.dedication + ", " + self.name + ", " + self.county


class Performance(models.Model):
    bellboardId = models.CharField(max_length=10)
    association = models.CharField(max_length=100)
    duration = models.DurationField()
    date = models.DateTimeField()
    method = models.CharField(max_length=1000)
    changes = models.IntegerField()
    composer = models.CharField(max_length=100)
    place = models.ForeignKey(Place)
    details = models.TextField()

    composer.null = True
    composer.blank = True

    details.null = True
    details.blank = True

    association.null = True
    association.blank = True

    duration.null = True
    duration.blank = True

    def __str__(self):
        return str(self.changes) + " " + self.method

class Footnote(models.Model):
    value = models.CharField(max_length=300)
    performance = models.ForeignKey(Performance)

    def __str__(self):
        return self.value

class RingingName(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Ringer(models.Model):
    name = models.CharField(max_length=100)
    ringingname = models.ForeignKey(RingingName, on_delete=models.SET_NULL)

    ringingname.null = True

    def __str__(self):
        additional = ""
        if self.ringingname is not None:
            additional = " (Linked)"
        return self.name + additional

class RingerPerformance(models.Model):
    bell = models.CharField(max_length=10)
    conductor = models.BooleanField()
    ringer = models.ForeignKey(Ringer, on_delete=models.SET_NULL)
    performance = models.ForeignKey(Performance)

    ringer.null = True

    def __str__(self):
        return self.ringer.name + " on " + str(self.bell) + " for " + str(self.performance)




