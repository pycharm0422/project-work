# Generated by Django 2.2.17 on 2021-06-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_code', '0032_detail_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='profile_pic',
            field=models.ImageField(default='default_pic.jpg', null=True, upload_to='media/% Y/% m/% d/'),
        ),
    ]
