from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0003_add_cc_lists'),
    ]

    # Store the cc_lists as a JSON blob for now
    operations = [
        migrations.AddField(
            model_name='Module1',
            name='living',
            field=models.TextField(default=''),
        ),
    ]