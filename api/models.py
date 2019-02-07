from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(models.Model):
    """
    Clients model.
    """
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField()
    position = models.CharField(max_length=64)


class Upload(models.Model):
    """
    File upload model.
    """
    ACTIVE_STATE = 'A'
    COMPLETED_STATE = 'C'
    UNKNOWN_STATE = 'U'
    STATES = (
        (UNKNOWN_STATE, _('Unknown')),
        (ACTIVE_STATE, _('Active')),
        (COMPLETED_STATE, _('Completed'))
    )
    state = models.CharField(
        max_length=1, choices=STATES, default=UNKNOWN_STATE
    )
    file_name = models.CharField(max_length=128, null=True)
    file_size = models.PositiveIntegerField(null=True)
    started = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True)
