# Generated by Django 3.0.3 on 2020-04-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillbook_app', '0004_auto_20200406_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.FileField(default='1', upload_to='post_files'),
            preserve_default=False,
        ),
    ]
