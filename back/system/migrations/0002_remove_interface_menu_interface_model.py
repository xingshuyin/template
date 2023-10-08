# Generated by Django 4.2.4 on 2023-10-08 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interface',
            name='menu',
        ),
        migrations.AddField(
            model_name='interface',
            name='model',
            field=models.CharField(db_comment='接口模型', default='a', max_length=100),
            preserve_default=False,
        ),
    ]