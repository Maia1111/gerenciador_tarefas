from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, Category

class DatePickerWidget(forms.DateInput):
    """
    Widget customizado para campo de data que garante formato correto.
    """
    
    def __init__(self, attrs=None):
        default_attrs = {
            'type': 'date',
            'class': 'form-control-modern date-picker'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
    
    def format_value(self, value):
        """
        Formata o valor da data para o formato esperado pelo widget HTML5.
        
        Args:
            value: Valor da data (pode ser datetime, date ou string)
            
        Returns:
            str: Data formatada como YYYY-MM-DD ou None
        """
        if value is None or value == '':
            return None
        
        # Se já está no formato correto, retornar
        if isinstance(value, str) and len(value) == 10:
            return value
        
        # Se é um objeto datetime ou date, formatar
        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d')
        
        return value

class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulário customizado de autenticação com campo 'remember_me'.
    
    Args:
        remember_me (BooleanField): Campo para lembrar usuário
    """
    remember_me = forms.BooleanField(
        label='Lembrar de mim',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'rememberMe'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizar widgets dos campos existentes
        self.fields['username'].widget.attrs.update({
            'class': 'form-control-clean',
            'placeholder': 'Digite seu nome de usuário',
            'autocomplete': 'username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control-clean',
            'placeholder': 'Digite sua senha',
            'autocomplete': 'current-password'
        })

class CategoryForm(forms.ModelForm):
    """
    Formulário para criar/atualizar categorias.
    """
    class Meta:
        model = Category
        fields = ['name', 'color', 'icon', 'description']
        widgets = {
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control-modern color-picker'
            }),
            'icon': forms.Select(choices=[
                ('fas fa-folder', 'Pasta'),
                ('fas fa-briefcase', 'Trabalho'),
                ('fas fa-home', 'Casa'),
                ('fas fa-graduation-cap', 'Estudos'),
                ('fas fa-heart', 'Pessoal'),
                ('fas fa-shopping-cart', 'Compras'),
                ('fas fa-dumbbell', 'Fitness'),
                ('fas fa-plane', 'Viagem'),
                ('fas fa-code', 'Programação'),
                ('fas fa-book', 'Leitura'),
            ]),
            'description': forms.Textarea(attrs={
                'class': 'form-control-modern',
                'rows': 3,
                'placeholder': 'Descreva o propósito desta categoria...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_name(self):
        """
        Valida se o nome da categoria não está duplicado para o usuário.
        """
        name = self.cleaned_data.get('name')
        if self.user and name:
            # Verificar duplicatas (exceto para edição)
            existing = Category.objects.filter(user=self.user, name=name)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError('Você já possui uma categoria com este nome.')
        
        return name

class TaskForm(forms.ModelForm):
    """
    Formulário para criar/atualizar tarefas, baseado no model Task.
    
    Args:
        Meta.model (Task): Modelo associado
        Meta.fields (list): Campos incluídos no form
    """
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category', 'completed']
        widgets = {
            'due_date': DatePickerWidget(),
            'priority': forms.Select(attrs={
                'class': 'form-control-modern priority-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control-modern category-select'
            }),
        } 