from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            default=1000,
            type=int,
        )

    def handle(self, *args, **options):
        total = options.get("total")
        seeder = Seed.seeder()

        seeder.add_entity(
            User,
            total,
            {
                "email": lambda x: seeder.faker.email(),
                "nickname": lambda x: Faker().name(),
            },
        )
        seeder.execute()
