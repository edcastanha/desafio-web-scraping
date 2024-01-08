from django.test import TestCase
from unittest.mock import patch, Mock
from meuapp.tarefas import get_queue, run_webScrappingTask

class TarefasTestCase(TestCase):

    @patch('meuapp.tarefas.enviar_para_fila_rabbitmq')  # Mock a função que envia para a fila
    def test_get_queue(self, mock_enviar_para_fila_rabbitmq):
        """
        Testa a função get_queue para verificar se ela chama corretamente os métodos da fila.
        """
        # Crie um mock para settings.RABBITMQ_HOST
        with patch('meuapp.tarefas.settings.RABBITMQ_HOST', 'localhost'):
            # Crie um mock para pika.BlockingConnection
            with patch('meuapp.tarefas.pika.BlockingConnection'):
                # Chame a função get_queue com um ID de instância fictício
                get_queue(123)  # Aqui, 123 é apenas um exemplo de ID

                # Verifique se a função para enviar para a fila foi chamada com o ID da instância
                mock_enviar_para_fila_rabbitmq.assert_called_once_with(123)

    def test_run_webScrappingTask(self):
        """
        Testa a função run_webScrappingTask para verificar se ela inicia a tarefa corretamente.
        """
        # Crie uma instância fictícia para testar a tarefa
        class MockTaskInstance:
            id = 1
            id_informacao_alvo = Mock()
            id_informacao_alvo.get_data.return_value = {'mock': 'data'}

        # Chame a função da tarefa
        run_webScrappingTask(MockTaskInstance())

        # Aqui, você pode adicionar mais asserções para verificar o comportamento esperado da função
        # Verifique se a função executa as operações esperadas ao iniciar a tarefa

