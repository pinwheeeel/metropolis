from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import permissions, serializers

from core.api.serializers.course import CourseSerializer
from core.models import Term

from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)

    class Meta:
        model = Term
        ordering = ["-start_date"]
        fields = "__all__"


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ("GET", "HEAD", "OPTIONS")


class TermProvider(BaseProvider):
    permission_classes = [ReadOnly]
    model = Term
    raw_serializers = {
        "_": Serializer,
    }

    def get_queryset(self, request):
        return Term.objects.filter(
            end_date__gte=timezone.now() - settings.TERM_GRACE_PERIOD
        )

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="term")
            )
            .filter(object_id=str(view.get_object().pk))
            .latest("action_time")
            .action_time
        )

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="term")
            )
            .latest("action_time")
            .action_time
        )
