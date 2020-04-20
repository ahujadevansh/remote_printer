import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import  PrintRequestFile

@receiver(post_delete, sender=PrintRequestFile)
def print_request_auto_delete_file_on_delete(sender, instance, **kwargs):
    # pylint: disable=unused-argument
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)

@receiver(pre_save, sender=PrintRequestFile)
def print_request_auto_delete_file_on_change(sender, instance, **kwargs):
    # pylint: disable=unused-argument
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).document
    except sender.DoesNotExist:
        return False

    new_file = instance.document
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
