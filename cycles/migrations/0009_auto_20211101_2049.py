# Generated by Django 3.2.7 on 2021-11-01 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cycles', '0008_tripdetailsmodel_coordinates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tripdetailsmodel',
            name='pathdetails_loc',
        ),
        migrations.RemoveField(
            model_name='tripdetailsmodel',
            name='pathdetails_long',
        ),
    ]