from django import forms
from django.contrib.auth import get_user_model
from .models import Course, Grade

User = get_user_model()


class AssignLecturerForm(forms.ModelForm):
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(role__in=['lecturer', 'hod']).order_by('last_name', 'first_name'),
        required=False,
        empty_label='— Unassign —',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
    )

    class Meta:
        model = Course
        fields = ['lecturer']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'code', 'name', 'description', 'credits', 'lecturer',
            'semester', 'academic_year', 'max_students', 'year_of_study', 'is_active',
        ]
        widgets = {
            'code':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MATH101'}),
            'name':          forms.TextInput(attrs={'class': 'form-control'}),
            'description':   forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'credits':       forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'lecturer':      forms.Select(attrs={'class': 'form-select'}),
            'semester':      forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024/2025'}),
            'max_students':  forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'year_of_study': forms.Select(attrs={'class': 'form-select'}),
            'is_active':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = [
            'coursework', 'assignments', 'tests', 'quizzes',
            'exams', 'practical_marks', 'participation',
            'total_score', 'score', 'remarks',
        ]
        widgets = {
            'coursework': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01'}),
            'assignments': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01'}),
            'tests': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01'}),
            'quizzes': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01'}),
            'exams': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01'}),
            'practical_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01'}),
            'participation': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01'}),
            'total_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01', 'placeholder': 'Optional auto-calculated total'}),
            'score':   forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0, 'max': 100, 'step': '0.01',
                'placeholder': 'Enter score (0 – 100)',
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional remarks…',
            }),
        }
