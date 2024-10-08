# Generated by Django 4.2.14 on 2024-08-02 21:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hlo", "0015_move_attachment_files"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stockitem",
            name="attachments",
            field=models.ManyToManyField(
                blank=True,
                related_name="stockitem",
                to="hlo.attachment",
            ),
        ),
    ]
