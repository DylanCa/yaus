# Generated by Django 5.1.4 on 2025-01-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("yaus", "0003_shortlink_deleted_at_shortlink_usage_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shortlink",
            name="redirect_string",
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
