from django.db import models
from django.utils.translation import gettext_lazy as _
from constants import READY, TICKET_STATE_CHOICES

from .process import Process


class Ticket(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('I18N_MSG_MODEL_NAME'))
    state = models.CharField(
        max_length=32, default=READY, choices=TICKET_STATE_CHOICES, blank=False, null=False,
        verbose_name=_('I18N_MSG_MODEL_NAME')
    )
    variables = models.JSONField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_VARIABLES'))
    context = models.JSONField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_CONTEXT'))
    scheme = models.JSONField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_VARIABLES'))
    process = models.ForeignKey(
        Process, on_delete=models.PROTECT, related_name='tickets', blank=True, null=True,
        verbose_name=_('I18N_MSG_MODEL_PROCESS')
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('I18N_MSG_MODEL_CREATED'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('I18N_MSG_MODEL_UPDATED'))
    completed = models.DateTimeField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_COMPLETED'))

    class Meta:
        verbose_name = _('I18N_MSG_MODEL_TICKET')
        verbose_name_plural = _('I18N_MSG_MODEL_TICKET')
        db_table = 'yflow_ticket'
        ordering = ('id',)

    def __str__(self):
        return self.name
