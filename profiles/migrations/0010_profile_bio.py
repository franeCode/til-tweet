# Generated by Django 5.0 on 2024-01-06 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_codingstack_remove_profile_bio_profile_coding_stack'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default='Default bio', max_length=150, null=True),
        ),
    ]
