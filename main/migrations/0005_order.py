# Generated by Django 4.1.3 on 2022-11-22 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_item_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.item')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'Order',
            },
        ),
    ]