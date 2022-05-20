# Generated by Django 3.2.13 on 2022-05-08 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("cost", models.PositiveIntegerField(default=0)),
                ("price", models.PositiveIntegerField(default=0)),
                ("stock", models.PositiveIntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[("normal", "Normal"), ("archived", "Archived")],
                        default="normal",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
