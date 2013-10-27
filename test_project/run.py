from __future__ import unicode_literals
import os
import sys
from importd import d

HERE = os.path.realpath(os.path.dirname(__file__))
PARENT = os.path.realpath(os.path.dirname(HERE))
sys.path.append(PARENT)

d(
    SITE_ID=1,
    LANGUAGES=[
        ('en', 'English'),
    ],
    # DATABASES={
    #     'default': {
    #         'ENGINE': "django.db.backends.sqlite3",
    #         'NAME': ':memory:',
    #     }
    # },
    INSTALLED_APPS=[
        "thadminjones",
        "thadminjones.contrib.treeadmin",
        "thadminjones.contrib.cms",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django.contrib.messages",
        "django.contrib.admin",
        "treeadmin",
        "cms",
        "mptt",
        "menus",
        "sekizai",
        "cms.plugins.twitter",
        "debug_toolbar",
    ],
    MIDDLEWARE_CLASSES=[
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware',
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ],
    INTERNAL_IPS=[
        "127.0.0.1",
    ],
    DEBUG_TOOLBAR_PANELS=[
        "debug_toolbar.panels.version.VersionDebugPanel",
        "debug_toolbar.panels.timer.TimerDebugPanel",
        "debug_toolbar.panels.request_vars.RequestVarsDebugPanel",
        "debug_toolbar.panels.template.TemplateDebugPanel",
        "debug_toolbar.panels.sql.SQLDebugPanel",
    ],
    DEBUG_TOOLBAR_CONFIG={
        "INTERCEPT_REDIRECTS": False,
        "HIDE_DJANGO_SQL": False,
        "ENABLE_STACKTRACES": True,
    },
    TEMPLATE_CONTEXT_PROCESSORS=[
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        'cms.context_processors.media',
        'sekizai.context_processors.sekizai',
    ],
    CMS_TEMPLATES=[
        ('cms_template.html', 'Template'),
    ],
    FIXTURE_DIRS=[HERE],
    STATIC_URL='/s/',
    MEDIA_URL='/m/',
    admin="^",
)

from django.db.models import (Model, BigIntegerField, BooleanField, CharField,
                              CommaSeparatedIntegerField, DateField,
                              DateTimeField, DecimalField, EmailField, FileField,
                              FilePathField, FloatField, ImageField,
                              IPAddressField, GenericIPAddressField,
                              NullBooleanField, PositiveIntegerField,
                              PositiveSmallIntegerField, SlugField,
                              SmallIntegerField, TextField, TimeField, URLField,
                              ForeignKey, ManyToManyField, OneToOneField)
from django.contrib import admin
from thadminjones.admin import SupportsQuickAdd

class TestModelFields(Model):
    big_int = BigIntegerField()
    yesno = BooleanField()
    title = CharField(max_length=150)
    csv_data = CommaSeparatedIntegerField(max_length=255)
    when = DateField()
    when_accurate = DateTimeField()
    amount = DecimalField(decimal_places=4)
    email = EmailField()
    upload = FileField(upload_to='test')
    path = FilePathField(path=HERE, recursive=False)
    inaccurate = FloatField()
    img = ImageField(upload_to='test')
    ip = IPAddressField()
    better_ip = GenericIPAddressField(protocol='both')
    yesnomaybe = NullBooleanField(default=None)
    posint = PositiveIntegerField()
    small_posint = PositiveSmallIntegerField()
    slug = SlugField()
    small_int = SmallIntegerField()
    content = TextField()
    when_time = TimeField()
    web_address = URLField()
    user = ForeignKey('auth.User')
    groups = ManyToManyField('auth.Group')
    one_to_one = OneToOneField('auth.Permission')

    class Meta:
        app_label = 'testing'
        verbose_name = 'test model fields'
        verbose_name_plural = 'test model fields'


class TestModelAdmin(SupportsQuickAdd, admin.ModelAdmin):
    pass
admin.site.register(TestModelFields, TestModelAdmin)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        d.do("syncdb", "--noinput")
        d.do('loaddata', 'initial_data.auth.json')
        d.do('loaddata', 'initial_data.cms.json')
        d.do("runserver", "0.0.0.0:8080")
    else:
        d.main()
