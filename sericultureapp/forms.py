from django import forms
from .models import *

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'size', 'description'] 
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the farm in detail'}),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'role', 'contact_info', 'salary', 'date_joined'] 

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['silkworm_batch', 'production_date', 'quantity', 'quality_grade']
        widgets = {
            'production_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'quality_grade': forms.Select(attrs={'class': 'form-control'}),
        }        

class SilkwormBatchForm(forms.ModelForm):
    class Meta:
        model = SilkwormBatch
        fields = ['batch_name', 'breed', 'quantity', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GrowthStageForm(forms.ModelForm):
    class Meta:
        model = GrowthStage
        fields = ['silkworm_batch', 'stage', 'start_date', 'end_date', 'observations']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PestOrDiseaseForm(forms.ModelForm):
    class Meta:
        model = PestOrDisease
        fields = ['silkwormbatch', 'issue_type', 'description', 'detection_date', 'resolution', 'resolved_date']
        widgets = {
            'detection_date': forms.DateInput(attrs={'type': 'date'}),
            'resolved_date': forms.DateInput(attrs={'type': 'date'}),
        }

    