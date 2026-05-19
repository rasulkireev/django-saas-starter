import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
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
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=250)),
                ("description", models.TextField(blank=True)),
                ("slug", models.SlugField(max_length=250)),
                ("tags", models.TextField()),
                ("content", models.TextField()),
                ("icon", models.ImageField(blank=True, upload_to="blog_post_icons/")),
                ("image", models.ImageField(blank=True, upload_to="blog_post_images/")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("published", "Published"),
                        ],
                        default="draft",
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]
