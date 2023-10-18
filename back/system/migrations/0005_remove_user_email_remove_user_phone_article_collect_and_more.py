# Generated by Django 4.2.4 on 2023-10-18 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_remove_spider_category_remove_spider_max_page_num_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AddField(
            model_name='article',
            name='collect',
            field=models.IntegerField(db_comment='收藏数', default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='comment',
            field=models.IntegerField(db_comment='评论数', default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='is_delete',
            field=models.BooleanField(db_comment='是否删除', default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='is_hot',
            field=models.BooleanField(db_comment='是否热门', default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='is_original',
            field=models.BooleanField(db_comment='是否原创', default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='is_recommend',
            field=models.BooleanField(db_comment='是否推荐', default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='is_top',
            field=models.BooleanField(db_comment='是否置顶', default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='like',
            field=models.IntegerField(db_comment='点赞数', default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='view',
            field=models.IntegerField(db_comment='浏览数', default=0),
        ),
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='姓名', max_length=100, null=True, verbose_name='姓名')),
                ('gender', models.IntegerField(choices=[(1, '男'), (2, '女')], db_comment='性别', default=1, verbose_name='性别')),
                ('email', models.EmailField(db_comment='邮箱', max_length=254, null=True, verbose_name='邮箱')),
                ('phone', models.CharField(db_comment='电话', max_length=12, null=True, verbose_name='电话')),
                ('article_collect', models.ManyToManyField(related_name='collect_user', to='system.article', verbose_name='收藏文章')),
                ('article_like', models.ManyToManyField(related_name='like_user', to='system.article', verbose_name='点赞文章')),
                ('follow_user', models.ManyToManyField(to='system.user_info', verbose_name='关注用户')),
            ],
        ),
        migrations.CreateModel(
            name='article_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('dept_belong', models.IntegerField(blank=True, db_comment='所属部门id', null=True)),
                ('creator', models.IntegerField(blank=True, db_comment='创建人id', null=True)),
                ('content', models.CharField(help_text='评论内容', max_length=1000)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.article')),
                ('reply', models.ForeignKey(blank=True, help_text='回复对象', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reply_set', to='system.article_comment', verbose_name='回复对象')),
                ('root', models.ForeignKey(blank=True, help_text='根评论对象', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='root_set', to='system.article_comment', verbose_name='根评论对象')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '文章评论',
                'db_table': 'article_comment',
                'db_table_comment': '文章评论',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='user_info',
            field=models.OneToOneField(db_comment='用户信息', null=True, on_delete=django.db.models.deletion.CASCADE, to='system.user_info', verbose_name='用户信息'),
        ),
    ]
