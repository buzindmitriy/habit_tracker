from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Habit


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time="08:00",
            action="Drink water",
            is_pleasant=False,
            time_to_complete=60
        )
        self.assertEqual(habit.action, "Drink water")
        self.assertEqual(Habit.objects.count(), 1)

    def test_habit_validation(self):
        habit = Habit(
            user=self.user,
            place="Home",
            time="08:00:00",
            action="Drink water",
            is_pleasant=True,
            reward="Reward",  # Приятная привычка не может иметь вознаграждение
            time_to_complete=60
        )
        with self.assertRaises(ValidationError) as context:
            habit.full_clean()

        # Проверяем структуру ошибок
        errors = context.exception.message_dict
        self.assertIn("__all__", errors)
        self.assertIn(
            "Приятная привычка не может иметь вознаграждение или связанную привычку.",
            errors["__all__"]
        )
