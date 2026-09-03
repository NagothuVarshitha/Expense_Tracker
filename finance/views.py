from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegistrationForm, TransactionForm
from .models import Transaction
from .serializers import TransactionSerializer


def totals(queryset):
    income = queryset.filter(transaction_type=Transaction.INCOME).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    expenses = queryset.filter(transaction_type=Transaction.EXPENSE).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    return income, expenses


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    income, expenses = totals(transactions)
    category_rows = list(transactions.filter(transaction_type=Transaction.EXPENSE).values('category').annotate(total=Sum('amount')).order_by('-total'))
    return render(request, 'dashboard.html', {
        'income': income, 'expenses': expenses, 'balance': income - expenses,
        'recent_transactions': transactions[:6], 'category_rows': category_rows,
        'category_labels': [row['category'] for row in category_rows],
        'category_values': [float(row['total']) for row in category_rows],
    })


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    query = request.GET.get('q', '').strip()
    transaction_type = request.GET.get('type', '')
    category = request.GET.get('category', '')
    date = request.GET.get('date', '')
    if query:
        transactions = transactions.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if transaction_type in {Transaction.INCOME, Transaction.EXPENSE}:
        transactions = transactions.filter(transaction_type=transaction_type)
    if category:
        transactions = transactions.filter(category=category)
    if date:
        transactions = transactions.filter(date=date)
    return render(request, 'transaction_list.html', {'transactions': transactions, 'categories': Transaction.CATEGORY_CHOICES, 'filters': request.GET})


@login_required
def transaction_create(request):
    form = TransactionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        messages.success(request, 'Transaction added successfully.')
        return redirect('transaction_list')
    return render(request, 'transaction_form.html', {'form': form, 'heading': 'Add transaction'})


@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    return render(request, 'transaction_detail.html', {'transaction': transaction})


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TransactionForm(request.POST or None, instance=transaction)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Transaction updated successfully.')
        return redirect('transaction_list')
    return render(request, 'transaction_form.html', {'form': form, 'heading': 'Edit transaction'})


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect('transaction_list')
    return render(request, 'confirm_delete.html', {'transaction': transaction})


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DashboardSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        income, expenses = totals(Transaction.objects.filter(user=request.user))
        return Response({'total_income': income, 'total_expenses': expenses, 'balance': income - expenses, 'savings': income - expenses})
