from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('module0', '0001_initial'),
    ]

    # Store the answers to cheetah sheet 1 as JSON blob for now
    operations = [
        migrations.AddField(
            model_name='Module0',
            name='cheetah_answers',
            field=models.TextField(default=''),
        ),
    ]