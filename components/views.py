from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView, UpdateAPIView, CreateAPIView
import hashlib
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.mixins import *
from django_filters.rest_framework import DjangoFilterBackend


EXPIRE = 600    # Token 过期时间，单位秒
REMIND_TOPIC_FOCUS = '您的话题收到关注'

# Create your views here.


def auth(token):
    ret = Token.objects.filter(token=token).first()
    if not ret:
        raise exceptions.AuthenticationFailed
    duration = timezone.now() - ret.time
    if duration.total_seconds() > EXPIRE:
        ret.delete()
        raise exceptions.APIException('Authentication expired.')
    return


def msgType(id):
    # 根据 id 判断是 topic(1) 还是 reply(2) 还是没有(0)
    topic = Topic.objects.filter(topic_id=id).first()
    if not topic:
        reply = Reply.objects.filter(reply_id=id).first()
        if not reply:
            return 0
        else:
            return 2
    else:
        return 1


def remindTopicFocusMsg(topic_id):
    return '您的话题' + str(topic_id) + '收到关注.'

class Login(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        nickname = request.data.get('nickname')
        password = request.data.get('password')
        try:
            user = Account.objects.get(nickname=nickname)
            if user.password == password:
                token = hashlib.md5()
                token.update(str(timezone.now()).encode('utf-8'))
                token.update(str(user.nickname).encode('utf-8'))
                token = token.hexdigest()
                Token.objects.update_or_create(nickname=nickname, defaults={
                    'token': token,
                    'time': timezone.now()
                })
                data = {
                    'status': 'success',
                    'token': token
                }
                return Response(data)
            else:
                raise exceptions.AuthenticationFailed
        except Account.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, *args, **kwargs):
        return Response("")


