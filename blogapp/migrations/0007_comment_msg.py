# Generated by Django 3.0.3 on 2020-03-31 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_comment_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='msg',
            field=models.CharField(max_length=160, null=True),
        ),
    ]
