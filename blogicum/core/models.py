from django.db import models


class PublishedModel(models.Model):
    """Абстракстаня модель. Добавляет флаг is_published."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    """Абстрактная модель. Добавляет поле title"""

    title = models.CharField(max_length=256, verbose_name='Заголовок')

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    """Абстрактная модель. Добавляет поле created_at"""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
