from rest_framework.serializers import ModelSerializer
from .models import *


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class LoginSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['nickname', 'password']


class SignupSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'nickname',
            'password',
            'avatar',
            'background',
            'signature'
        ]


class SuperSignupSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'nickname',
            'password',
            'avatar',
            'background',
            'signature'
        ]

    def create(self, validated_data):
        validated_data['type'] = 'super'
        return Account.objects.create(**validated_data)


class InfoSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'account_id',
            'nickname',
            'avatar',
            'background',
            'signature'
        ]


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ['token', 'date']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

    def create(self, validated_data):
        new_id = Id.objects.create()
        validated_data['topic_id'] = new_id
        return Topic.objects.create(**validated_data)


class TopicCreateSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['category2_id', 'account_id', 'content', 'tags']

    def create(self, validated_data):
        new_id = Id.objects.create()
        validated_data['topic_id'] = new_id
        return Topic.objects.create(**validated_data)


class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        new_id = Id.objects.create()
        validated_data['reply_id'] = new_id
        return Reply.objects.create(**validated_data)


class ReplyCreateSerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = ['master_id', 'account_id', 'content']

    def create(self, validated_data):
        new_id = Id.objects.create()
        validated_data['reply_id'] = new_id
        return Reply.objects.create(**validated_data)


class RemindSerializer(ModelSerializer):
    class Meta:
        model = Remind
        fields = '__all__'


class FocusAccountSerializer(ModelSerializer):
    class Meta:
        model = FocusAccount
        fields = '__all__'


class FocusTopicSerializer(ModelSerializer):
    class Meta:
        model = FocusTopic
        fields = '__all__'


class ReplyCollectSerializer(ModelSerializer):
    class Meta:
        model = ReplyCollect
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category1
        fields = '__all__'


class Category2Serializer(ModelSerializer):
    class Meta:
        model = Category2
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class TopicAttitudeSerializer(ModelSerializer):
    class Meta:
        model = TopicAttitude
        fields = '__all__'
