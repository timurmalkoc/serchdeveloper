# Generated by Django 4.1.2 on 2022-10-31 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_rename_skills_skill"),
        ("project", "0005_project_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("owner", "project")},
        ),
    ]
