from django.test import TestCase, Client
from django.urls import reverse
from cloudtasks.models import Task

class CloudPulseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            title="Tarefa de Teste",
            description="Testando o backend",
            category="docker",
            priority="high",
            status="pending"
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Painel de Controle em Nuvem")
        self.assertContains(response, "Tarefa de Teste")

    def test_theory_view(self):
        response = self.client.get(reverse('theory'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "O que são Contêineres?")
        self.assertContains(response, "Comparativo: Contêineres vs Máquinas Virtuais")

    def test_api_system_info(self):
        response = self.client.get(reverse('api_system_info'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('hostname', data)
        self.assertIn('python_version', data)
        self.assertIn('is_docker', data)

    def test_api_tasks(self):
        response = self.client.get(reverse('api_tasks'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(data['count'], 1)

    def test_task_create_and_delete(self):
        # Create
        post_res = self.client.post(reverse('task_create'), {
            'title': 'Nova Tarefa Criada via Teste',
            'description': 'Validando POST',
            'category': 'backend',
            'priority': 'medium',
            'status': 'pending',
        })
        self.assertEqual(post_res.status_code, 302) # Redirect to index
        self.assertTrue(Task.objects.filter(title='Nova Tarefa Criada via Teste').exists())

        # Delete
        new_task = Task.objects.get(title='Nova Tarefa Criada via Teste')
        del_res = self.client.post(reverse('task_delete', args=[new_task.id]))
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Task.objects.filter(title='Nova Tarefa Criada via Teste').exists())
