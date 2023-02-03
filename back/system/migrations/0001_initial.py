# Generated by Django 4.1.1 on 2023-01-14 20:39

from django.db import migrations, models
import django.db.models.deletion
import system.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('dept_belong_id', models.IntegerField(blank=True, help_text='所属部门id', null=True)),
                ('is_delete', models.BooleanField(default=False, help_text='是否逻辑删除')),
                ('name', models.CharField(help_text='名称', max_length=100, verbose_name='名称')),
                ('code', models.CharField(db_index=True, help_text='地区编码', max_length=20, unique=True, verbose_name='地区编码')),
                ('level', models.BigIntegerField(help_text='地区层级(0省份 1城市 2区县 3乡级)', verbose_name='地区层级(0省份 1城市 2区县 3乡级)')),
                ('lat', models.CharField(blank=True, max_length=10, null=True)),
                ('lng', models.CharField(blank=True, max_length=10, null=True)),
                ('pcode', models.ForeignKey(blank=True, db_constraint=False, help_text='父地区编码', null=True, on_delete=django.db.models.deletion.CASCADE, to='system.area', to_field='code', verbose_name='父地区编码')),
            ],
            options={
                'verbose_name': '地区表',
                'verbose_name_plural': '地区表',
                'db_table': 'area',
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间')),
                ('name', models.CharField(help_text='部门名称', max_length=20)),
                ('key', models.CharField(help_text='标识符', max_length=50, null=True)),
                ('sort', models.IntegerField(default=1, help_text='排序')),
                ('owner', models.CharField(blank=True, help_text='负责人', max_length=32, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='system.dept')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
                'db_table': 'Dept',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('dept_belong_id', models.IntegerField(blank=True, help_text='所属部门id', null=True)),
                ('is_delete', models.BooleanField(default=False, help_text='是否逻辑删除')),
                ('file', models.FileField(max_length=200, storage=system.models.storage(), upload_to=system.models.make_file_name)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '文件',
                'db_table': 'File',
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('dept_belong_id', models.IntegerField(blank=True, help_text='所属部门id', null=True)),
                ('is_delete', models.BooleanField(default=False, help_text='是否逻辑删除')),
                ('username', models.CharField(blank=True, help_text='登录用户名', max_length=32, null=True, verbose_name='登录用户名')),
                ('ip', models.CharField(blank=True, help_text='登录ip', max_length=32, null=True, verbose_name='登录ip')),
                ('agent', models.TextField(blank=True, help_text='agent信息', null=True, verbose_name='agent信息')),
                ('browser', models.CharField(blank=True, help_text='浏览器名', max_length=200, null=True, verbose_name='浏览器名')),
                ('os', models.CharField(blank=True, help_text='操作系统', max_length=200, null=True, verbose_name='操作系统')),
                ('continent', models.CharField(blank=True, help_text='州', max_length=50, null=True, verbose_name='州')),
                ('country', models.CharField(blank=True, help_text='国家', max_length=50, null=True, verbose_name='国家')),
                ('province', models.CharField(blank=True, help_text='省份', max_length=50, null=True, verbose_name='省份')),
                ('city', models.CharField(blank=True, help_text='城市', max_length=50, null=True, verbose_name='城市')),
                ('district', models.CharField(blank=True, help_text='县区', max_length=50, null=True, verbose_name='县区')),
                ('isp', models.CharField(blank=True, help_text='运营商', max_length=50, null=True, verbose_name='运营商')),
                ('area_code', models.CharField(blank=True, help_text='区域代码', max_length=50, null=True, verbose_name='区域代码')),
                ('country_english', models.CharField(blank=True, help_text='英文全称', max_length=50, null=True, verbose_name='英文全称')),
                ('country_code', models.CharField(blank=True, help_text='简称', max_length=50, null=True, verbose_name='简称')),
                ('longitude', models.CharField(blank=True, help_text='经度', max_length=50, null=True, verbose_name='经度')),
                ('latitude', models.CharField(blank=True, help_text='纬度', max_length=50, null=True, verbose_name='纬度')),
                ('login_type', models.IntegerField(choices=[(1, '普通登录')], default=1, help_text='登录类型', verbose_name='登录类型')),
            ],
            options={
                'verbose_name': '登录日志',
                'verbose_name_plural': '登录日志',
                'db_table': 'LoginLog',
                'ordering': ('-createAt',),
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('dept_belong_id', models.IntegerField(blank=True, help_text='所属部门id', null=True)),
                ('is_delete', models.BooleanField(default=False, help_text='是否逻辑删除')),
                ('icon', models.CharField(blank=True, help_text='菜单图标', max_length=64, null=True)),
                ('label', models.CharField(help_text='菜单名称', max_length=64)),
                ('sort', models.IntegerField(blank=True, default=1, help_text='显示排序', null=True)),
                ('is_link', models.BooleanField(default=False, help_text='是否外链')),
                ('is_catalog', models.BooleanField(default=False, help_text='是否目录')),
                ('path', models.CharField(blank=True, help_text='路由地址', max_length=128, null=True)),
                ('component', models.CharField(blank=True, help_text='组件地址', max_length=128, null=True)),
                ('name', models.CharField(blank=True, help_text='路由名称', max_length=50, null=True)),
                ('disable', models.BooleanField(blank=True, default=False, help_text='禁用状态', null=True)),
                ('cache', models.BooleanField(blank=True, default=False, help_text='是否页面缓存', null=True)),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, help_text='上级菜单', null=True, on_delete=django.db.models.deletion.PROTECT, to='system.menu')),
            ],
            options={
                'verbose_name': '菜单表',
                'verbose_name_plural': '菜单表',
                'db_table': 'Menu',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='MenuInterface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('dept_belong_id', models.IntegerField(blank=True, help_text='所属部门id', null=True)),
                ('is_delete', models.BooleanField(default=False, help_text='是否逻辑删除')),
                ('name', models.CharField(help_text='接口名称', max_length=50)),
                ('key', models.CharField(help_text='标识符', max_length=50, null=True)),
                ('method', models.IntegerField(choices=[(0, 'GET'), (1, 'POST'), (2, 'PUT'), (3, 'DELETE')], help_text='请求方式')),
                ('path', models.CharField(help_text='接口地址', max_length=100)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.menu')),
            ],
            options={
                'verbose_name': '菜单接口',
                'verbose_name_plural': '菜单接口',
                'db_table': 'MenuInterface',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('dept_belong_id', models.IntegerField(blank=True, help_text='所属部门id', null=True)),
                ('is_delete', models.BooleanField(default=False, help_text='是否逻辑删除')),
                ('name', models.CharField(max_length=50)),
                ('key', models.CharField(help_text='标识符', max_length=50, null=True)),
                ('permission', models.IntegerField(choices=[(0, '仅本人数据权限'), (1, '本部门及以下数据权限'), (2, '本部门数据权限'), (3, '全部数据权限'), (4, '自定数据权限')], default=0, help_text='数据权限范围')),
                ('is_admin', models.BooleanField(default=False, help_text='是否为管理员')),
                ('dept', models.ManyToManyField(to='system.dept')),
                ('menu', models.ManyToManyField(blank=True, to='system.menu')),
                ('menu_interface', models.ManyToManyField(blank=True, to='system.menuinterface')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
                'db_table': 'Role',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('dept_belong_id', models.IntegerField(blank=True, help_text='所属部门id', null=True)),
                ('is_delete', models.BooleanField(default=False, help_text='是否逻辑删除')),
                ('name', models.CharField(help_text='名称', max_length=100, null=True, verbose_name='名称')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='system.area', to_field='code')),
            ],
            options={
                'verbose_name': '企业信息',
                'verbose_name_plural': '企业信息',
                'db_table': 'Enterprise',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('createAt', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updateAt', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('dept_belong_id', models.IntegerField(blank=True, help_text='所属部门id', null=True)),
                ('is_delete', models.BooleanField(default=False, help_text='是否逻辑删除')),
                ('name', models.CharField(help_text='名称', max_length=100, null=True)),
                ('username', models.CharField(help_text='用户名', max_length=100, unique=True)),
                ('role', models.JSONField(default=list, help_text='用户角色')),
                ('email', models.EmailField(help_text='邮箱', max_length=254, null=True)),
                ('phone', models.CharField(help_text='电话', max_length=12, null=True)),
                ('is_super', models.BooleanField(default=False, help_text='是否为超级管理员')),
                ('dept', models.ForeignKey(help_text='所属部门', null=True, on_delete=django.db.models.deletion.PROTECT, to='system.dept')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'User',
            },
            managers=[
                ('objects', system.models.UserManager()),
            ],
        ),
    ]
