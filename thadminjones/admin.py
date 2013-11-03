# -*- coding: utf-8 -*-
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import NoReverseMatch, reverse


class SupportsQuickAdd(object):
    """
    A small mixin class to enable certain ModelAdmins to appear in a dropdown
    of links to add views for individual models; useful mostly to provide
    access site-wide to higher priority models [eg: in a CMS-esque fashion]
    """

    def has_quick_add_permission(self, request):
        return self.has_add_permission(request)

    def get_quick_add_url(self, request):
        if not self.has_quick_add_permission(request):
            return None
        opts = self.model._meta
        model_name = getattr(opts, 'model_name', opts.module_name)
        urlformat = '%s:%s_%s_add' % (self.admin_site.app_name, opts.app_label,
                                      model_name)
        try:
            url = reverse(urlformat)
        except NoReverseMatch as e:
            return None
        return {'url': url, 'name': opts.verbose_name}

    def get_model_perms(self, request):
        existing = super(SupportsQuickAdd, self).get_model_perms(request)
        if 'quickadd' not in existing:
            existing['quickadd'] = self.has_quick_add_permission(request)
        return existing
