# Generated by Django 4.0.6 on 2022-08-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0003_rename_unix_timestamp_block_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='hash',
            field=models.CharField(editable=False, max_length=40),
        ),
        migrations.AlterField(
            model_name='block',
            name='hash_target_zeros',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='block',
            name='height',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='block',
            name='merkle_hash',
            field=models.CharField(editable=False, max_length=40),
        ),
        migrations.AlterField(
            model_name='block',
            name='nonce',
            field=models.TextField(editable=False),
        ),
        migrations.AlterField(
            model_name='block',
            name='num_transactions',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='block',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
