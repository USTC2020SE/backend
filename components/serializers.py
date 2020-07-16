from rest_framework.serializers import ModelSerializer
from .models import *


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class RemindSerializer(ModelSerializer):
    class Meta:
        model = Remind
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

