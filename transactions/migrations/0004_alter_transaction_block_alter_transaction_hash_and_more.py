# Generated by Django 4.0.6 on 2022-08-05 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0002_remove_block_prev_blk_hash_block_prev_block_and_more'),
        ('transactions', '0003_alter_transaction_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='blocks.block'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='hash',
            field=models.CharField(default=22, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='txin',
            name='gen_tx',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.transaction'),
        ),
        migrations.AlterField(
            model_name='txin',
            name='spend_tx',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to='transactions.transaction'),
        ),
        migrations.AlterField(
            model_name='txout',
            name='gen_tx',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='transactions.transaction'),
        ),
    ]