# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-22 15:16
from __future__ import unicode_literals

from django.db import migrations
import csv
import os

def read_csv(name, delimiter=","):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), name)) as f:
        reader = csv.DictReader(f, delimiter=str(delimiter))
        data = []
        for row in reader:
            data.append(row)
    return data

def assign_statics(apps, schema_editor):
    Wormhole = apps.get_model('whsales', 'Wormhole')
    System = apps.get_model('whsales', 'System')
    data = read_csv('systems.csv', delimiter=',')
    for s in data:
        system = System.objects.get(id=int(s['solarSystemID']))
        if s['static1']:
            static = Wormhole.objects.get(name=s['static1'])
            system.statics.add(static)
            print "Assigning %s to %s" % (static.name, system.name)
        if s['static2']:
            static = Wormhole.objects.get(name=s['static2'])
            system.statics.add(static)
            print "Assigning %s to %s" % (static.name, system.name)

def remove_statics(apps, schema_editor):
    System = apps.get_model('whsales', 'System')
    for s in System.objects.all():
        s.statics.clear()

class Migration(migrations.Migration):

    dependencies = [
        ('whsales', '0003_systems'),
    ]

    operations = [
        migrations.RunPython(assign_statics, remove_statics)
    ]
