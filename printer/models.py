import os
import datetime
from enum import Enum

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from tinymce.models import HTMLField
from remote_printer.users.models import CustomUser

from core.models import MetaDataModel


class PrintRequest(MetaDataModel):

    class STATUS(Enum):
        requested = (1, "Requested")
        printed = (2, "Printed")
        rejected = (3, "Rejected")
        cancelled = (4, "Cancelled")
        paid = (5, "Paid")

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=[x.value for x in STATUS], default=STATUS.get_value("requested"))
    description = HTMLField('Description', blank=True)
    printed_on = models.DateTimeField(blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    rejected_on = models.DateTimeField(blank=True, null=True)
    paid_on = models.DateField(blank=True, null=True)
    is_both_side = models.BooleanField(default=True, verbose_name="Both Sides")
    is_color = models.BooleanField(default=False, verbose_name="Color")
    no_of_front_page = models.PositiveIntegerField(default=0, verbose_name="Want some front pages")
    no_of_blank_page = models.PositiveIntegerField(default=0, verbose_name="Want some blank pages")
    no_of_page = models.PositiveIntegerField(default=0)
    no_of_bnw_page = models.PositiveIntegerField(default=0)
    no_of_color_page = models.PositiveIntegerField(default=0)
    amount = models.FloatField(default=0)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _('Print Request')
        verbose_name_plural = _('Print Requests')

    def __str__(self):
        return self.client.email

    def get_absolute_url(self):
        return reverse("printer:user_print_request_list")


class PrintRequestFile(MetaDataModel):

    def print_request_file_path(self, filename):
        # pylint: disable=no-member
        basefilename, file_extension = os.path.splitext(filename)
        randomstr = datetime.datetime.now().strftime('%d-%m-%Y_%I:%M:%S,%f')
        if len(basefilename) > 101:
            basefilename = basefilename[:101]
        return 'print/{client_id}/{print_request_id}/{basename}_{random_string}{ext}'.format(
            client_id=self.print_request.client.pk, print_request_id=self.print_request,
            basename=basefilename, random_string=randomstr, ext=file_extension)


    id = models.BigAutoField(primary_key=True)
    print_request = models.ForeignKey(PrintRequest, on_delete=models.CASCADE)
    document = models.FileField(upload_to=print_request_file_path, null=True)
    no_of_copies = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _('Print Request File')
        verbose_name_plural = _('Print Requests Files')

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.print_request.pk}-{self.print_request.client}"

    def document_name(self):
        name, ext = os.path.splitext(self.document.name)
        name = os.path.basename(name).split('_')
        name = '_'.join(name[0:len(name)-2]) + ext
        return name


class Price(MetaDataModel):

    page = models.FloatField()
    bnw_page = models.FloatField()
    color_pages = models.FloatField()
    wef = models.DateTimeField(auto_now_add=True)
    created_at = None

    class Meta:
        ordering = ["-wef"]
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __str__(self):
        return f'{self.wef.date()}'
