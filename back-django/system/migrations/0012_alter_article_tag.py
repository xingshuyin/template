# Generated by Django 4.2.6 on 2023-10-21 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_alter_user_info_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tag',
            field=models.JSONField(db_comment='标签', default=list, null=True, verbose_name='标签'),
        ),
    ]
