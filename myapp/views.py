from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import SecurityEvent
from .forms import SecurityEventForm


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
