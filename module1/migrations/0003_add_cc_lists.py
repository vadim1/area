from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0002_add_directions_why_list'),
    ]

    # Store the cc_lists as a JSON blob for now
    operations = [
        migrations.AddField(
            model_name='Module1',
            name='cc1_list',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='Module1',
            name='cc2_list',
            field=models.TextField(default=''),
        ),
    ]