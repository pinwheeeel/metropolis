import json
from queue import LifoQueue

from django.db.models import signals
from django.dispatch import Signal, receiver
from django.http import StreamingHttpResponse
from rest_framework import permissions, response
from rest_framework import serializers as serializers2
from rest_framework.views import APIView

from .. import serializers
from ... import models

global_notifs = Signal()


@receiver(signals.post_save, sender=models.Announcement)
def announcement_change(sender, **kwargs):
    global_notifs.send("announcement_change", orig_sender=sender, kwargs=kwargs)


@receiver(signals.post_save, sender=models.BlogPost)
def blogpost_change(sender, **kwargs):
    global_notifs.send("blogpost_change", orig_sender=sender, kwargs=kwargs)


class NotificationStream:
    def __init__(
        self,
        signal,
        serializer,
    ):
        self.signal = signal
        self.serializer = serializer
        self.q = LifoQueue()
        self.__setup()

    def __setup(self):
        self.signal.connect(self.__receive)
        self.q.put(("init", {}))

    def __del__(self):
        self.signal.disconnect(self.__receive)

    def __receive(self, sender, **kwargs):
        self.q.put((sender, kwargs))

    def __iter__(self):
        return self

    def __next__(self):
        sender, kwargs = self.q.get()
        event_name, data = self.serializer(sender, **kwargs)
        return f"event: {event_name}\n" f"data: {json.dumps(data)}\n"


def serializer(sender, signal=None, orig_sender=None, kwargs={}):
    if sender == "announcement_change":
        return (
            sender,
            serializers.AnnouncementSerializer(kwargs["instance"]).data,
        )
    elif sender == "blogpost_change":
        return (
            sender,
            serializers.BlogPostSerializer(kwargs["instance"]).data,
        )
    else:
        return (sender, kwargs)


class NotificationsNew(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        response = StreamingHttpResponse(
            NotificationStream(
                signal=global_notifs,
                serializer=serializer,
            ),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        return response


class TokenSerializer(serializers2.Serializer):
    expo_push_token = serializers2.CharField()


class NotifToken(APIView):
    """
    Submit and delete notifcation push tokens.
    Supports Expo notification push tokens only for now.
    """

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, format=None):
        s = TokenSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        request.user.expo_notif_token = s.validated_data["expo_push_token"]
        request.user.save()
        return response.Response(None)

    def delete(self, request, format=None):
        request.user.expo_notif_token = None
        request.user.save()
        return response.Response(None)
