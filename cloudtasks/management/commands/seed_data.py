from django.core.management.base import BaseCommand
from cloudtasks.models import Task

class Command(BaseCommand):
    help = 'Popula o banco de dados com tarefas iniciais demonstrativas'

    def handle(self, *args, **options):
        initial_tasks = [
            {
                'title': 'Construir imagem Docker com Dockerfile multi-stage',
                'description': 'Compilar a imagem de contêiner utilizando python:3.11-slim para manter o tamanho mínimo e camadas otimizadas.',
                'category': 'docker',
                'priority': 'critical',
                'status': 'completed',
            },
            {
                'title': 'Verificar isolamento de processos e UTS namespace',
                'description': 'Validar que o Hostname gerado dentro do contêiner corresponde ao Container ID isolado e não ao computador hospedeiro.',
                'category': 'docker',
                'priority': 'high',
                'status': 'in_progress',
            },
            {
                'title': 'Desenvolver API REST com métricas de telemetria',
                'description': 'Expor endpoint /api/system-info/ retornando dados de ambiente, sistema operacional e IP interno em formato JSON.',
                'category': 'backend',
                'priority': 'high',
                'status': 'completed',
            },
            {
                'title': 'Elaborar comparativo de desempenho: Contêineres vs VMs',
                'description': 'Documentar na página de teoria o impacto do Hypervisor, tempo de boot (ms vs min) e densidade de instâncias.',
                'category': 'nuvem',
                'priority': 'medium',
                'status': 'completed',
            },
            {
                'title': 'Mapear portas e volumes com docker run e compose',
                'description': 'Executar o contêiner mapeando a porta 8000:8000 e configurar volume persistente para o banco de dados SQLite.',
                'category': 'devops',
                'priority': 'medium',
                'status': 'pending',
            },
        ]

        created_count = 0
        for task_data in initial_tasks:
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                defaults=task_data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Seed concluído com sucesso! {created_count} novas tarefas criadas.'))

