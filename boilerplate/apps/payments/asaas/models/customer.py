from dataclasses import dataclass


@dataclass
class CustomerIn:
    name: str
    cpfCnpj: str
    email: str = ''
    phone: str = ''
    mobilePhone: str = ''
    address: str = ''
    addressNumber: str = ''
    complement: str = ''
    province: str = ''
    postalCode: str = ''
    externalReference: str = ''
    observations: str = ''
    notificationDisabled: bool = False
    additionalEmails: str = ''
    foreignCustomer: bool = False
    company: str = ''
    municipalInscription: str = ''
    stateInscription: str = ''
    groupName: str = ''
