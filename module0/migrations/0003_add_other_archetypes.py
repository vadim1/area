from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('module0', '0002_add_cheetah_answers'),
    ]

    # Store the other archetypes as a blob for now
    # This returned as a tuple from compute_archetypes
    operations = [
        migrations.AddField(
            model_name='Module0',
            name='other_archetypes',
            field=models.TextField(default=''),
        ),
    ]