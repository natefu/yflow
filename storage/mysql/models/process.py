from django.db import models
from django.utils.translation import gettext_lazy as _


class Process(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('I18N_MSG_MODEL_NAME'))
    version = models.IntegerField(default=1, verbose_name=_('I18N_MSG_MODEL_VERSION'))
    scheme = models.JSONField(blank=True, null=True, verbose_name=_('I18N_MSG_MODEL_VARIABLES'))
    deprecated = models.BooleanField(default=False, verbose_name=_('I18N_MSG_MODEL_DEPRECATED'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('I18N_MSG_MODEL_CREATED'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('I18N_MSG_MODEL_UPDATED'))

    class Meta:
        verbose_name = _('I18N_MSG_MODEL_PROCESS')
        verbose_name_plural = _('I18N_MSG_MODEL_PROCESS')
        db_table = 'yflow_process'
        unique_together = ('name', 'version')
        ordering = ('id',)

    def __str__(self):
        return self.name