class Signup(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = SignupSerializer

    def get(self, request, *args, **kwargs):
        return Response("")


class getUserInfo(ListAPIView):     # DONE
    queryset = Account.objects.all()
    serializer_class = InfoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('account_id',)


class updateUserInfo(UpdateModelMixin, GenericViewSet):     # DONE
    """
    向 infou/account_id/ 发送 PUT/PATCH 以进行更新
    """
    queryset = Account.objects.all()
    serializer_class = InfoSerializer


class getTopic(ListAPIView):        # DONE
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('topic_id',)


class updateTopic(UpdateModelMixin, GenericViewSet):        # DONE
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class getReply(ListAPIView):            # DONE
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('reply_id',)


class createReply(CreateAPIView):       # DONE
    queryset = Reply.objects.all()
    serializer_class = ReplyCreateSerializer

    def post(self, request, *args, **kwargs):
        ret = self.create(request, *args, **kwargs)
        parent_id = request.data.get('master_id')
        parent_msg_type = msgType(parent_id)
        if parent_msg_type == 1:
            parent_topic = Topic.objects.filter(topic_id=parent_id).first()
            create_remind = Remind.objects.create(
                receiver_id=parent_topic.account_id,
                content='您的话题'+str(parent_id)+'收到回复'
            )
        elif parent_msg_type == 2:
            parent_reply = Reply.objects.filter(reply_id=parent_id).first()
            create_remind = Remind.objects.create(
                receiver_id=parent_reply.account_id,
                content='您的回复/评论'+str(parent_id)+'收到评论'
            )
        else:
            raise exceptions.NotFound
        return ret


class updateReply(UpdateModelMixin, GenericViewSet):        # DONE
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()


class getRemind(ListAPIView):       # DONE
    queryset = Remind.objects.all()
    serializer_class = RemindSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('remind_id',)


class createRemind(CreateAPIView):      # not needed?
    queryset = Remind.objects.all()
    serializer_class = RemindSerializer


class getMsgsFromUser(ListAPIView):     # DONE
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        ret_list = []
        topics = Topic.objects.filter(account_id=user_id)
        replies = Reply.objects.filter(account_id=user_id)
        for topic in topics:
            ret_list.append([topic.topic_id.id, 1])
        for reply in replies:
            ret_list.append([reply.reply_id.id, 2])
        return Response(data=ret_list, status=status.HTTP_200_OK)


class getFocusFromUser(ListAPIView):
    queryset = FocusAccount.objects.all()
    serializer_class = FocusAccountSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('focusing_id',)


class getFocusTopic(ListAPIView):
    queryset = FocusTopic.objects.all()
    serializer_class = FocusTopicSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('account_id',)


class collectReply(ListCreateAPIView):      # DONE
    queryset = ReplyCollect.objects.all()
    serializer_class = ReplyCollectSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('account_id',)

    def post(self, request, *args, **kwargs):
        ret = self.create(request, *args, **kwargs)
        reply = Reply.objects.filter(reply_id=request.data.get('reply_id')).first()
        reply_creator = reply.account_id
        created_remind = Remind.objects.create(
            receiver_id=reply_creator,
            content='回复/评论'+str(reply.reply_id.id)+'收到收藏'
        )
        return ret


class getRemindFromUser(ListAPIView):       # DONE
    queryset = Remind.objects.all()
    serializer_class = RemindSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        ret_list = []
        reminds = Remind.objects.filter(receiver_id=user_id)
        for remind in reminds:
            ret_list.append(remind.remind_id)
        return Response(data=ret_list, status=status.HTTP_200_OK)


class getCategory(ListAPIView):     # DONE
    queryset = Category1.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        categories = []
        cat1 = Category1.objects.all()
        cat2 = Category2.objects.all()
        for cat in cat1:
            categories.append([cat.category1_name,0,cat.category1_id])
        for cat in cat2:
            categories.append([cat.category2_name,Category1.objects.filter(category1_id=cat.category1_id.category1_id).first().category1_name,cat.category2_id])
        return Response(data=categories, status=status.HTTP_200_OK)


class createCategory1(CreateAPIView):       # backdoor
    queryset = Category1.objects.all()
    serializer_class = CategorySerializer


class createCategory2(CreateAPIView):       # backdoor
    queryset = Category2.objects.all()
    serializer_class = Category2Serializer


class getTopicFromCategory(ListAPIView):       # DONE
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get(self, request, *args, **kwargs):
        cat = request.data.get('category')
        ret_list = []
        topics = Topic.objects.filter(category2_id=cat)
        for topic in topics:
            ret_list.append(topic.topic_id.id)
        return Response(data=ret_list, status=status.HTTP_200_OK)


class createTopic(CreateAPIView):       # DONE
    queryset = Topic.objects.all()
    serializer_class = TopicCreateSerializer


class createFocusFromTopic(CreateAPIView):      # DONE
    queryset = FocusTopic.objects.all()
    serializer_class = FocusTopicSerializer

    def post(self, request, *args, **kwargs):
        ret = self.create(request, *args, **kwargs)
        focused_id = request.data.get('focused_id')
        focused_topic = Topic.objects.filter(topic_id=focused_id).first()
        focused_topic_creator = focused_topic.account_id
        created_remind = Remind.objects.create(
            receiver_id=focused_topic_creator,
            content=remindTopicFocusMsg(focused_id)
        )
        return ret


class createReportFromMsg(CreateAPIView):       # DONE
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def post(self, request, *args, **kwargs):
        ret = self.create(request, *args, **kwargs)
        msg_id = request.data.get('message_id')
        reported_msg_type = msgType(msg_id)
        if reported_msg_type == 1:  # Topic
            reported_topic = Topic.objects.filter(topic_id=msg_id).first()
            reported_topic_creator = reported_topic.account_id
            created_remind_user = Remind.objects.create(
                receiver_id=reported_topic_creator,
                content='话题'+str(msg_id)+'收到举报'
            )
            superlist = Account.objects.filter(type='super')
            for super in superlist:
                created_remind_super = Remind.objects.create(
                receiver_id=super.account_id,
                content='话题'+str(msg_id)+'收到举报'
            )
        elif reported_msg_type == 2:
            reported_reply = Reply.objects.filter(reply_id=msg_id).first()
            reported_reply_creator = reported_reply.account_id
            created_remind_user = Remind.objects.create(
                receiver_id=reported_reply_creator,
                content='回复/评论'+str(msg_id)+'收到举报'
            )
            superlist = Account.objects.filter(type='super')
            for super in superlist:
                created_remind_super = Remind.objects.create(
                receiver_id=super.account_id,
                content='回复/评论'+str(msg_id)+'收到举报'
            )
        return ret


class createAttitudeFromMsg(CreateAPIView):     # DONE
    queryset = TopicAttitude.objects.all()
    serializer_class = TopicAttitudeSerializer

    def post(self, request, *args, **kwargs):
        msg_type = msgType(request.data.get('id'))
        attitude=request.data.get('attitude')
        if msg_type == 1:   # Topic
            try:
                ret = TopicAttitude.objects.create(
                    topic_id=Topic.objects.filter(topic_id=request.data.get('id')).first(),
                    account_id=Account.objects.filter(account_id=request.data.get('account_id')).first(),
                    attitude=True if attitude == 1 else False
                )
                topic = Topic.objects.filter(topic_id=request.data.get('id')).first()
                if attitude == 1:
                    old_up = topic.up_vote_count
                    Topic.objects.filter(topic_id=request.data.get('id')).update(up_vote_count=old_up+1)
                    topic_creator = topic.account_id
                    create_remind = Remind.objects.create(
                        receiver_id=topic_creator,
                        content='话题'+str(topic.topic_id.id)+'收到一个赞'
                    )
                elif attitude == 2:
                    old_down = topic.down_vote_count
                    Topic.objects.filter(topic_id=request.data.get('id')).update(down_vote_count=old_down+1)
                    topic_creator = topic.account_id
                    create_remind = Remind.objects.create(
                        receiver_id=topic_creator,
                        content='话题'+str(topic.topic_id.id)+'收到一个踩'
                    )
                return Response(status.HTTP_200_OK)
            except:
                return Response(status.HTTP_400_BAD_REQUEST)
        elif msg_type == 2:
            try:
                ret = ReplyAttitude.objects.create(
                    reply_id=Reply.objects.filter(reply_id=request.data.get('id')).first(),
                    account_id=Account.objects.filter(account_id=request.data.get('account_id')).first(),
                    attitude=True if attitude == 1 else False
                )
                reply = Reply.objects.filter(reply_id=request.data.get('id')).first()
                if attitude == 1:
                    old_up = reply.up_vote_count
                    Reply.objects.filter(reply_id=request.data.get('id')).update(up_vote_count=old_up+1)
                    reply_creator = reply.account_id
                    create_remind = Remind.objects.create(
                        receiver_id=reply_creator,
                        content='回复/评论'+str(reply.reply_id.id)+'收到一个赞'
                    )
                elif attitude == 2:
                    old_down = reply.down_vote_count
                    Reply.objects.filter(reply_id=request.data.get('id')).update(down_vote_count=old_down+1)
                    reply_creator = reply.account_id
                    create_remind = Remind.objects.create(
                        receiver_id=reply_creator,
                        content='回复/评论'+str(reply.reply_id.id)+'收到一个踩'
                    )
                return Response(status.HTTP_200_OK)
            except:
                return Response(status.HTTP_400_BAD_REQUEST)
        return Response(status.HTTP_404_NOT_FOUND)


class getReplyFromMsg(ListAPIView):     # DONE
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get(self, request, *args, **kwargs):
        ret = []
        direct = Reply.objects.filter(master_id=request.data.get('id'))
        for msg in direct:
            ret.append([msg.reply_id.id, msg.master_id.id])
        for item in ret:
            append_list = Reply.objects.filter(master_id=item[0])
            for append_item in append_list:
                ret.append([append_item.reply_id.id, append_item.master_id.id])
        return Response(data=ret, status=status.HTTP_200_OK)


class dealReport(CreateAPIView):        # DONE
    queryset = Remind.objects.all()
    serializer_class = RemindSerializer

    def post(self, request, *args, **kwargs):
        is_super = False
        superlist = Account.objects.filter(type='super')
        for super in superlist:
            if super.account_id == request.data.get('id'):
                is_super = True
        if is_super is False:
            raise exceptions.AuthenticationFailed
        report_id = request.data.get('report_id')
        reason = request.data.get('reason')
        status = request.data.get('status')
        Report.objects.filter(report_id=report_id).update(
            reason=reason,
            status=status
        )
        report = Report.objects.filter(report_id=report_id).first()
        reporter = report.reporter
        create_remind = Remind.objects.create(
            receiver_id=reporter,
            content='您对'+str(report_id)+'的举报已有结果'
        )
        msg_id = report.message_id
        msg_type = msgType(msg_id)
        if msg_type == 1:
            topic_creator = Topic.objects.filter(topic_id=msg_id).first().account_id
            create_remind = Remind.objects.create(
                receiver_id=topic_creator,
                content='您的话题'+str(report_id)+'被举报，已有结果'
            )
            if status == 'success':
                Topic.objects.filter(topic_id=msg_id).update(legal=False)
        elif msg_type == 2:
            reply_creator = Reply.objects.filter(reply_id=msg_id).first().account_id
            create_remind = Remind.objects.create(
                receiver_id=reply_creator,
                content='您的回复/评论'+str(report_id)+'被举报，已有结果'
            )
            if status == 'success':
                Reply.objects.filter(reply_id=msg_id).update(legal=False)
        else:
            raise exceptions.NotFound
        return Response(data=report)


class Super(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = SuperSignupSerializer
