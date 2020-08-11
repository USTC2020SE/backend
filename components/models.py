from django.db import models
from django.utils import timezone

# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<id>/<filename>
    return 'users/{0}/{1}'.format(instance.id, filename)


def topic_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/topics/<id>/<filename>
    return 'topics/{0}/{1}'.format(instance.topic_id, filename)


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)     # 账户ID(PK)
    password = models.CharField(max_length=15)
    nickname = models.CharField(max_length=15)  # 账户昵称
    # avatar = models.ImageField(upload_to=user_directory_path)    # 头像 - 目录储存方式
    # background = models.ImageField(upload_to=user_directory_path)    # 背景图片 - 目录储存方式
    avatar = models.CharField(max_length=500)   # 头像 - base64储存方式
    background = models.CharField(max_length=1000) # 背景图片 - bas64储存方式
    signature = models.CharField(max_length=50) # 签名或个人简介
    NORMAL = 'normal'
    SUPER = 'super'
    ACCOUNT_TYPE = [
        (NORMAL, '普通用户'),
        (SUPER, '管理用户'),
    ]
    type = models.CharField(max_length=10, default=NORMAL, choices=ACCOUNT_TYPE)


class Token(models.Model):
    name = models.CharField(max_length=15, primary_key=True)
    token = models.CharField(max_length=64)
    time = models.DateTimeField()
    date = models.CharField(max_length=12, default="")


class FocusAccount(models.Model): # 用户关注别人，多对多关系，使用一张表专门记录
    focusing_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id', related_name='focusing_id')
    focused_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id', related_name='focused_id')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['focusing_id', 'focused_id'], name='unique_focus')
        ]


class Category1(models.Model):  # 顶层分类
    category1_id = models.AutoField(primary_key=True)
    category1_name = models.TextField()


class Category2(models.Model):  # 第二层分类
    category2_id = models.AutoField(primary_key=True)
    category2_name = models.TextField()
    category1_id = models.ForeignKey('Category1', on_delete=models.CASCADE, to_field='category1_id')

# 匿名的话，判断anonymity。如果不匿名，就使用用户昵称为显示名称。如果匿名，就使用account_id和topic_id一起Hash得出匿名名称


class Id(models.Model):
    id = models.AutoField(primary_key=True)     # Topic / Reply 的统一 ID 空间


class Topic(models.Model):  # 主题
    # topic_id = models.AutoField(primary_key=True)  # 主题id
    topic_id = models.OneToOneField('Id', on_delete=models.CASCADE, to_field='id', primary_key=True)
    category2_id = models.ForeignKey('Category2', on_delete=models.CASCADE, to_field='category2_id')
    account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')  # 发送者
    content = models.TextField()                # 内容
    create_time = models.DateTimeField()        # 创建时间，用以排序。一般从最新的信息到较老的信息排序
    tags = models.BigIntegerField()             # 话题标签，请使用一个整数表示该话题的所有标签，最长64位。这个暂时不知道是干嘛用的
    legal = models.BooleanField()               # 合法性，当前内容被举报不合法时，不应该对非主题/回复/评论发布者显示内容
    up_vote_count = models.IntegerField()       # 主题被点赞计数
    down_vote_count = models.IntegerField()


class FocusTopic(models.Model): # 用户关注别人，多对多关系，使用一张表专门记录
    topic_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
    focused_id = models.ForeignKey('Topic', on_delete=models.CASCADE, to_field='topic_id')


class TopicAttitude(models.Model):
    topic_id = models.ForeignKey('Topic', on_delete=models.CASCADE, to_field='topic_id')
    account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
    attitude = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['topic_id', 'account_id'], name='unique_topic_attitude')  # 主题id和账号的联合唯一约束, 一个账号对同一个主题只能有一种态度
        ]

# class TopicUpVote(models.Model): # 用户点赞主题，多对多关系，使用一张表专门记录。下同，不再赘述
#     topic_id = models.ForeignKey('Topic', on_delete=models.CASCADE, to_field='topic_id')
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
#
#
# class TopicDownVote(models.Model):
#     topic_id = models.ForeignKey('Topic', on_delete=models.CASCADE, to_field='topic_id')
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')


