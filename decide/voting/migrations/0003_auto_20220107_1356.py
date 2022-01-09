# Generated by Django 2.0 on 2022-01-07 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_auto_20220107_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='points',
            field=models.PositiveIntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(1, 'DHONT'), (0, 'IDENTITY'), (4, 'EQUALITY'), (3, 'SAINTE_LAGUE'), (2, 'BORDA')], default=1),
        ),
    ]
