from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class AccountView(ModelViewSet):
    # provide default GET/POST/DELETE/PUT
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'nickname', 'type',)


class MessageIdView(ModelViewSet):
    queryset = MessageId.objects.all()
    serializer_class = MessageIdSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)


class TopicView(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'sender', 'anonymity', 'category', 'tags',)


class TopicPictureView(ModelViewSet):
    queryset = TopicPicture.objects.all()
    serializer_class = TopicPictureSerializer
    lookup_field = 'topic_id'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('topic_id',)


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'comment_id'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('comment_id', 'master_id', 'sender', 'anonymity')


class ReportView(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'message_id', 'reporter', 'status',)
