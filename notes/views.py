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
    """Display notes for a specific year"""
    # Get all subjects for this year that aren't quantum
    subjects = Subject.objects.filter(year=year, is_quantum=False)
    
    # Get all notes for these subjects
    notes = Note.objects.filter(
        chapter__subject__year=year,
        chapter__subject__is_quantum=False
    ).order_by('-upload_date')  # Changed from uploaded_at to upload_date
    
    return render(request, 'year_notes.html', {
        'year': year,
        'subjects': subjects,
        'notes': notes,
        'is_staff': request.user.is_staff  # Pass this to template to control delete button visibility
    })

def quantum(request):
    """Display quantum notes organized by year"""
    # Get all quantum notes and organize them by year
    quantum_subjects = Subject.objects.filter(is_quantum=True)
    
    year_notes = {}
    for year in range(1, 5):  # Years 1-4
        notes_data = []
        subjects = quantum_subjects.filter(year=year)
        
        for subject in subjects:
            for chapter in subject.chapter_set.all():
                for note in chapter.note_set.all():
                    notes_data.append({
                        'note': note,
                        'chapter': chapter,
                        'subject': subject
                    })
        
        if notes_data:  # Only add years that have notes
            year_notes[year] = {
                'year_name': f'{year}{"st" if year == 1 else "nd" if year == 2 else "rd" if year == 3 else "th"} Year',
                'notes': notes_data
            }
    
    return render(request, 'quantum.html', {
        'year_notes': year_notes,
        'is_staff': request.user.is_staff  # Pass this to template to control delete button visibility
    })

def staff_required(view_func):
    """Decorator to restrict access to staff only"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Only administrators can perform this action!')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@staff_required  # Only allow staff to access this view
def add_note(request):
    """Add a new note (staff only)"""
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            subject, created = Subject.objects.get_or_create(
                name=request.POST.get('subject'),
                year=request.POST.get('year'),
                is_quantum=request.POST.get('is_quantum') == 'true'
            )
            
            if 'subject_image' in request.FILES:
                subject.image = request.FILES['subject_image']
                subject.save()
            
            chapter, created = subject.chapter_set.get_or_create(
                name=request.POST.get('chapter')
            )
            
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