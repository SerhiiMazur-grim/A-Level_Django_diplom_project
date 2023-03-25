from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Ticket(models.Model):
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, _('Low')),
        (PRIORITY_MEDIUM, _('Medium')),
        (PRIORITY_HIGH, _('High')),
    )

    STATUS_IN_PROGRESS = 'In progress'
    STATUS_RESOLVED = 'Resolved'
    STATUS_REJECTED = 'Rejected'
    STATUS_RESTORED = 'Restored'

    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, _('In progress')),
        (STATUS_RESOLVED, _('Resolved')),
        (STATUS_REJECTED, _('Rejected')),
        (STATUS_RESTORED, _('Restored')),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tickets'

    def __str__(self):
        return self.subject

    def resolved(self):
        self.status = self.STATUS_RESOLVED
        self.save()

    def rejected(self):
        self.status = self.STATUS_REJECTED
        self.save()

    def restored(self):
        self.status = self.STATUS_RESTORED
        self.save()
    
    def get_comments(self):
        return self.comments.all()
