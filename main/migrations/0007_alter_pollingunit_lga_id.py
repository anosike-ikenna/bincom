# Generated by Django 3.2.5 on 2021-08-19 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_ward_lga_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollingunit',
            name='lga_id',
            field=models.IntegerField(),
        ),
    ]
