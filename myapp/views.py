from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import SecurityEvent
from .forms import SecurityEventForm
import json
import pandas as pd
from django.core.management import call_command
from django.contrib.admin.views.decorators import staff_member_required



def home(request):
    """Homepage with dataset description and navigation links."""
    return render(request, 'myapp/home.html')


def record_list(request):
    """List all SecurityEvent records with pagination (20 per page)."""
    events = SecurityEvent.objects.all()
    paginator = Paginator(events, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/list.html', {'page_obj': page_obj})


def record_detail(request, pk):
    """Display a single SecurityEvent record."""
    event = get_object_or_404(SecurityEvent, pk=pk)
    return render(request, 'myapp/detail.html', {'object': event})


def record_create(request):
    """Create a new SecurityEvent record."""
    if request.method == 'POST':
        form = SecurityEventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Security event created successfully.')
            return redirect('record_list')
    else:
        form = SecurityEventForm()
    return render(request, 'myapp/form.html', {'form': form})


def record_update(request, pk):
    """Update an existing SecurityEvent record."""
    event = get_object_or_404(SecurityEvent, pk=pk)
    if request.method == 'POST':
        form = SecurityEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Security event updated successfully.')
            return redirect('record_detail', pk=pk)
    else:
        form = SecurityEventForm(instance=event)
    return render(request, 'myapp/form.html', {'form': form, 'object': event})


def record_delete(request, pk):
    """Delete a SecurityEvent record with confirmation."""
    event = get_object_or_404(SecurityEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Security event deleted successfully.')
        return redirect('record_list')
    return render(request, 'myapp/confirm_delete.html', {'object': event})


def analytics(request):
    """Display analytics dashboard with charts for attack categories, daily trends, and actions taken."""
    qs = SecurityEvent.objects.values(
        'category__name', 'timestamp', 'action_taken', 'threat_score', 'packet_length'
    )
    df = pd.DataFrame(qs)

    if df.empty:
        return render(request, 'myapp/analytics.html', {
            'attack_chart_json': json.dumps({'labels': [], 'values': []}),
            'trend_chart_json': json.dumps({'labels': [], 'values': []}),
            'action_chart_json': json.dumps({'labels': [], 'values': []}),
            'summary': {},
        })

    attack_counts = df.groupby('category__name').size()
    daily_counts = df.groupby(df['timestamp'].dt.date).size()
    action_counts = df.groupby('action_taken').size()

    attack_chart = {
        'labels': attack_counts.index.tolist(),
        'values': attack_counts.values.tolist(),
    }

    trend_chart = {
        'labels': [str(d) for d in daily_counts.index.tolist()],
        'values': daily_counts.values.tolist(),
    }

    action_chart = {
        'labels': action_counts.index.tolist(),
        'values': action_counts.values.tolist(),
    }

    stats_table = df[['threat_score', 'packet_length']].agg(['count', 'mean', 'min', 'max']).round(2).to_dict()

    return render(request, 'myapp/analytics.html', {
        'attack_chart_json': json.dumps(attack_chart),
        'trend_chart_json': json.dumps(trend_chart),
        'action_chart_json': json.dumps(action_chart),
        'summary': stats_table,
    })


@staff_member_required
def fetch_view(request):
    """Trigger the fetch_data management command to import new weather data (staff only)."""
    if request.method == 'POST':
        call_command('fetch_data')
        messages.success(request, 'Weather data fetched successfully.')
        return redirect('record_list')
    return render(request, 'myapp/fetch_done.html')
