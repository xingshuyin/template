# Generated by Django 4.2.4 on 2023-10-18 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_remove_article_pub_time_remove_user_user_info_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AlterField(
            model_name='article_comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.user_info'),
        ),
    ]
