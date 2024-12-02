from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.asaas import AsaasApi
from payments.asaas.models.customer import CustomerIn

from accounts.models import User


@receiver(post_save, sender=User)
async def create_asaas_customer(
    sender: Type[User],
    instance: User,
    created: bool,
    **kwargs: dict,
):
    customer = CustomerIn(
        name=instance.name,
        cpfCnpj=instance.cpf_cnpj,
        email=instance.email,
    )
    if created:
        response = await AsaasApi.customers.create(customer)

        if response.is_success:
            instance.asaas_customer_id = response.json()['id']
            await instance.asave(update_fields=['asaas_customer_id'])
        return

    response = await AsaasApi.customers.update(
        instance.asaas_customer_id, customer
    )
