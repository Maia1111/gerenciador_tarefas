from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    """
    Modelo para categorias de tarefas.
    
    Args:
        name (str): Nome da categoria
        color (str): Cor hexadecimal da categoria
        icon (str): Ícone FontAwesome da categoria
        user (User): Usuário dono da categoria
    """
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#7c3aed')  # Hex color
    icon = models.CharField(max_length=50, default='fas fa-folder')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ['name', 'user']
    
    def __str__(self):
        return self.name
    
    def get_total_tasks(self):
        """Retorna o total de tarefas na categoria."""
        return self.task_set.count()
    
    def get_completed_tasks(self):
        """Retorna o número de tarefas concluídas na categoria."""
        return self.task_set.filter(completed=True).count()
    
    def get_pending_tasks(self):
        """Retorna o número de tarefas pendentes na categoria."""
        return self.task_set.filter(completed=False).count()

class Task(models.Model):
    """
    Modelo para representar uma tarefa no sistema de gerenciamento.
    
    Args:
        user (User): Usuário dono da tarefa
        title (str): Título da tarefa
        description (str): Descrição detalhada
        due_date (date): Data de vencimento opcional
        completed (bool): Status de conclusão
        priority (str): Prioridade da tarefa
        category (Category): Categoria da tarefa
    """
    
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    position = models.PositiveIntegerField(default=0)  # Para drag & drop

    class Meta:
        ordering = ['position', '-created_at']

    def __str__(self):
        return self.title
    
    @property
    def priority_color(self):
        """Retorna a cor baseada na prioridade."""
        colors = {
            'low': '#22c55e',      # Verde
            'medium': '#f59e0b',   # Amarelo
            'high': '#f43f5e',     # Vermelho
            'urgent': '#dc2626',   # Vermelho escuro
        }
        return colors.get(self.priority, '#64748b')
