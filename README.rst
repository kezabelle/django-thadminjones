===================
Thadmin Jones 0.1.0
===================

`thadminjones` is a package for the `Django`_ `admin`_ backend, implementing
a new theme, reminiscent of the `Wordpress`_ administration.

It's less of a whole-sale replacement than many other packages, insofar
as only the following templates have been changed:

* `admin/base_site.html`
* `admin/filter.html`

and the existing CSS is built upon, rather than thrown out to start from
scratch.

Due to the non-intrusive nature of the theme, things like nice responsive
changelist tables haven't been addressed.

The license
-----------

Let us get this out of the way. It's GPLv2. Not the license I'd have
picked, but `Wordpress`_ is also `GPLv2`_, and as this is probably considered
a derivitive work, the viral nature of the GPL requires this be
GPL compatible, and I don't know licenses enough to make an informed
decision as to whether another license would be permissable.

I'm sorry if that means you can't use this, or contribute to it.

.. _GPLv2: http://wordpress.org/about/license/

How to install
--------------

Edit your ``INSTALLED_APPS`` to reflect the new
package::

  INSTALLED_APPS = (
    'thadminjones',
    'django.contrib.admin',
  )

Due to the way templates are discovered, you must explicitly opt-in to
using the `thadminjones` templates, which means the package **must** be
before the standard `admin`_ package.

Alternatively, if you have any ``TEMPLATE_DIRS`` which include any of
the following templates, you may need to adapt those to include the
template changes required by `thadminjones`:

* `admin/base_site.html`
* `admin/filter.html`

Features
--------

The **quick add** menu
^^^^^^^^^^^^^^^^^^^^^^

As a convienience, it is possible to have certain ``ModelAdmin``
instances listed in a **Quick Add** menu at the top of every
page; to enable a ``ModelAdmin`` in this menu, you can either
inherit from the ``SupportsQuickAdd`` mixin class::

  from thadminjones.admin import SupportsQuickAdd

  class MyModelAdmin(SupportsQuickAdd, ModelAdmin):
      pass

or you can define `has_quick_add_permission` and `get_quick_add_url`
on your existing ``ModelAdmin``. See the implementation of the mixin
class for implementation info.

What about third party apps?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Other apps can have styles pulled in by including a file in::

  <app.name>/static/<last.part.of.app.name>/css/thadminjones.css

They will be put in the right place by the `collectstatic`_
management command, and are discovered by a template tag in the
bundled `admin/base_site.html` which looks for certain filenames
using the AppDirectories `staticfiles`_ finder.

.. _collectstatic: https://docs.djangoproject.com/en/stable/ref/contrib/staticfiles/#django-admin-collectstatic
.. _staticfiles: https://docs.djangoproject.com/en/stable/ref/contrib/staticfiles/

About the name
--------------

It's a play on words, a reference to `Thad Jones`_, a Jazz musician.
I'm hardly alone in naming `Django`_ packages in relation to Jazz,
as off the top of my head I can think of:

* `Grappelli`_ (`Stéphane Grappelli`_)
* `Ella`_ (`Ella Fitzgerald`_)
* `Armstrong`_ (`Louis Armstrong`_)
* `Ellington`_ (`Duke Ellington`_)
* `Mingus`_ (`Charles Mingus`_)
* (maybe) `django-bakery`_ (`Chet Baker`_)

.. _Thad Jones: http://en.wikipedia.org/wiki/Thad_Jones
.. _Grappelli: http://grappelliproject.com/
.. _Stéphane Grappelli: http://en.wikipedia.org/wiki/St%C3%A9phane_Grappelli
.. _Ella: https://github.com/ella/ella
.. _Ella Fitzgerald: http://en.wikipedia.org/wiki/Ella_Fitzgerald
.. _Armstrong: http://armstrongcms.org/
.. _Louis Armstrong: http://en.wikipedia.org/wiki/Louis_Armstrong
.. _Ellington: http://www.ellingtoncms.com/
.. _Duke Ellington: http://en.wikipedia.org/wiki/Duke_Ellington
.. _Mingus: https://github.com/montylounge/django-mingus
.. _Charles Mingus: http://en.wikipedia.org/wiki/Charles_Mingus
.. _django-bakery: https://github.com/datadesk/django-bakery
.. _Chet Baker: http://en.wikipedia.org/wiki/Chet_Baker

Screenshots
-----------

* TODO :(

Contributing
------------

The quickest way to get up and running to contribute is::

    $ mkvirtualenv thadmin
    $ git clone git@github.com:kezabelle/django-thadminjones.git
    $ python django-thadminjones/setup.py develop

Which will install all the requirements for running the ``test_project``,
thereafter, you can spin up a clean-room project accessible at 127.0.0.1:8080
by doing::

    $ python django-thadminjones/test_project/run.py

Tickets can be opened on the `django-thadminjones GitHub repository`_ - if you're
reporting a visual bug, please try to include a screenshot illustrating the
problem, or a pull request for the ``test_project`` to demonstrate it.

.. _django-thadminjones GitHub repository: https://github.com/kezabelle/django-thadminjones/issues

.. _Django: https://djangoproject.com/
.. _admin: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
.. _Wordpress: http://wordpress.org/
