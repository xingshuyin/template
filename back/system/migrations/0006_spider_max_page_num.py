# Generated by Django 4.1.1 on 2023-03-19 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_remove_article_link_article_source_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spider',
            name='max_page_num',
            field=models.IntegerField(blank=True, help_text='分页页数最大值', null=True),
        ),
    ]
