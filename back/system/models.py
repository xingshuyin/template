from email.policy import default
import hashlib
import os
from random import choices
from secrets import choice
from typing import Any, Dict, Tuple
import uuid
from attr import fields
from django.apps import apps
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField, ForeignKey
from itertools import chain
from django.forms import ModelForm
import datetime
import time
from django.core.files.storage import FileSystemStorage
from root.settings import BASE_DIR
from django.utils._os import safe_join
from django.utils.encoding import filepath_to_uri
from urllib.parse import urljoin


class base_model(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)
    update_time = models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)
    dept_belong = models.IntegerField(db_comment='所属部门id', null=True, blank=True)
    creator = models.IntegerField(db_comment='创建人id', null=True, blank=True)
    public_model = False  # 是否公开, 公开数据list查询不受部门限制, 但受角色的接口

    class Meta:
        abstract = True
        ordering = ('-create_time', )

    def model_to_dict(self, fields=None, exclude=None, deep=2):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, "editable", False):
            #     continue
            # if fields is not None and f.name not in fields:
            #     continue
            # if exclude and f.name in exclude:
            #     continue
            v = f.value_from_object(self)
            if isinstance(f, ManyToManyField):  # 外键序列化,使用它必须继承本模型
                if deep > 0:
                    v = [i.model_to_dict(deep=deep - 1) for i in v] if v else []
                else:
                    v = [i.id for i in v] if v else []
            elif isinstance(f, ForeignKey):  # 外键序列化,使用它必须继承本模型
                if deep > 0:
                    v = f.related_model.objects.get(pk=v).model_to_dict(deep=deep - 1) if v else None
                else:
                    pass
            if isinstance(f, DateTimeField):
                v = v.strftime('%Y-%m-%d %H:%M:%S') if v else None
            data[f.name] = v

        return data


def make_file_name(instance, filename):
    today = datetime.date.today()
    return f"upload/{today.year}/{today.month}/{today.day}/{str(time.time())+'_'+filename}"


class storage(FileSystemStorage):

    def __init__(self):
        super().__init__()
        # self._location = os.path.join(BASE_DIR, "media")  # 自定义文件的路径或者使用settings中的MEDIA_ROOT
        # self._base_url = '/media/'

    def _save(self, name, content):
        name = super()._save(name, content)
        print('_save', self.base_url.lstrip('/'), name)
        return self.base_url.lstrip('/') + name  # TODO:文件上传- 保存文件的路径拼接上base_url

    def path(self, name):  # 构造文件的路径 删除拼接上的base_url
        print('path', safe_join(self.location, name.lstrip(self.base_url.lstrip('/'))))
        return safe_join(self.location, name.lstrip(self.base_url.lstrip('/')))

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip("/")
        print(url)
        return url

    def delete(self, name):
        if not name:
            raise ValueError("The name must be given to delete().")
        name = self.path(name)
        # If the file or directory exists, delete it from the filesystem.
        try:
            if os.path.isdir(name):
                os.rmdir(name)
            else:
                os.remove(name)
        except FileNotFoundError:
            # FileNotFoundError is raised if the file or directory was removed
            # concurrently.
            pass


fs = storage()


# TODO:文件上传-模型/表单
class file(base_model):
    file = models.FileField(upload_to=make_file_name, max_length=200, storage=fs)
    name = models.CharField(max_length=100)

    def delete(self, using: Any = ..., keep_parents: bool = ...) -> Tuple[int, Dict[str, int]]:
        print('file delete', self.file)
        self.file.delete()
        return super().delete()

    class Meta:
        db_table = "file"
        verbose_name = "文件"
        db_table_comment = verbose_name


class FileForm(ModelForm):

    class Meta:
        model = file
        fields = '__all__'


class dept(base_model):
    name = models.CharField(max_length=20, db_comment='部门名称')
    key = models.CharField(max_length=50, db_comment="标识符", null=True)
    parent = models.ForeignKey(to='self', on_delete=models.PROTECT, null=True, blank=True)
    sort = models.IntegerField(default=1, db_comment="排序")
    owner = models.CharField(max_length=32, null=True, blank=True, db_comment="负责人")

    class Meta:
        db_table = "dept"
        verbose_name = "部门"
        db_table_comment = verbose_name
        ordering = ("sort", )


