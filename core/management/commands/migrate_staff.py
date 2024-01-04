from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.conf import settings
from core.models import (
    StaffMember,
    User,
)  # Update 'your_app' with the actual name of your app


class Command(BaseCommand):
    help = "Populate staff members based on METROPOLIS_STAFFS and bio settings."

    def handle(self, *args, **options):
        try:
            for position, user_ids in settings.METROPOLIS_STAFFS.items():
                for user_id in user_ids:
                    try:
                        user = User.objects.get(pk=user_id)
                        bio = settings.METROPOLIS_STAFF_BIO.get(user_id, "")
                        if not bio:
                            print(
                                f"Bio for user {user.username}  ID:{user.id} is empty"
                            )
                        staff_member, created = StaffMember.objects.get_or_create(
                            user=user, bio=bio
                        )
                        staff_member.positions = list(staff_member.positions) + [
                            position
                        ]
                        staff_member.save()
                    except User.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f"User {user_id} does not exist")
                        )
                    except IntegrityError:
                        self.stdout.write(
                            self.style.WARNING(
                                f"StaffMember for user {user_id} already exists"
                            )
                        )

        except AttributeError:
            self.stdout.write(
                self.style.SUCCESS("METROPOLIS_STAFFS does not exist anymore")
            )

        self.stdout.write(self.style.SUCCESS("Command completed successfully"))
