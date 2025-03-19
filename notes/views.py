from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib import messages
from .models import Note, Subject  # Add Subject to imports if not already there
from django.core.exceptions import PermissionDenied

def home(request):
    """Home page view with recent notes"""
    recent_notes = Note.objects.all().order_by('-upload_date')[:5]  # Changed from uploaded_at to upload_date
    return render(request, 'home.html', {
        'recent_notes': recent_notes
    })

def year_notes(request, year):
    """Display notes for a specific year (excluding quantum)"""
    subjects = Subject.objects.filter(year=year, is_quantum=False)  # Added is_quantum=False
    context = {
        'year': f'{year}{"st" if year == 1 else "nd" if year == 2 else "rd" if year == 3 else "th"} Year',
        'subjects': []
    }
    
    for subject in subjects:
        subject_notes = Note.objects.filter(chapter__subject=subject).order_by('-upload_date')
        context['subjects'].append({
            'subject': subject,
            'notes': subject_notes
        })
    
    return render(request, 'year_view.html', context)

def quantum(request):
    """Display quantum notes"""
    subjects = Subject.objects.filter(is_quantum=True)
    context = {
        'year': 'Quantum',
        'subjects': []
    }
    
    for subject in subjects:
        subject_notes = Note.objects.filter(chapter__subject=subject).order_by('-upload_date')
        context['subjects'].append({
            'subject': subject,
            'notes': subject_notes
        })
    
    return render(request, 'quantum.html', context)  # Changed to quantum.html

def staff_required(view_func):
    """Decorator to restrict access to staff only"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Only administrators can perform this action!')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@staff_required
def add_note(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        chapter_image = request.FILES.get('chapter_image')  # Get chapter image
        
        if uploaded_file:
            subject, created = Subject.objects.get_or_create(
                name=request.POST.get('subject'),
                year=request.POST.get('year'),
                is_quantum=request.POST.get('is_quantum') == 'true'
            )
            
            # Create chapter with image
            chapter, created = subject.chapter_set.get_or_create(
                name=request.POST.get('chapter')
            )
            
            if chapter_image:
                chapter.image = chapter_image
                chapter.save()
            
            note = Note(
                title=request.POST.get('title'),
                file=uploaded_file,
                uploaded_by=request.user,
                chapter=chapter
            )
            note.save()
            
            messages.success(request, 'Note uploaded successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please select a file to upload!')
    
    return render(request, 'add_note.html')

@login_required
@staff_required  # Only allow staff to access this view
def delete_note(request, note_id):
    """Delete a note (staff only)"""
    note = get_object_or_404(Note, id=note_id)
    is_quantum = note.chapter.subject.is_quantum
    year = note.chapter.subject.year
    
    # Delete the note
    note.file.delete()  # Delete the actual file
    note.delete()       # Delete the database entry
    
    messages.success(request, 'Note deleted successfully!')
    
    # Redirect based on note type
    if is_quantum:
        return redirect('quantum')
    return redirect('year_notes', year=year)

def signup(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signup
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {
        'form': form
    })

def first_year(request):
    subjects = Subject.objects.filter(year=1)
    context = {
        'year': '1st Year',
        'subjects': []
    }
    
    for subject in subjects:
        subject_notes = Note.objects.filter(chapter__subject=subject).order_by('-upload_date')
        context['subjects'].append({
            'subject': subject,
            'notes': subject_notes
        })
    
    return render(request, 'year_view.html', context)

def second_year(request):
    subjects = Subject.objects.filter(year=2)
    context = {
        'year': '2nd Year',
        'subjects': []
    }
    
    for subject in subjects:
        subject_notes = Note.objects.filter(chapter__subject=subject).order_by('-upload_date')
        context['subjects'].append({
            'subject': subject,
            'notes': subject_notes
        })
    
    return render(request, 'year_view.html', context)

def third_year(request):
    subjects = Subject.objects.filter(year=3)
    context = {
        'year': '3rd Year',
        'subjects': []
    }
    
    for subject in subjects:
        subject_notes = Note.objects.filter(chapter__subject=subject).order_by('-upload_date')
        context['subjects'].append({
            'subject': subject,
            'notes': subject_notes
        })
    
    return render(request, 'year_view.html', context)

def fourth_year(request):
    subjects = Subject.objects.filter(year=4)
    context = {
        'year': '4th Year',
        'subjects': []
    }
    
    for subject in subjects:
        subject_notes = Note.objects.filter(chapter__subject=subject).order_by('-upload_date')
        context['subjects'].append({
            'subject': subject,
            'notes': subject_notes
        })
    
    return render(request, 'year_view.html', context)

def subject_notes(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    notes = Note.objects.filter(chapter__subject=subject).order_by('-upload_date')
    return render(request, 'subject_notes.html', {
        'subject': subject,
        'notes': notes
    })