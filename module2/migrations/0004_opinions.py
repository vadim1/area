from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('module2', '0003_more_facts'),
    ]

    operations = [
        migrations.AddField(
            model_name='Module2',
            name='opinions',
            field=models.TextField(default=''),
        ),
    ]