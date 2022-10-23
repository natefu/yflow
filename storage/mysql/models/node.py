from django.db import models
from django.utils.translation import gettext_lazy as _
from constants import READY, NODE_STATE_CHOICES

from .ticket import Ticket


class Node(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.PROTECT, related_name='nodes', blank=False, null=False,
        verbose_name=_('I18N_MSG_MODEL_TICKET')
    )
    identifier = models.CharField(max_length=32, verbose_name=_('I18N_MSG_MODEL_IDENTIFIER'))
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('I18N_MSG_MODEL_NAME'))
    state = models.CharField(
        max_length=32, default=READY, choices=NODE_STATE_CHOICES, blank=False, null=False,
        verbose_name=_('I18N_MSG_MODEL_STATE')
    )
    element = models.CharField(max_length=32, blank=False, null=False, verbose_name=_('I18N_MSG_MODEL_ELEMENT'))
    variables = models.JSONField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_VARIABLES'))
    context = models.JSONField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_CONTEXT'))
    scheme = models.JSONField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_SCHEME'))
    condition = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('I18N_MSG_MODEL_CONDITION'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('I18N_MSG_MODEL_CREATED'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('I18N_MSG_MODEL_UPDATED'))
    completed = models.DateTimeField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_COMPLETED'))

    class Meta:
        verbose_name = _('I18N_MSG_MODEL_NODE')
        verbose_name_plural = _('I18N_MSG_MODEL_NODE')
        unique_together = ('ticket', 'identifier')
        db_table = 'yflow_node'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}-{self.identifier}'


class NodeFlow(models.Model):
    source = models.ForeignKey(
        Node, on_delete=models.PROTECT, related_name='source', verbose_name=_('I18N_MSG_MODEL_SOURCE')
    )
    target = models.ForeignKey(
        Node, on_delete=models.PROTECT, related_name='target', verbose_name=_('I18N_MSG_MODEL_TARGET')
    )
    condition = models.CharField(blank=True, null=True, max_length=128, verbose_name=_('I18N_MSG_MODEL_CONDITION'))
    name = models.CharField(max_length=128, verbose_name=_('I18N_MSG_MODEL_NAME'))

    class Meta:
        verbose_name = _('I18N_MSG_MODEL_FLOW')
        verbose_name_plural = _('I18N_MSG_MODEL_FLOW')
        unique_together = ('source', 'target')
        db_table = 'yflow_nodeflow'
        ordering = ('id',)

    def __str__(self):
        return f'{self.source}-{self.target}'