class menu(base_model):
    parent = models.ForeignKey(
        to="menu",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_constraint=False,
        db_comment="上级菜单",
    )
    icon = models.CharField(max_length=64, null=True, blank=True, db_comment="菜单图标")
    label = models.CharField(max_length=64, db_comment="菜单名称")
    sort = models.IntegerField(default=1, null=True, blank=True, db_comment="显示排序")
    ISLINK_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    is_link = models.BooleanField(default=False, db_comment="是否外链")
    is_catalog = models.BooleanField(default=False, db_comment="是否目录")
    path = models.CharField(max_length=128, null=True, blank=True, db_comment="路由地址")
    component = models.CharField(max_length=128, null=True, blank=True, db_comment="组件地址")
    name = models.CharField(max_length=50, null=True, blank=True, db_comment="路由名称")
    disable = models.BooleanField(default=False, null=True, blank=True, db_comment="禁用状态")
    cache = models.BooleanField(default=False, null=True, blank=True, db_comment="是否页面缓存")

    class Meta:
        db_table = "menu"
        verbose_name = "菜单"
        db_table_comment = verbose_name
        ordering = ("sort", )


class interface(base_model):
    name = models.CharField(max_length=50, db_comment='接口名称')
    key = models.CharField(max_length=50, db_comment="标识符", null=True)
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(choices=METHOD_CHOICES, db_comment='请求方式')
    path = models.CharField(max_length=100, db_comment="接口地址")
    model = models.CharField(max_length=100, db_comment="接口模型")
    model_name = models.CharField(max_length=100, db_comment="接口模型名称")

    class Meta:
        db_table = "interface"
        verbose_name = "接口"
        db_table_comment = verbose_name


class role(base_model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50, db_comment="标识符", null=True)
    PERMISSION_CHOICES = (
        (0, "仅本人数据权限"),
        (1, "本部门及以下数据权限"),
        (2, "本部门数据权限"),
        (3, "全部数据权限"),
        (4, "自定数据权限"),
    )
    permission = models.IntegerField(choices=PERMISSION_CHOICES, db_comment="数据权限范围", default=0)
    menu = models.ManyToManyField(menu, blank=True)
    interface = models.ManyToManyField(interface, blank=True)
    is_admin = models.BooleanField(default=False, db_comment='是否为管理员')

    class Meta:
        db_table = "role"
        verbose_name = "角色"
        db_table_comment = verbose_name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)


class user(AbstractBaseUser, base_model):
    openid = models.CharField(max_length=100, db_comment='微信openid', verbose_name='微信openid', unique=True, null=True)
    username = models.CharField(max_length=100, db_comment='账号', verbose_name='账号', unique=True)
    role = models.JSONField(default=list, db_comment='角色', verbose_name='角色')
    type = models.IntegerField(choices=((1, '前端'), (2, '后端')), default=1, db_comment='类型', verbose_name='类型')
    dept = models.ForeignKey(dept, on_delete=models.PROTECT, null=True, db_comment="部门", verbose_name='部门')
    USERNAME_FIELD = 'username'
    objects = UserManager()
    is_super = models.BooleanField(default=False, db_comment='是否为超级管理员', verbose_name='是否为超级管理员')

    def set_password(self, raw_password):  # TODO:model-用户表-设置密码方式
        # encode(encoding="UTF-8")  之后 通过索引获取的值为unciode编码值
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        db_table_comment = verbose_name
        
class user_info(base_model):
    icon = models.CharField(max_length=100, db_comment='头像', verbose_name='头像', null=True)
    birthday = models.DateField(db_comment='生日', verbose_name='生日', null=True)
    signature = models.CharField(max_length=100, db_comment='个性签名', verbose_name='个性签名', null=True)
    user = models.OneToOneField(user, on_delete=models.CASCADE, null=True, db_comment="用户", verbose_name='用户')
    name = models.CharField(max_length=100, db_comment='姓名', verbose_name='姓名', null=True)
    gender = models.IntegerField(choices=((1, '男'), (2, '女'), (0, '未知')), default=0, db_comment='性别', verbose_name='性别', null=True)
    email = models.EmailField(db_comment="邮箱", verbose_name='邮箱', null=True)
    phone = models.CharField(max_length=12, db_comment="电话", verbose_name='电话', null=True)
    follow_user = models.ManyToManyField('self', symmetrical=False, verbose_name='关注用户')
    article_like = models.ManyToManyField('article', related_name='like_user', verbose_name='点赞文章')
    article_collect = models.ManyToManyField('article', related_name='collect_user', verbose_name='收藏文章')
    class Meta:
        db_table = "user_info"
        verbose_name = "用户信息"
        db_table_comment = verbose_name
