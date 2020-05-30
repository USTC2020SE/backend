from rest_framework.serializers import ModelSerializer
from .models import *


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class MessageIdSerializer(ModelSerializer):
    class Meta:
        model = MessageId
        fields = '__all__'


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TopicPictureSerializer(ModelSerializer):
    class Meta:
        model = TopicPicture
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
