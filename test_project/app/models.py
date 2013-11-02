# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from importd import d
from django.db.models import (Model, BigIntegerField, BooleanField, CharField,
                              CommaSeparatedIntegerField, DateField,
                              DateTimeField, DecimalField, EmailField, FileField,
                              FilePathField, FloatField, ImageField,
                              IPAddressField, GenericIPAddressField,
                              NullBooleanField, PositiveIntegerField,
                              PositiveSmallIntegerField, SlugField,
                              SmallIntegerField, TextField, TimeField, URLField,
                              ForeignKey, ManyToManyField, OneToOneField)


class TestModelFields(Model):
    big_int = BigIntegerField()
    yesno = BooleanField()
    title = CharField(max_length=150)
    csv_data = CommaSeparatedIntegerField(max_length=255)
    when = DateField()
    when_accurate = DateTimeField()
    amount = DecimalField(max_digits=8, decimal_places=4)
    email = EmailField()
    upload = FileField(upload_to='test')
    path = FilePathField(path=d.APP_DIR, recursive=False, match=".json$")
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
        verbose_name = 'test model fields'
        verbose_name_plural = 'test model fields'


class ReducedPermissions(TestModelFields):
    class Meta:
        proxy = True
        verbose_name = 'reduced permission'
        verbose_name_plural = 'reduced permissions'


class TestInlineModel(Model):
    fk = ForeignKey(TestModelFields)
    m2m = ManyToManyField('auth.User')
    yesno = BooleanField()
