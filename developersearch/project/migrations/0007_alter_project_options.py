# Generated by Django 4.1.2 on 2022-10-31 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0006_review_owner_alter_review_unique_together"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["-created"]},
        ),
    ]
