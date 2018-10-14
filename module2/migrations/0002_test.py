from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('module2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='Module2',
            name='perspective',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='Module2',
            name='opinions_reality',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='Module2',
            name='opinions_important',
            field=models.CharField(default='', max_length=10),
        ),
    ]