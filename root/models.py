import os
from django.db import models
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
import json
# Create your models here.
import uuid
from django_countries.fields import CountryField

# class AnimationDestination(models.Model):
#     position = models.


class Animation(models.Model):
    CHOICES = (
        ('REACTION', 'Reaction'),
        ('BURPEE', 'Burpee'),
    )
    AndroidAssetBundle = models.URLField(max_length=2048)
    destination = JSONField()
    endTime = models.FloatField()
    iOSAssetBundle = models.URLField(max_length=2048)
    loopCount = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    startTime = models.FloatField()
    trim = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    blend = models.CharField(max_length=9,
                             choices=CHOICES)
    stitch = models.CharField(max_length=9,
                              choices=CHOICES)

    def __str__(self):
        return str(self.name)


class Movement(models.Model):
    ORIENTATION_CHOICES = (
        ('LookAhead', 'LookAhead'),
        ('lookAtTarget', 'lookAtTarget'),
        ('lookAtPosition', 'lookAtPosition'),
    )
    EASETYPE_CHOICES = (
        ('OutFlash', 'OutFlash'),
        ('InFlash', 'InFlash'),
    )

    startPointId = models.IntegerField()
    duration = models.PositiveIntegerField()
    loopCount = models.PositiveIntegerField()
    pathType = models.CharField(max_length=255)
    orientationType = models.CharField(
        max_length=50, choices=ORIENTATION_CHOICES)
    entityOrientation = JSONField()
    easeType = models.CharField(max_length=50, choices=EASETYPE_CHOICES)
    isSpeedBased = models.BooleanField()
    lookAtValue = models.FloatField()
    waypoints = JSONField()


class Effect(models.Model):
    EFFECT_TYPE_CHOICES = (
        ('2D', '2D'),
        ('3D', '3D'),
        ('2D/3D', '2D/3D'),
    )
    name = models.CharField(max_length=255)
    effectType = models.CharField(max_length=50,choices=EFFECT_TYPE_CHOICES)
    prefabName = models.CharField(max_length=25)
    iOSBundleUrl = models.URLField()
    androidBundleUrl = models.URLField()
    transform = JSONField()
    startTime = models.IntegerField()
    endTime = models.IntegerField()
    loop = models.BooleanField()
    identifiableSurfaces = models.CharField(max_length=255)


class Light(models.Model):
    LIGHT_TYPE_CHOICES = (
        ('POINT', 'Point'),
        ('AREA', 'Area'),
        ('SUN', 'Sun'),
    )
    LIGHT_SHADOW_CHOICES = (
        ('SOFT', 'SOFT'),
        ('NORMAL', 'NORMAL'),
        ('NONE', 'NONE'),
    )
    LIGHT_MODE_CHOICES = (
        ('REALTIME', 'RealTime'),
        ('Delay', 'Delay'),
    )
    name = models.CharField(max_length=255)
    type = models.CharField(choices=LIGHT_TYPE_CHOICES, max_length=50)
    range = models.IntegerField()
    startTime = models.IntegerField()
    endTime = models.IntegerField()
    intensity = models.FloatField()
    indirectMultiplier = models.IntegerField()
    mode = models.CharField(choices=LIGHT_MODE_CHOICES, max_length=50)
    lightMapUrl = models.URLField(max_length=2048)
    shadowType = models.CharField(choices=LIGHT_SHADOW_CHOICES, max_length=50)
    shadowStrength = models.IntegerField()
    color = models.CharField(max_length=30)
    exposure = models.CharField(max_length=30)
    localPosition = JSONField()
    localRotation = JSONField()


class Sound(models.Model):
    SOUND_TYPE_CHOICES = (
        ('M4A', 'M4A'),
        ('MPEG', 'MPEG'),
        ('AAC', 'AAC'),
        ('WAV', 'WAV'),
    )
    objectName = models.CharField(max_length=255)
    audioType = models.CharField(max_length=255, choices=SOUND_TYPE_CHOICES)
    audioUrl = models.URLField(max_length=2048)
    loopCount = models.PositiveIntegerField()
    volume = models.FloatField()
    pitch = models.FloatField()
    startTime = models.PositiveIntegerField()
    endTime = models.PositiveIntegerField()


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class TextToSpeech(models.Model):
    GENDER_CHOICE = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    TYPE_CHOICE = (
        ('SPECIFIC', 'Specific'),
        ('NORMAL', 'Normal'),
    )
    VOICE_EFFECT_CHOICE = (
        ('NONE', 'None'),
        ('SHADY', 'Shady'),
        ('THIN', 'Thin'),
    )
    country = CountryField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    endTime = models.FloatField()
    gender = models.CharField(choices=GENDER_CHOICE, max_length=50)
    startTime = models.FloatField()
    text = models.CharField(max_length=255)
    type = models.CharField(choices=TYPE_CHOICE, max_length=50)
    voiceEffect = models.CharField(choices=VOICE_EFFECT_CHOICE, max_length=50)
    voiceName = models.CharField(max_length=255)
    voiceVolume = models.PositiveIntegerField()


class Model(models.Model):
    def getId(self):
        return str(self.id)

    TYPE_CHOICES = (
        ('CHARACTER', 'Character'),
    )
    startTime = models.FloatField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    objectDbHash = models.CharField(max_length=255)
    AndroidAssetBundle = models.URLField()
    endTime = models.FloatField()
    iOSAssetBundle = models.URLField()
    objectId = models.UUIDField(default=uuid.uuid4, editable=False)
    layer = models.PositiveIntegerField()
    name = models.CharField(max_length=255, blank=True)
    origin = JSONField()
    animation = models.ForeignKey(
        Animation, blank=True, on_delete=models.CASCADE)
    textToSpeech = models.ForeignKey(
        TextToSpeech, blank=True, on_delete=models.CASCADE)
    movement = models.ForeignKey(
        Movement, blank=True, on_delete=models.CASCADE)
    sound = models.ForeignKey(
        Sound, blank=True, on_delete=models.CASCADE
    )
    light = models.ForeignKey(
        Light, blank=True, on_delete=models.CASCADE
    )
    effect = models.ForeignKey(
        Effect, blank=True, on_delete=models.CASCADE
    )
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
