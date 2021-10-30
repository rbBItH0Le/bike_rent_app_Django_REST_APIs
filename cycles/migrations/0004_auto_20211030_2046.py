# Generated by Django 3.2.7 on 2021-10-30 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycles', '0003_auto_20211030_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='activetripmodel',
            name='ended_at',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='activetripmodel',
            name='started_at',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tripmodel',
            name='charge',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tripmodel',
            name='ended_at',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tripmodel',
            name='started_at',
            field=models.BigIntegerField(null=True),
        ),
    ]