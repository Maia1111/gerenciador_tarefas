from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task, Category
from .forms import TaskForm, CategoryForm, CustomAuthenticationForm
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

# Create your views here.

class TaskListView(LoginRequiredMixin, ListView):
    """
    View para listar tarefas do usuário logado.
    
    Args:
        model (Task): Modelo usado
        template_name (str): Template para renderizar
        context_object_name (str): Nome do objeto no contexto
    """
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.date.today()
        
        # Adicionar estatísticas das tarefas
        tasks = context['tasks']
        context['total_tasks'] = tasks.count()
        context['completed_tasks'] = tasks.filter(completed=True).count()
        context['pending_tasks'] = tasks.filter(completed=False).count()
        context['overdue_tasks'] = tasks.filter(
            due_date__lt=datetime.date.today(), 
            completed=False
        ).count()
        

        
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar nova tarefa.
    
    Args:
        model (Task): Modelo usado
        form_class (TaskForm): Formulário associado
        template_name (str): Template para renderizar
        success_url (str): URL de redirecionamento após sucesso
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar tarefa existente.
    
    Args:
        model (Task): Modelo usado
        form_class (TaskForm): Formulário associado
        template_name (str): Template para renderizar
        success_url (str): URL de redirecionamento após sucesso
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)  # type: ignore

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para deletar tarefa.
    
    Args:
        model (Task): Modelo usado
        template_name (str): Template para confirmação
        success_url (str): URL de redirecionamento após deleção
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)  # type: ignore

class CustomLoginView(LoginView):
    """
    View customizada de login que processa o campo 'remember_me'.
    
    Args:
        form_class (CustomAuthenticationForm): Formulário customizado de autenticação
        template_name (str): Template para renderizar
    """
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        """
        Processa o formulário válido e configura a sessão baseada no 'remember_me'.
        
        Args:
            form (CustomAuthenticationForm): Formulário validado
            
        Returns:
            HttpResponse: Resposta de redirecionamento
        """
        remember_me = form.cleaned_data.get('remember_me')
        
        # Configurar duração da sessão baseada no checkbox
        if remember_me:
            # Lembrar por 2 semanas
            self.request.session.set_expiry(1209600)  # 2 semanas em segundos
        else:
            # Expirar quando o browser fechar
            self.request.session.set_expiry(0)
        
        return super().form_valid(form)

class RegisterView(CreateView):
    """
    View para registro de novos usuários.
    
    Args:
        form_class (UserCreationForm): Formulário de criação de usuário
        template_name (str): Template para renderizar
        success_url (str): URL de redirecionamento após sucesso
    """
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

# Category Views
class CategoryCreateView(LoginRequiredMixin, CreateView):
    """View para criar nova categoria."""
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('category_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryListView(LoginRequiredMixin, ListView):
    """View para listar categorias do usuário."""
    model = Category
    template_name = 'tasks/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar categoria existente.
    
    Args:
        model (Category): Modelo usado
        form_class (CategoryForm): Formulário associado
        template_name (str): Template para renderizar
        success_url (str): URL de redirecionamento após sucesso
    """
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('category_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """View para deletar categoria do usuário."""
    model = Category
    template_name = 'tasks/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

@login_required
def debug_categories(request):
    """View para debug das categorias."""
    categories = Category.objects.filter(user=request.user)
    all_categories = Category.objects.all()
    
    context = {
        'categories': categories,
        'all_categories': all_categories,
    }
    
    return render(request, 'tasks/debug_categories.html', context)

# AJAX Views
@login_required
@require_http_methods(["POST"])
def toggle_task_status(request, task_id):
    """AJAX endpoint para alternar status da tarefa."""
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        data = json.loads(request.body)
        task.completed = data.get('completed', not task.completed)
        task.save()
        
        return JsonResponse({
            'success': True,
            'completed': task.completed,
            'message': 'Status da tarefa atualizado com sucesso.'
        })
    except Task.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Tarefa não encontrada.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["POST"])
def quick_add_task(request):
    """AJAX endpoint para adicionar tarefa rapidamente."""
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        
        if not title:
            return JsonResponse({
                'success': False,
                'message': 'Título é obrigatório.'
            }, status=400)
        
        task = Task.objects.create(
            user=request.user,
            title=title,
            due_date=data.get('due_date') or None,
            priority=data.get('priority', 'medium')
        )
        
        return JsonResponse({
            'success': True,
            'task_id': task.id,
            'message': 'Tarefa criada com sucesso!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["POST"])
def update_task_position(request):
    """AJAX endpoint para atualizar posição das tarefas (drag & drop)."""
    try:
        data = json.loads(request.body)
        task_ids = data.get('task_ids', [])
        
        for index, task_id in enumerate(task_ids):
            Task.objects.filter(
                id=task_id, 
                user=request.user
            ).update(position=index)
        
        return JsonResponse({
            'success': True,
            'message': 'Posições atualizadas com sucesso.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }, status=500)
