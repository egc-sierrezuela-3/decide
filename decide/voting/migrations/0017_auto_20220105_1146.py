# Generated by Django 2.0 on 2022-01-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0016_auto_20220105_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(0, 'IDENTITY'), (2, 'BORDA'), (3, 'SAINTE_LAGUE'), (1, 'DHONT'), (4, 'EQUALITY')], default=1),
        ),
    ]
