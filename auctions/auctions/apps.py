from django.apps import AppConfig

import inject

from auctions.application.ports import EmailGateway
from auctions.application.repositories import AuctionsRepository
from auctions.infrastructure.adapters import DummyEmailGateway
from auctions.infrastructure.repositories import DjangoORMAuctionsRepository


def inject_config(binder: inject.Binder) -> None:
    binder.bind(EmailGateway, DummyEmailGateway())
    binder.bind(AuctionsRepository, DjangoORMAuctionsRepository())


class AuctionsConfig(AppConfig):
    name = 'auctions'

    def ready(self) -> None:
        super().ready()
        inject.configure(inject_config)
