# Generated by Django 4.1.1 on 2023-01-17 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_remove_enterprise_image2'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ype',
            field=models.IntegerField(choices=[(1, '前端'), (2, '后端')], default=1, help_text='用户类型'),
        ),
        migrations.AlterField(
            model_name='user',
            name='openid',
            field=models.CharField(help_text='微信openid', max_length=100, null=True, unique=True),
        ),
    ]