class Reply(models.Model):
    reply_id = models.OneToOneField('Id', on_delete=models.CASCADE, to_field='id', primary_key=True)   # Reply id
    master_id = models.ForeignKey('Id', on_delete=models.CASCADE, to_field='id', related_name='master_id')    # 父消息ID
    account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
    content = models.TextField()
    create_time = models.DateTimeField()
    legal = models.BooleanField(default=True)
    up_vote_count = models.IntegerField(default=0)
    down_vote_count = models.IntegerField(default=0)


class ReplyAttitude(models.Model):
    reply_id = models.ForeignKey('Reply', on_delete=models.CASCADE, to_field='reply_id')
    account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
    attitude = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reply_id', 'account_id'], name='unique_reply_attitude')  # 消息id和账号的联合唯一约束, 一个账号对同一个消息只能有一种态度
        ]


class ReplyCollect(models.Model):
    reply_id = models.ForeignKey('Reply', on_delete=models.CASCADE, to_field='reply_id')
    account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reply_id', 'account_id'], name='unique_collect')   # 一个账号对一个消息只能收藏一次
        ]


# class Answer(models.Model):  # 回复
#     answer_id = models.AutoField(primary_key=True)
#     topic_id = models.ForeignKey('Topic', on_delete=models.CASCADE, to_field='topic_id')
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
#     content = models.TextField()  # 内容
#     create_time = models.DateTimeField()  # 创建时间，用以排序。一般从最新的信息到较老的信息排序
#     legal = models.BooleanField()
#     up_vote_count = models.IntegerField()
#     down_vote_count = models.IntegerField()
#
#
# class AnswerUpVote(models.Model):
#     answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE, to_field='answer_id')
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
#
#
# class AnswerDownVote(models.Model):
#     answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE, to_field='answer_id')
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
#
#
# class AnswerCollection(models.Model):
#     answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE, to_field='answer_id')
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')


# class TopicPicture(models.Model):
 # topic_id = models.ForeignKey('Topic', on_delete=models.CASCADE, to_field='id')
    # image = models.FileField(upload_to=topic_directory_path)
  # image = models.CharField(max_length=5000)


# class Comment(models.Model):  # 评论，这个比较难搞
#     # comment_id表示该回复自己的id
#     # master_id表示父消息id，可以指向一个Topic代表外层回复；可以指向一个Comment代表嵌套回复；父id被删除则级联删除
#     comment_id = models.AutoField(primary_key=True)
#     answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE, to_field='answer_id')
#     master_id = models.ForeignKey('Comment', on_delete=models.CASCADE, to_field='comment_id')  # 注意，外键可以为空
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
#     content = models.TextField()  # 内容
#     create_time = models.DateTimeField()  # 创建时间，用以排序。一般从最新的信息到较老的信息排序
#     legal = models.BooleanField()
#     up_vote_count = models.IntegerField()
#     down_vote_count = models.IntegerField()
#
#
# class CommentUpVote(models.Model):
#     comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE, to_field='comment_id')
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
#
#
# class CommentDownVote(models.Model):
#     comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE, to_field='comment_id')
#     account_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')


class Remind(models.Model): # 提醒管理统一格式为：被提醒者、发生时间、提醒内容三部分，具体细分种类由提醒内容决定
    # 分好多种类，待完成。
    remind_id = models.AutoField(primary_key=True)
    receiver_id = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')  # 被提醒者
    create_time = models.DateTimeField(default=timezone.now)
    content = models.TextField()


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    # 当被举报话题被删除时置空，表示被举报话题已不存在
    message_id = models.ForeignKey('Id', on_delete=models.SET_NULL, null=True, to_field='id')
    reporter = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='account_id')
    reason = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    SUCCESS = 'success'
    FAILURE = 'failure'
    PENDING = 'pending'
    REPORT_STATUS = [
        (SUCCESS, '举报成功'),
        (FAILURE, '举报驳回'),
        (PENDING, '正在处理'),
    ]
    status = models.CharField(max_length=10, choices=REPORT_STATUS, default=PENDING)
