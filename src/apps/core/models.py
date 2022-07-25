from django.db import models
from django.utils.translation import gettext_lazy as _
from django_models.models import SignalsModel, TimestampedModel, UUIDModel
from django_models.models.generic import CodeModel

TERMS_OF_SERVICE_TYPES = (
    ('user', _('User')),
    ('store', _('Store')),
)


class BaseModel(TimestampedModel, UUIDModel, SignalsModel):
    class Meta:
        abstract = True


class TermsOfService(BaseModel):
    profile_type = models.CharField(
        max_length=18, choices=TERMS_OF_SERVICE_TYPES, null=True, blank=True, verbose_name=_('Profile Type')
    )
    text = models.TextField(_('Terms of Service text'), blank=True)

    class Meta:
        verbose_name = _('Terms of Service')
        verbose_name_plural = _('Terms of service')


class SMTPSettings(BaseModel):
    host = models.CharField(max_length=200, blank=True, verbose_name=_('Host'))
    port = models.IntegerField(blank=True, verbose_name=_('Port'))
    username = models.CharField(max_length=128, blank=True, verbose_name=_('User'))
    password = models.CharField(max_length=128, blank=True, verbose_name=_('Password'))
    use_tls = models.BooleanField(default=False, verbose_name=_('Use TLS'))
    use_ssl = models.BooleanField(default=False, verbose_name=_('Use SSL'))
    timeout = models.IntegerField(blank=True, default=10, verbose_name=_('Timeout'))
    ssl_keyfile = models.FileField(blank=True, null=True, verbose_name=_('SSL Keyfile'))
    ssl_certfile = models.FileField(blank=True, null=True, verbose_name=_('SSL Certfile'))
    is_active = models.BooleanField(default=False, verbose_name=_('Active'))

    class Meta:
        verbose_name = _('Email Settings')
        verbose_name_plural = _('Email Settings')

    def __str__(self):
        return '{}:{}'.format(self.host, self.port)

    def pre_save(self, save_kwargs):
        if save_kwargs["is_creation"] and type(self).objects.exists():
            raise ValueError("This model has already its record.")
