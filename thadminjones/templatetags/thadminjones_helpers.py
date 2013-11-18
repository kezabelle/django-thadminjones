# -*- coding: utf-8 -*-
import logging
import re
from classytags.arguments import Argument, IntegerArgument
from classytags.core import Options, Tag
from classytags.helpers import AsTag, InclusionTag
from django import template
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.staticfiles.finders import AppDirectoriesFinder
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import resolve, reverse
from django.utils.encoding import force_unicode
from django.conf import settings
from django.utils.text import slugify


register = template.Library()
logger = logging.getLogger(__name__)
multiple_slashes_re = re.compile('/{2,}')


class FindMineralCSS(AsTag):
    name = 'thadminjones_css'
    options = Options(
        'as', Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, **kwargs):
        appdirs = AppDirectoriesFinder()
        targets = []
        for app_name in appdirs.apps:
            app = app_name
            if '.' in app_name:
                oldpath, app = app_name.rsplit('.', 1)
            target = '%s/css/thadminjones.css' % app
            if appdirs.find_in_app(app_name, target):
                targets.append(target)
        return targets

    def render_tag(self, context, **kwargs):
        varname = kwargs.pop(self.varname_name)
        value = self.get_value(context, **kwargs)
        if varname:
            context[varname] = value
            return ''
        css = '<link rel="stylesheet" type="text/css" href="%s">'
        return "\n".join(css % staticfiles_storage.url(x) for x in value)
register.tag(FindMineralCSS)


class AdminHelper(object):
    def __init__(self, request):
        self.request = request

    def get_namespace(self):
        current_view = resolve(self.request.path)
        namespace = getattr(current_view, 'app_name', None)
        if namespace is None:
            namespace = 'admin'
        return namespace

    def get_index_url(self):
        return reverse('%s:index' % self.get_namespace())

    def get_index_view(self):
        return resolve(self.get_index_url())


class MaybeFail(object):
    """
    collect various reasons to fail rendering ...
    """
    def __init__(self, request, context):
        self.request = request
        self.context = context

    def __call__(self):
        return not all([
            self.valid_user(),
            self.authenticated(),
            self.isnt_honeypot(),
        ])

    def valid_user(self):
        return hasattr(self.request, 'user')

    def authenticated(self):
        return self.request.user.is_authenticated()

    def isnt_honeypot(self):
        if 'admin_honeypot' in settings.INSTALLED_APPS:
            from admin_honeypot.forms import HoneypotLoginForm
            if ('form' in self.context
                    and isinstance(self.context['form'], HoneypotLoginForm)):
                return False
        return True


class AppList(InclusionTag):
    name = 'thadminjones_applist'
    template = 'thadminjones/applist.html'

    def get_context(self, context, **kwargs):
        request = context['request']
        if MaybeFail(request, context)():
            return {}

        index_view = AdminHelper(request).get_index_view()
        template_response = index_view.func(request)
        return {
            'apps': template_response.context_data['app_list'],
            'current_app': template_response._current_app,
            'path': request.path,
        }
register.tag(AppList)


class QuickAddList(InclusionTag):
    name = 'thadminjones_quickadd'
    template = 'thadminjones/quickadd.html'

    def get_models(self, request, admin_site):
        for model, model_admin in admin_site._registry.items():
            if not hasattr(model_admin, 'has_quick_add_permission'):
                logger.debug(
                    "{cls!r} doesn't have "
                    "`has_quick_add_permission`".format(cls=model_admin)
                )
                continue

            if not hasattr(model_admin, 'get_quick_add_url'):
                logger.debug(
                    "{cls!r} doesn't have `get_quick_add_url`, but did have "
                    "`has_quick_add_permission`".format(cls=model_admin)
                )
                continue

            if model_admin.has_quick_add_permission(request):
                result = model_admin.get_quick_add_url(request)
                if result is None:
                    logger.debug(
                        "{cls!r} `get_quick_add_url` returned nothing worth "
                        "mentioning".format(cls=model_admin)
                    )
                else:
                    yield result

    def get_context(self, context, **kwargs):
        request = context['request']
        if MaybeFail(request, context)():
            return {}
        index_view = AdminHelper(request).get_index_view()
        admin_site = index_view.func.func_closure[0].cell_contents
        models = sorted(self.get_models(request, admin_site),
                        key=lambda dict_: force_unicode(dict_['name']))
        template_response = index_view.func(request)
        return {
            'models': models,
            'current_app': template_response._current_app,
            'path': request.path,
        }
register.tag(QuickAddList)


class RecentActions(InclusionTag):
    name = 'thadminjones_recentactions'
    template = 'thadminjones/recentactions.html'

    options = Options(
        IntegerArgument('maxnum', default=10, required=False, resolve=True),
    )

    def get_context(self, context, maxnum, **kwargs):
        request = context['request']
        if MaybeFail(request, context)():
            return {}

        root_url = AdminHelper(request).get_index_url()

        def get_log_entries(user_id, maxnum, admin_root):
            """
            This exists because LogEntry has a stupid bloody get_absolute_url()
            in < 1.6
            """
            entries = (LogEntry.objects.filter(user__id__exact=user_id)
                       .exclude(action_flag=DELETION)
                       .select_related('content_type', 'user'))
            for entry in entries[:maxnum]:
                existing_url = entry.get_admin_url()
                if not existing_url.startswith(admin_root):
                    real_url = '/%s/%s/' % (admin_root, existing_url)
                    entry.get_absolute_url = re.sub(pattern=multiple_slashes_re,
                                                    repl='/', string=real_url)
                else:
                    entry.get_absolute_url = existing_url
                yield entry

        entries = get_log_entries(user_id=request.user.pk, maxnum=maxnum,
                                  admin_root=root_url)
        return {
            'admin_log': list(entries),
        }
register.tag(RecentActions)


class SlugifyForAdmin(Tag):
    name = 'thadminjones_slugify'

    def render_tag(self, context, **kwargs):
        request = context['request']
        path = unicode(request.path)
        root_url = AdminHelper(request).get_index_url()
        return slugify(path.replace(root_url, '').strip('/'))
register.tag(SlugifyForAdmin)
