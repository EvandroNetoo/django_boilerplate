import re

from django.core.exceptions import ValidationError

CPF_LENGTH = 11
CPF_MOD_ADJUSTMENT = 10
CNPJ_LENGTH = 14
MAGIC_THRESHOLD = 2


def is_valid_cpf(cpf):
    if cpf == cpf[0] * len(cpf):
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10) % 11
        if digito == CPF_MOD_ADJUSTMENT:
            digito = 0
        if digito != int(cpf[i]):
            return False
    return True


def is_valid_cnpj(cnpj):
    if len(cnpj) < CNPJ_LENGTH:
        return False
    if cnpj == cnpj[0] * len(cnpj):
        return False

    pesos = [6, 7, 8, 9, 2, 3, 4, 5]
    for i in range(12, 14):
        soma = sum(
            int(cnpj[j]) * pesos[(j - 12) % len(pesos)] for j in range(i)
        )
        digito = soma % 11
        digito = 0 if digito < MAGIC_THRESHOLD else 11 - digito
        if digito != int(cnpj[i]):
            return False
    return True


def validate_cpf_cnpj(value: str):
    cpf_cnpj = re.sub(r'\D', '', value)

    if len(cpf_cnpj) < CPF_LENGTH:
        raise ValidationError('CPF/CNPJ inválido')

    if not is_valid_cpf(cpf_cnpj) and not is_valid_cnpj(cpf_cnpj):
        raise ValidationError('CPF/CNPJ inválido')


def validate_cpf_cnpj_format(value: str):
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', value) and not re.match(
        r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', value
    ):
        raise ValidationError('Formato do CPF/CNPJ inválido')
