import uuid

from django.db import models


class UuidModel(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False,
    )
    updated_at = models.DateTimeField(
        'atualizado em',
        auto_now_add=False,
        auto_now=True,
    )

    class Meta:
        abstract = True


class Active(models.Model):
    active = models.BooleanField('ativo', default=True)
    exist_deleted = models.BooleanField(
        'existe/deletado',
        default=True,
        help_text='Se for True o item existe. Se for False o item foi deletado.',
    )

    class Meta:
        abstract = True
