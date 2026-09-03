from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from finance.models import Transaction


class Command(BaseCommand):
    help = 'Create a demo user and realistic sample transactions.'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        if created:
            user.set_password('DemoPass123!')
            user.save()
        Transaction.objects.filter(user=user).delete()
        today = timezone.localdate()
        entries = [
            ('Salary', Decimal('50000'), 'INCOME', 'Salary'), ('Freelance', Decimal('8000'), 'INCOME', 'Freelance'),
            ('Food', Decimal('3000'), 'EXPENSE', 'Food'), ('Rent', Decimal('10000'), 'EXPENSE', 'Bills'),
            ('Travel', Decimal('2500'), 'EXPENSE', 'Travel'), ('Shopping', Decimal('4000'), 'EXPENSE', 'Shopping'),
        ]
        Transaction.objects.bulk_create([Transaction(user=user, title=title, amount=amount, transaction_type=kind, category=category, date=today - timedelta(days=index * 3)) for index, (title, amount, kind, category) in enumerate(entries)])
        self.stdout.write(self.style.SUCCESS('Demo user ready: username=demo password=DemoPass123!'))
