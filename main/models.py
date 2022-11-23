from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'элемент'
        verbose_name_plural = 'Объекты'


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    def amount(self):
        return self.item.price * self.quantity

    def increase(self):
        self.quantity += 1
        self.save()

    def decrease(self):
        if self.quantity == 1:
            self.delete()
        else:
            self.quantity -= 1
            self.save()

    def __str__(self):
        return f'{self.item}: {self.quantity}'

    @classmethod
    def clean_order(cls):
        cls.objects.all().delete()

    @classmethod
    def total_amount(cls):
        return sum([elem.amount() for elem in cls.objects.all()])