class area(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称", db_comment="名称")
    code = models.CharField(max_length=20, verbose_name="地区编码", db_comment="地区编码", unique=True, db_index=True)
    level = models.BigIntegerField(verbose_name="地区等级", db_comment="地区等级(0省份 1城市 2区县 3乡级)")
    lat = models.CharField(max_length=10, db_comment='纬度', verbose_name='纬度', null=True, blank=True)
    lng = models.CharField(max_length=10, db_comment='经度', verbose_name='经度', null=True, blank=True)
    parent = models.ForeignKey(
        to="self",
        verbose_name="父地区编码",
        to_field="code",
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True,
        blank=True,
        db_comment="父地区编码",
    )
    public_model = True

    class Meta:
        db_table = "area"
        verbose_name = "地区"
        db_table_comment = verbose_name
        ordering = ("code", )

    def __str__(self):
        return f"{self.name}"


class log(base_model):
    LOGIN_TYPE_CHOICES = ((1, "普通登录"), )
    username = models.CharField(max_length=32, verbose_name="登录用户名", null=True, blank=True, db_comment="登录用户名")
    ip = models.CharField(max_length=32, verbose_name="登录ip", null=True, blank=True, db_comment="登录ip")
    agent = models.TextField(verbose_name="agent信息", null=True, blank=True, db_comment="agent信息")
    browser = models.CharField(max_length=200, verbose_name="浏览器名", null=True, blank=True, db_comment="浏览器名")
    os = models.CharField(max_length=200, verbose_name="操作系统", null=True, blank=True, db_comment="操作系统")
    continent = models.CharField(max_length=50, verbose_name="州", null=True, blank=True, db_comment="州")
    country = models.CharField(max_length=50, verbose_name="国家", null=True, blank=True, db_comment="国家")
    province = models.CharField(max_length=50, verbose_name="省份", null=True, blank=True, db_comment="省份")
    city = models.CharField(max_length=50, verbose_name="城市", null=True, blank=True, db_comment="城市")
    district = models.CharField(max_length=50, verbose_name="县区", null=True, blank=True, db_comment="县区")
    isp = models.CharField(max_length=50, verbose_name="运营商", null=True, blank=True, db_comment="运营商")
    area_code = models.CharField(max_length=50, verbose_name="区域代码", null=True, blank=True, db_comment="区域代码")
    country_english = models.CharField(max_length=50, verbose_name="英文全称", null=True, blank=True, db_comment="英文全称")
    country_code = models.CharField(max_length=50, verbose_name="简称", null=True, blank=True, db_comment="简称")
    longitude = models.CharField(max_length=50, verbose_name="经度", null=True, blank=True, db_comment="经度")
    latitude = models.CharField(max_length=50, verbose_name="纬度", null=True, blank=True, db_comment="纬度")
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="登录类型", db_comment="登录类型")

    class Meta:
        db_table = "log"
        verbose_name = "登录日志"
        db_table_comment = verbose_name
        ordering = ("-create_time", )


