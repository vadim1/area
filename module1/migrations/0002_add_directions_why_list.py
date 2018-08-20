from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0001_initial'),
    ]

    # Store the why_list as a JSON blob for now
    operations = [
        migrations.AddField(
            model_name='Module1',
            name='why_list',
            field=models.TextField(default=''),
        ),
    ]