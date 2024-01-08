from django.test import TestCase
from myapp.models import InformacaoAlvo, Tarefas
from django.utils import timezone
from unittest.mock import patch

class InformacaoAlvoTestCase(TestCase):
    def setUp(self):
        self.info_alvo = InformacaoAlvo.objects.create(
            token='abc123',
            url_alvo='https://example.com',
            codigo_acesso='123456',
            status='Aguardando',
            url_arquivo='https://example.com/file.txt'
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.info_alvo),
            "Código: 123456, URL: https://example.com"
        )

    def test_get_data_method(self):
        data = self.info_alvo.get_data()
        self.assertEqual(data['id'], self.info_alvo.id)
        self.assertEqual(data['token'], 'abc123')
        self.assertEqual(data['url_alvo'], 'https://example.com')
        self.assertEqual(data['codigo_acesso'], '123456')
        self.assertEqual(data['status'], 'Aguardando')
        self.assertEqual(data['path_arquivo'], 'https://example.com/file.txt')
        self.assertEqual(
            data['data_atualizado'],
            self.info_alvo.data_atualizacao.strftime("%d/%m/%Y %H:%M:%S")
        )

class TarefasTestCase(TestCase):
    def setUp(self):
        self.info_alvo = InformacaoAlvo.objects.create(
            token='def456',
            url_alvo='https://example.org',
            codigo_acesso='789012',
            status='Processando',
            url_arquivo='https://example.org/file.txt'
        )
        self.tarefa = Tarefas.objects.create(
            id_informacao_alvo=self.info_alvo,
            tarefa='Test Task',
            status=False,
            data_inicio=timezone.now(),
            data_fim=None
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.tarefa),
            "Tarefa: Test Task, Status: False"
        )

    def test_tarefa_created_with_correct_info_alvo(self):
        self.assertEqual(self.tarefa.id_informacao_alvo, self.info_alvo)
        self.assertEqual(self.tarefa.tarefa, 'Test Task')
        self.assertFalse(self.tarefa.status)
        self.assertIsNotNone(self.tarefa.data_inicio)
        self.assertIsNone(self.tarefa.data_fim)

    @patch('myapp.models.run_webScrappingTask.delay')
    def test_signal_is_called_on_info_alvo_creation(self, mock_run_webScrappingTask):
        self.assertEqual(mock_run_webScrappingTask.call_count, 1)
        self.assertEqual(
            mock_run_webScrappingTask.call_args.kwargs['task_data']['id'],
            self.info_alvo.id
        )
        self.assertEqual(
            mock_run_webScrappingTask.call_args.kwargs['task_data']['url'],
            'https://example.org'
        )
        self.assertEqual(
            mock_run_webScrappingTask.call_args.kwargs['task_data']['codigo'],
            '789012'
        )
