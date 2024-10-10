from django.db import models


class Items(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(max_length=255, verbose_name='Description')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.title