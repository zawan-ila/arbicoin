# Generated by Django 4.0.6 on 2022-09-20 12:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transactioninput',
            name='gen_transaction',
            field=models.ForeignKey(blank=True, help_text='transaction that generated this input', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='used_outputs', to='transactions.transaction'),
        ),
    ]
