# Generated by Django 4.0.6 on 2022-08-05 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0002_remove_block_prev_blk_hash_block_prev_block_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='unix_timestamp',
            new_name='timestamp',
        ),
    ]
