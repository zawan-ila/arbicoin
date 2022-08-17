# Generated by Django 4.0.6 on 2022-08-17 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=40)),
                ('merkle_hash', models.CharField(max_length=40)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('height', models.PositiveIntegerField()),
                ('num_transactions', models.PositiveIntegerField()),
                ('hash_target_zeros', models.PositiveIntegerField(default=0, help_text='difficulty of mining the block')),
                ('nonce', models.TextField()),
                ('prev_block', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blocks.block')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