class spider(base_model):
    name = models.CharField(max_length=50, db_comment='规则名称-')
    allowed_domains = models.CharField(max_length=800, db_comment='域名列表(逗号分隔)', null=True, blank=True)
    start_urls = models.CharField(max_length=200, db_comment='开始页(逗号分隔)', null=True, blank=True)

    type = models.IntegerField(choices=((1, '普通分页爬虫'), (2, 'json分页爬虫')), db_comment='类型', default=1)

    page_min = models.IntegerField(db_comment='页数最小值', null=True, blank=True)
    page_max = models.IntegerField(db_comment='页数最大值', null=True, blank=True)
    page_shift = models.CharField(max_length=200, db_comment='页码转换', null=True, blank=True)

    get_page = models.CharField(max_length=200, db_comment='分页提取', null=True, blank=True)
    get_item = models.CharField(max_length=200, db_comment='内容提取', null=True, blank=True)
    re_page = models.CharField(max_length=200, db_comment='分页过滤', null=True, blank=True)
    re_item = models.CharField(max_length=200, db_comment='内容过滤', null=True, blank=True)

    path_name = models.CharField(max_length=200, db_comment='标题获取', null=True, blank=True)
    path_time = models.CharField(max_length=200, db_comment='时间获取', null=True, blank=True)
    path_source = models.CharField(max_length=200, db_comment='来源获取', null=True, blank=True)
    path_content = models.CharField(max_length=200, db_comment='文章获取', null=True, blank=True)
    re_time = models.CharField(max_length=200, db_comment='时间提取', null=True, blank=True)
    re_source = models.CharField(max_length=200, db_comment='来源提取', null=True, blank=True)
    enable = models.BooleanField(db_comment="是否启用", default=True)

    class Meta:
        db_table = 'spider'
        verbose_name = "爬虫规则表"
        db_table_comment = verbose_name


class enterprise(base_model):
    name = models.CharField(max_length=100, verbose_name="名称", db_comment="名称", null=True)
    code = models.CharField(max_length=100, unique=True, db_comment='唯一编码', verbose_name="编码")
    area = models.ForeignKey(area, on_delete=models.DO_NOTHING, null=True, to_field="code", db_comment="区域", verbose_name='区域')
    file = models.JSONField(default=list, db_comment="文件", verbose_name='文件')
    image = models.JSONField(default=list, db_comment="图片", verbose_name='图片')  # JSON类型前端直接传列表就可以,不需要JSON化, 前端axios接收后也不用解析直接使用

    def delete(self, using=None, keep_parents=False):
        f = file.objects.filter(id__in=[i['id'] for i in [*self.file, *self.image]])
        for i in f:  # TODO:删除的同时删除文件,
            # 必须是单个model对象的delete才会触发, 文件必须是用f-jfile或f-jimage组件上传的
            i.delete()
        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        db_table = "enterprise"
        verbose_name = "企业"
        db_table_comment = verbose_name


class article(base_model):
    name = models.CharField(max_length=200, verbose_name="名称", db_comment='名称')
    source = models.CharField(max_length=200, verbose_name="来源", db_comment='来源', null=True)
    tag = models.IntegerField(verbose_name="标签", db_comment='标签', null=True)
    content = models.TextField(verbose_name="内容", db_comment='内容')
    file = models.JSONField(default=list, db_comment="文件", verbose_name='文件', null=True)
    url = models.CharField(max_length=100, db_comment='文章链接', verbose_name='文章链接', null=True, blank=True)
    url_hash = models.CharField(max_length=255, unique=True, db_index=True, null=True, blank=True)
    type = models.IntegerField(default=1, choices=((1, '发布'), (2, '抓取')), db_comment='文章类型(1 发布, 2 抓取)')

    view = models.IntegerField(db_comment="浏览数", default=0)
    like = models.IntegerField(db_comment="点赞数", default=0)
    comment = models.IntegerField(db_comment="评论数", default=0)
    collect = models.IntegerField(db_comment="收藏数", default=0)
    is_delete = models.BooleanField(default=False, db_comment='是否删除')
    is_top = models.BooleanField(default=False, db_comment='是否置顶')
    is_hot = models.BooleanField(default=False, db_comment='是否热门')
    is_original = models.BooleanField(default=False, db_comment='是否原创')
    is_recommend = models.BooleanField(default=False, db_comment='是否推荐')

    class Meta:
        db_table = "article"
        verbose_name = "文章"
        db_table_comment = verbose_name


class article_comment(base_model):
    user = models.ForeignKey(user_info, on_delete=models.PROTECT)
    article = models.ForeignKey(article, on_delete=models.PROTECT)
    content = models.CharField(max_length=1000, help_text='评论内容')
    reply = models.ForeignKey(to='self', help_text='回复对象', verbose_name='回复对象', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='reply_set')
    root = models.ForeignKey(to='self', help_text='根评论对象', verbose_name='根评论对象', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='root_set')

    class Meta:
        db_table = 'article_comment'
        db_table_comment = '文章评论'
        verbose_name = "文章评论"