# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-22 03:30
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

def generate_wormholes(apps, schema_editor):
    Wormhole = apps.get_model('whsales', 'Wormhole')
    data = read_csv('wormholes.csv')
    for w in data:
        print "Creating " + w['name']
        clean_data = {}
        clean_data['lifetime'] = int(w['lifetime'])
        clean_data['jumpable'] = int(w['jumpable'])
        clean_data['mass'] = int(w['mass'])
        if w['regenerate'] == 'TRUE':
            clean_data['regenerate'] = True
        else:
            clean_data['regenerate'] = False
        w.update(clean_data)
        Wormhole.objects.update_or_create(name=w['name'], defaults=w)

def delete_wormholes(apps, schema_editor):
    Wormhole = apps.get_model('whsales', 'Wormhole')
    Wormhole.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('whsales', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_wormholes, delete_wormholes),
    ]
