from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('module2', '0002_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='Module2',
            name='more_facts',
            field=models.TextField(default=''),
        ),
    ]