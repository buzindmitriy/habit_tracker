from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Habit


class HabitViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_habit_with_time(self):
        data = {
            "place": "Home",
            "time": "08:00:00",  # Формат времени должен быть HH:MM:SS
            "action": "Drink water",
            "is_pleasant": False,
            "periodicity": 1,  # Обязательное поле
            "time_to_complete": 60  # Не более 120 секунд
        }
        response = self.client.post('/api/habits/', data, format='json')
        print(response.data)  # Отладочная информация
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)

        # Проверяем, что время сохранено корректно
        habit = Habit.objects.first()
        self.assertEqual(str(habit.time), "08:00:00")

    def test_list_habits(self):
        # Очищаем базу данных перед тестом
        Habit.objects.all().delete()

        # Создаем одну привычку для текущего пользователя
        Habit.objects.create(
            user=self.user,
            place="Home",
            time="08:00:00",
            action="Drink water",
            is_pleasant=False,
            periodicity=1,
            time_to_complete=60
        )

        # Выполняем GET-запрос
        response = self.client.get('/api/habits/')
        print(response.data)  # Отладочная информация

        # Проверяем статус код и количество привычек
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if hasattr(response.data, 'results'):  # Если используется пагинация
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 4)

    def tearDown(self):
        # Удаляем все объекты после каждого теста
        Habit.objects.all().delete()
