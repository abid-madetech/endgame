from django.db import models
import uuid


class KSBType(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)


class KSB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(unique=True)
    ksb_type = models.ForeignKey(KSBType, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, related_name='ksbs')
    completed = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
