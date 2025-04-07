from unittest.mock import patch
from django.test import TestCase
from ..tasks import send_telegram_notification


class CeleryTaskTest(TestCase):
    @patch('habits.tasks.send_telegram_notification.apply_async')
    def test_send_telegram_notification(self, mock_apply_async):
        # Вызываем задачу
        send_telegram_notification.delay("123456789", "Test message")

        # Проверяем, что задача была вызвана с правильными аргументами
        mock_apply_async.assert_called_once_with(
            ('123456789', 'Test message'),  # Позиционные аргументы
            {}  # Ключевые аргументы
        )
