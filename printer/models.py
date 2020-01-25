import os
import datetime
from enum import Enum

from django.db import models
from django.utils.translation import ugettext_lazy as _

from tinymce import HTMLField

from remote_printer.users.models import CustomUser
from core.models import MetaDataModel

class PrintRequest(MetaDataModel):

    class STATUS(Enum):
        _1 = (1, "Requested")
        _2 = (2, "Printed")
        _3 = (3, "Rejected")
        _4 = (4, "Partly Paid")
        _5 = (5, "Paid")

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=[x.value for x in STATUS])
    description = HTMLField('Description')
    printed_on = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    paid_on = models.DateField(blank=True, null=True)
    is_both_sides = models.BooleanField(default=True, verbose_name="Both Sides")
    is_color = models.BooleanField(default=False, verbose_name="Color")
    front_page = models.IntegerField(default=0, verbose_name="Want some front pages")
    blank_pages = models.IntegerField(default=0, verbose_name="Want some front pages")
    no_of_bnw_Single_pages = models.IntegerField(default=0)
    no_of_bnw_double_pages = models.IntegerField(default=0)
    no_of_color_Single_pages = models.IntegerField(default=0)
    no_of_color_double_pages = models.IntegerField(default=0)
    amount_paid = models.FloatField(default=0)


    class Meta:
        ordering = ["-created_at"]
        verbose_name = _('Print Request')
        verbose_name_plural = _('Print Requests')

    def __str__(self):
        return self.client

    # def get_absolute_url(self):
    #     return reverse("books_book_detail", kwargs={"pk": self.pk})


class PrintRequestFile(models.Model):

    def print_request_file_path(self, filename):
        basefilename, file_extension = os.path.splitext(filename)
        randomstr = datetime.datetime.now().strftime('%d-%m-%Y_%I:%M:%S,%f')
        return 'print/{client_id}/{basename}_{random_string}{ext}'.format(
            client_id=self.print_request_id.client, basename=basefilename, random_string=randomstr, ext=file_extension)


    id = models.BigAutoField(primary_key=True)
    print_request_id = models.ForeignKey(PrintRequest, on_delete=models.CASCADE)
    document = models.FileField(upload_to=print_request_file_path)
    no_of_copies = models.IntegerField()

    def __str__(self):
        return self.print_request_id.client
