import os
from django.db import models
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
import json
# Create your models here.


# class AnimationDestination(models.Model):
#     position = models.

class Animation(models.Model):
    CHOICES = (
        ('REACTION', 'Reaction'),
        ('BURPEE', 'Burpee')
    )
    AndroidAssetBundle = models.URLField(max_length=2048)
    destination = JSONField()
    endTime = models.PositiveIntegerField()
    iOSAssetBundle = models.URLField(max_length=2048)
    loopCount = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    startTime = models.IntegerField()
    trim = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    blend = models.CharField(max_length=9,
                             choices=CHOICES)
    stitch = models.CharField(max_length=9,
                              choices=CHOICES)

    def __str__(self):
        return str(self.name)


class Movement(models.Model):
    pass


class Model(models.Model):
    def getId(self):
        return str(self.id)
    name = models.CharField(max_length=255, blank=True)
    animation = models.ForeignKey(
        Animation, blank=True, on_delete=models.CASCADE)
    # movement = models.ForeignKey(
    #     Movement, blank=True, on_delete=models.CASCADE)
    if not os.path.exists("jsonDirectory"):
        os.mkdir("jsonDirectory")

    def save(self, *args, **kwargs):
        data = {
            "AndroidAssetBundle": self.animation.AndroidAssetBundle,
            "animationId": self.animation.id,
            "destination": self.animation.destination,
            "endTime": self.animation.endTime,
            "iOSAssetBundle": self.animation.iOSAssetBundle,
            "loopCount": self.animation.loopCount,
            "name": self.animation.name,
            "startTime": self.animation.startTime,
            "trim": self.animation.trim,
            "blend": self.animation.blend,
            "stitch": self.animation.stitch,
        }
        super().save(*args, **kwargs)
        with open(f"jsonDirectory/Model-{self.id}.json", "w") as outfile:
            json.dump(data, outfile)

    def __str__(self):
        return str(self.name)
