# Generated by Django 5.0 on 2024-01-04 04:35

import core.utils.fields
import django.db.models.deletion
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models, IntegrityError


def populate_bios(apps, schema_editor):
    StaffMember = apps.get_model("core", "StaffMember")
    User = apps.get_model("core", "User")
    
    for position, user_ids in settings.METROPOLIS_STAFFS.items():
        for user_id in user_ids:
            try:
                user = User.objects.get(pk=user_id)
                bio = settings.METROPOLIS_STAFF_BIO.get(user_id, "")
                staff_member, created = StaffMember.objects.get_or_create(
                    user=user, bio=bio
                )
                staff_member.positions = list(staff_member.positions) + [position]
                staff_member.save()
            except User.DoesNotExist:
                print(f"User {user_id} does not exist")
            except IntegrityError:
                print(f"StaffMember for user {user_id} already exists")


def reversed_pop(apps, schema_editor):
    raise RuntimeError("Cannot reverse this migration.")
    # just uncomment the above line if you want to reverse this migration, but you will lose all staff bios


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        (
            "core",
            "0058_fix_blogpost_featured_image_description_squashed_0068_remove_user_expo_notif_token_delete_recurrencerule",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffMember",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="staff",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        help_text="The users staff bio (displayed on the staff page)."
                    ),
                ),
                (
                    "positions",
                    core.utils.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("Project Manager", "Project Manager"),
                                ("Frontend Developer", "Frontend Developer"),
                                ("Backend Developer", "Backend Developer"),
                                ("App Developer", "App Developer"),
                                ("Graphic Designer", "Graphic Designer"),
                                ("Content Creator", "Content Creator"),
                                ("Doodle Developer", "Doodle Developer"),
                            ]
                        ),
                        help_text="The positions the user had/does hold.",
                        size=None,
                    ),
                ),
                (
                    "positions_leading",
                    core.utils.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("Frontend Developer", "Frontend Developer"),
                                ("Backend Developer", "Backend Developer"),
                                ("App Developer", "App Developer"),
                                ("Graphic Designer", "Graphic Designer"),
                                ("Content Creator", "Content Creator"),
                                ("Doodle Developer", "Doodle Developer"),
                            ]
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "years",
                    core.utils.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("2021-2022", "2021-2022"),
                                ("2022-2023", "2022-2023"),
                                ("2023-2024", "2023-2024"),
                                ("2024-2025", "2024-2025"),
                            ]
                        ),
                        help_text="The years the user was a staff member. Used to determine if the user is an alumni.",
                        size=None,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="If the user is no longer a member of metro for whatever reason. Toggle this instead of deleting.",
                    ),
                ),
            ],
            options={
                "verbose_name": "Staff Member",
                "verbose_name_plural": "Staff Members",
            },
        ),
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("username"),
                name="username-lower-check",
            ),
        ),
        migrations.AddConstraint(
            model_name="staffmember",
            constraint=models.UniqueConstraint(
                fields=("user",), name="unique_staff_member"
            ),
        ),
        migrations.RunPython(populate_bios, reversed_pop),
    ]
