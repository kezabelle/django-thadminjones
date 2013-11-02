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
        "django_pdb",
        "app",
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

from django.template.loader import add_to_builtins
add_to_builtins('django_pdb.templatetags.pdb')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        d.do("syncdb", "--noinput")
        d.do('loaddata', 'initial_data.auth.json')
        d.do('loaddata', 'initial_data.cms.json')
        d.do("runserver", "0.0.0.0:8080")
    else:
        d.main()
