# Generated by Django 2.1.7 on 2019-03-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ramiel', '0002_auto_20190302_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineuser',
            name='username',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='author',
            field=models.CharField(blank=True, max_length=110, null=True),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='author_line_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
