from django.db import models

class MetaDataModel(models.Model):

    """
    An abstract base class model that provides self updating ``created_at`` and ``updated_at`` fields
    and a soft delete fields ``is_deleted``
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
