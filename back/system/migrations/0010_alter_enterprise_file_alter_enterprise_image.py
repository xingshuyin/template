# Generated by Django 4.1.1 on 2023-01-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_enterprise_image2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='file',
            field=models.JSONField(default=list, help_text='文件'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='image',
            field=models.JSONField(default=list, help_text='图片'),
        ),
    ]
