from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from utils.models import Active, TimeStampedModel

from accounts.managers import UserManager
from accounts.validators import validate_cpf_cnpj, validate_cpf_cnpj_format


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, Active):
    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    email = models.EmailField(
        'email',
        unique=True,
        blank=False,
        validators=[validate_email],
    )

    name = models.CharField(
        'nome',
        max_length=150,
        blank=False,
    )

    cpf_cnpj = models.CharField(
        'CPF/CNPJ',
        max_length=18,
        blank=False,
        validators=[validate_cpf_cnpj, validate_cpf_cnpj_format],
    )
    asaas_customer_id = models.CharField(
        'id do cliente no asaas',
        max_length=16,
        blank=True,
    )

    is_staff = models.BooleanField(
        'status de staff',
        default=False,
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'cpf_cnpj']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def first_name(self):
        return self.name.split(' ')[0]
