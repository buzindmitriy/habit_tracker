from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='related_habits'
    )
    periodicity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    reward = models.CharField(max_length=255, null=True, blank=True)
    time_to_complete = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)]
    )
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя одновременно выбирать связанную привычку и вознаграждение.")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")
        if self.periodicity > 7:
            raise ValidationError("Периодичность не может быть реже 1 раза в 7 дней.")
