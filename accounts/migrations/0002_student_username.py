# Generated by Django 4.1 on 2023-04-23 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='username',
            field=models.CharField(default=1, max_length=70),
            preserve_default=False,
        ),
    ]
