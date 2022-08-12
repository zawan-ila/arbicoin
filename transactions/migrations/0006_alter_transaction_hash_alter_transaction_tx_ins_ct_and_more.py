# Generated by Django 4.0.6 on 2022-08-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transaction_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='hash',
            field=models.CharField(blank=True, editable=False, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tx_ins_ct',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tx_outs_ct',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='txin',
            name='gen_tx_idx',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='txin',
            name='hash',
            field=models.CharField(blank=True, editable=False, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='txin',
            name='spend_tx_idx',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='txin',
            name='value',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='txout',
            name='blk_height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='txout',
            name='gen_tx_idx',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='txout',
            name='hash',
            field=models.CharField(blank=True, editable=False, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='txout',
            name='value',
            field=models.PositiveIntegerField(default=0),
        ),
    ]