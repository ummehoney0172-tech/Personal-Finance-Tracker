import json
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExpenseForm
from .models import Expense


@login_required
def expense_list(request):
    qs = Expense.objects.filter(user=request.user)
    category = request.GET.get('category', '').strip()
    if category:
        qs = qs.filter(category=category)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'expenses/expense_list.html', {
        'page_obj': page_obj,
        'categories': Expense.CATEGORY_CHOICES,
        'selected_category': category,
    })


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added.')
            return redirect('expense_list')
    else:
        form = ExpenseForm(initial={'date': date.today()})
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Add Expense'})


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated.')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Edit Expense'})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted.')
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


@login_required
def dashboard(request):
    today = date.today()
    month_start = today.replace(day=1)
    qs = Expense.objects.filter(user=request.user)

    total = qs.aggregate(s=Sum('amount'))['s'] or Decimal('0')
    month_total = qs.filter(date__gte=month_start).aggregate(s=Sum('amount'))['s'] or Decimal('0')
    days_in_month = (today - month_start).days + 1
    daily_avg = (month_total / days_in_month) if days_in_month else Decimal('0')

    by_category = (
        qs.values('category')
          .annotate(total=Sum('amount'))
          .order_by('-total')
    )
    category_labels = [row['category'] for row in by_category]
    category_data = [float(row['total']) for row in by_category]

    last_7_start = today - timedelta(days=6)
    daily_qs = (
        qs.filter(date__gte=last_7_start)
          .values('date')
          .annotate(total=Sum('amount'))
    )
    daily_map = defaultdict(float)
    for row in daily_qs:
        daily_map[row['date']] = float(row['total'])
    daily_labels = [(last_7_start + timedelta(days=i)).strftime('%b %d') for i in range(7)]
    daily_data = [daily_map[last_7_start + timedelta(days=i)] for i in range(7)]

    return render(request, 'expenses/dashboard.html', {
        'total': total,
        'month_total': month_total,
        'daily_avg': daily_avg.quantize(Decimal('0.01')),
        'category_labels_json': json.dumps(category_labels),
        'category_data_json': json.dumps(category_data),
        'daily_labels_json': json.dumps(daily_labels),
        'daily_data_json': json.dumps(daily_data),
        'recent': qs[:5],
    })
