# Generated by Django 4.0.6 on 2022-08-05 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_transaction_block_alter_transaction_hash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='hash',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
