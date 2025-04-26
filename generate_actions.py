from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now, timedelta
import random

def generate_fake_logs(user, obj, count=10):
    content_type = ContentType.objects.get_for_model(obj)
    action_flags = [ADDITION, CHANGE, DELETION]
    messages = {
        ADDITION: "Added new object",
        CHANGE: "Updated object details",
        DELETION: "Deleted object"
    }

    for i in range(count):
        days_ago = random.randint(0, 10)
        time_offset = timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        action_flag = random.choice(action_flags)

        LogEntry.objects.create(
            user_id=user.id,
            content_type=content_type,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=action_flag,
            change_message=messages[action_flag],
            action_time=now() - time_offset
        )
