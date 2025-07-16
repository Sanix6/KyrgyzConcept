from django.db import models
from django.utils.translation import gettext_lazy as _



class Countries(models.Model):
    name = models.CharField(
        _('Страна'),
        max_length=200,
        help_text="Название страны (например, Kyrgyzstan)"
    )
    code_name = models.CharField(
        _('Код страны'),
        max_length=3,
        unique=True,
        help_text="Код страны в формате ISO Alpha-3 (например, 'KGZ')"
    )
    img = models.ImageField(
        _('Флаг'),
        upload_to='countries',
        help_text="Изображение флага страны"
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return f"{self.name} ({self.code_name})" if self.code_name else self.name

    def save(self, *args, **kwargs):
        self.code_name = self.code_name.upper()
        super().save(*args, **kwargs)


class Cities(models.Model):
    country = models.ForeignKey(
        Countries,
        related_name="cities",
        on_delete=models.CASCADE,
        verbose_name=_("Страна"),
        help_text="Страна, к которой относится город"
    )
    name = models.CharField(
        _('Город'),
        max_length=200,
        help_text="Название города (например, Bishkek)"
    )
    code_name = models.CharField(
        _('Код города'),
        max_length=3,
        help_text="Код города в формате IATA (например, 'FRU')"
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f"{self.name} ({self.code_name})"

    def save(self, *args, **kwargs):
        self.code_name = self.code_name.upper()
        super().save(*args, **kwargs)


class Airports(models.Model):
    city = models.ForeignKey(
        Cities,
        related_name="airports",
        on_delete=models.CASCADE,
        verbose_name='Город',
        help_text="Город, к которому относится аэропорт"
    )
    name = models.CharField(
        _('Аэропорт'),
        max_length=200,
        help_text="Название аэропорта (например, Manas International Airport)"
    )
    code_name = models.CharField(
        _('Код аэропорта'),
        max_length=3,
        help_text="Код аэропорта в формате IATA (например, 'FRU')"
    )

    class Meta:
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'

    def __str__(self):
        return f"{self.name} ({self.code_name})"

    def save(self, *args, **kwargs):
        self.code_name = self.code_name.upper()
        super().save(*args, **kwargs)

        