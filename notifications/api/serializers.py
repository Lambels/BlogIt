from rest_framework import serializers
from notifications.models import Notification


class NotificationSerizlizer(serializers.ModelSerializer):


    class Meta:
        model = Notification
        fields = '__all__'


class DeleteNotificationSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField()


    def validate_notification_id(self, notification_id):
        try:
            Notification.objects.get(id=notification_id)
            return notification_id
        except Notification.DoesNotExist:
            raise serializers.ValidationError("Notification not found.")


    def validate(self, data):
        notification = Notification.objects.get(id=data['notification_id'])

        if not notification.userTo == self.context.get('user'):
            raise serializers.ValidationError("You cant erase someone elses notification.")


        return data


    def update(self, instance, validated_data):
        notification = Notification.objects.get(id=validated_data['notification_id'])
        notification.delete()


        return notification