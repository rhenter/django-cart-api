from ckeditor.widgets import CKEditorWidget
from django import forms
from django.conf import settings
from django.contrib import admin

from .models import SMTPSettings, TermsOfService

admin.site.site_header = f'{settings.APP_NAME} Admin'
admin.site.site_title = settings.APP_NAME
admin.site.enable_nav_sidebar = False


class TermsOfServiceForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = TermsOfService
        fields = '__all__'


@admin.register(SMTPSettings)
class SMTPSettingsAdmin(admin.ModelAdmin):
    model = SMTPSettings
    list_display = [
        'host',
        'port',
        'username',
        'timeout',
        'use_tls',
        'use_ssl',
        'is_active',
    ]
    exclude = ['code']

    def has_add_permission(self, *args, **kwargs):
        return not SMTPSettings.objects.exists()
