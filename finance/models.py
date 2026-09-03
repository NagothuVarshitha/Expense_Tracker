from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Transaction(models.Model):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'
    TYPE_CHOICES = [(INCOME, 'Income'), (EXPENSE, 'Expense')]
    CATEGORY_CHOICES = [
        ('Food', 'Food'), ('Travel', 'Travel'), ('Shopping', 'Shopping'),
        ('Bills', 'Bills'), ('Entertainment', 'Entertainment'), ('Education', 'Education'),
        ('Health', 'Health'), ('Salary', 'Salary'), ('Freelance', 'Freelance'), ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    transaction_type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Other')
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [models.Index(fields=['user', '-date']), models.Index(fields=['user', 'transaction_type'])]

    def __str__(self):
        return f'{self.title} ({self.transaction_type})'
