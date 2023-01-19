from django.db import models
from django.utils.translation import gettext_lazy as _


class ExcelFile(models.Model):
    api_document_id = models.BigIntegerField(verbose_name=_('Document Id'))
    file_url = models.URLField(verbose_name=_('File Url'))
    file = models.FileField(
        upload_to='excel_files/',
        null=True,
        blank=True,
        help_text=_('Excel file'),
    )
    output_file = models.FileField(
        upload_to='downloaded/',
        null=True,
        blank=True,
        help_text=_('Output file'),
    )
    is_download = models.BooleanField(
        default=False,
        help_text=_('Is Downloaded'),
    )
    is_finished = models.BooleanField(
        default=False,
        help_text=_('Is Finished'),
    )
    retry_count = models.PositiveSmallIntegerField(
        default=0,
        help_text=_('Retry Count'),
    )
    data = models.JSONField(
        null=True,
        blank=True,
        help_text=_('Data'),
    )

    class Meta:
        verbose_name = _("Excel Değişken Dosyası")
        verbose_name_plural = _("Excel Değişken Dosyaları")
        ordering = ('id',)
