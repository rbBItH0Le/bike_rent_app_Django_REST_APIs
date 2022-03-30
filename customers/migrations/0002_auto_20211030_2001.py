# Generated by Django 3.2.7 on 2021-10-30 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customodel',
            name='active_trip_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customodel',
            name='email_verified',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='customodel',
            name='session_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='custsessionmodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]