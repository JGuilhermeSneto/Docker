from django.db import models

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('docker', '🐳 Docker & Contêineres'),
        ('nuvem', '☁️ Infraestrutura & Nuvem'),
        ('backend', '⚙️ Backend & API'),
        ('frontend', '🎨 Frontend & UI'),
        ('devops', '🚀 CI/CD & Deploy'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
    ]

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True)
    category = models.CharField('Categoria', max_length=30, choices=CATEGORY_CHOICES, default='docker')
    priority = models.CharField('Prioridade', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
