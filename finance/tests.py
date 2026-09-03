from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Transaction


class FinanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='StrongPass123!')
        self.other = User.objects.create_user(username='bob', password='StrongPass123!')
        self.transaction = Transaction.objects.create(user=self.user, title='Salary', amount=Decimal('50000'), transaction_type='INCOME', category='Salary', date=date.today())

    def test_registration_and_login(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'email': 'new@example.com', 'password1': 'AnotherStrong123!', 'password2': 'AnotherStrong123!'})
        self.assertRedirects(response, reverse('dashboard'))
        self.client.logout()
        self.assertTrue(self.client.login(username='newuser', password='AnotherStrong123!'))

    def test_unauthorized_pages_redirect(self):
        self.assertRedirects(self.client.get(reverse('dashboard')), f'{reverse("login")}?next={reverse("dashboard")}')

    def test_crud_and_dashboard(self):
        self.client.login(username='alice', password='StrongPass123!')
        response = self.client.post(reverse('transaction_create'), {'title': 'Lunch', 'amount': '300', 'transaction_type': 'EXPENSE', 'category': 'Food', 'date': date.today(), 'description': ''})
        self.assertRedirects(response, reverse('transaction_list'))
        expense = Transaction.objects.get(title='Lunch')
        self.assertContains(self.client.get(reverse('dashboard')), '₹50000.00')
        self.client.post(reverse('transaction_update', args=[expense.pk]), {'title': 'Dinner', 'amount': '400', 'transaction_type': 'EXPENSE', 'category': 'Food', 'date': date.today(), 'description': ''})
        self.assertTrue(Transaction.objects.filter(title='Dinner').exists())
        self.client.post(reverse('transaction_delete', args=[expense.pk]))
        self.assertFalse(Transaction.objects.filter(pk=expense.pk).exists())

    def test_user_isolation(self):
        other_transaction = Transaction.objects.create(user=self.other, title='Private', amount=Decimal('10'), transaction_type='EXPENSE', category='Other', date=date.today())
        self.client.login(username='alice', password='StrongPass123!')
        self.assertEqual(self.client.get(reverse('transaction_detail', args=[other_transaction.pk])).status_code, 404)
        self.assertNotContains(self.client.get(reverse('transaction_list')), 'Private')

    def test_api_is_authenticated_and_isolated(self):
        self.assertEqual(self.client.get('/api/transactions/').status_code, 403)
        self.client.login(username='alice', password='StrongPass123!')
        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_income'], 50000.0)
        response = self.client.post('/api/transactions/', {'title': 'Contract', 'amount': '1000', 'transaction_type': 'INCOME', 'category': 'Freelance', 'date': str(date.today())}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], 'Contract')
