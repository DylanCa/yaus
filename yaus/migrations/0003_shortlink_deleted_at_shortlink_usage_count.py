# Generated by Django 5.1.4 on 2025-01-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("yaus", "0002_shortlink_created_at_shortlink_owner_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="shortlink",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="shortlink",
            name="usage_count",
            field=models.IntegerField(default=0),
        ),
    ]