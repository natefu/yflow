from django.db import models
from django.utils.translation import gettext_lazy as _
from constants import READY, INSTANCE_STATE_CHOICES

from .node import Node


class Instance(models.Model):
    node = models.ForeignKey(
        Node, on_delete=models.PROTECT, related_name='instances', blank=False, null=False,
        verbose_name=_('I18N_MSG_MODEL_TICKET')
    )
    state = models.CharField(
        max_length=32, default=READY, choices=INSTANCE_STATE_CHOICES, blank=False, null=False,
        verbose_name=_('I18N_MSG_MODEL_STATE')
    )
    scheme = models.JSONField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_SCHEME'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('I18N_MSG_MODEL_CREATED'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('I18N_MSG_MODEL_UPDATED'))
    completed = models.DateTimeField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_COMPLETED'))

    class Meta:
        verbose_name = _('I18N_MSG_MODEL_NODE')
        verbose_name_plural = _('I18N_MSG_MODEL_NODE')
        db_table = 'yflow_instance'
        ordering = ('id',)

    def __str__(self):
        return f'{self.node}-instances'
