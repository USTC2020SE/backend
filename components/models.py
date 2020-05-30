from django.db import models

# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<id>/<filename>
    return 'users/{0}/{1}'.format(instance.id, filename)


def topic_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/topics/<id>/<filename>
    return 'topics/{0}/{1}'.format(instance.topic_id, filename)


class Account(models.Model):
    id = models.AutoField(primary_key=True)     # 账户ID(PK)
    nickname = models.CharField(max_length=15)  # 账户昵称
    # avatar = models.ImageField(upload_to=user_directory_path)    # 头像 - 目录储存方式
    # background = models.ImageField(upload_to=user_directory_path)    # 背景图片 - 目录储存方式
    avatar = models.CharField(max_length=500)   # 头像 - base64储存方式
    background = models.CharField(max_length=1000) # 背景图片 - bas64储存方式
    signature = models.CharField(max_length=50) # 签名
    NORMAL = 'normal'
    SUPER = 'super'
    ACCOUNT_TYPE = [
        (NORMAL, '普通用户'),
        (SUPER, '管理用户'),
    ]
    type = models.CharField(max_length=10, default=NORMAL, choices=ACCOUNT_TYPE)


class MessageId(models.Model):
    id = models.AutoField(primary_key=True)     # 所有话题、回复、内层回复的统一ID


class Topic(models.Model):
    id = models.OneToOneField('MessageId', on_delete=models.CASCADE, to_field='id', primary_key=True)     # 话题ID(PK)
    sender = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='id')  # 发送者
    content = models.TextField()                # 内容
    create_time = models.DateTimeField()        # 创建时间
    anonymity = models.BooleanField()           # 匿名性
    expire_time = models.DateTimeField(blank=True)  # 过期时间
    category = models.PositiveIntegerField()    # 话题分类
    tags = models.BigIntegerField()             # 话题标签，请使用一个整数表示该话题的所有标签，最长64位


class TopicPicture(models.Model):
    topic_id = models.ForeignKey('Topic', on_delete=models.CASCADE, to_field='id')
    # image = models.FileField(upload_to=topic_directory_path)
    image = models.CharField(max_length=5000)


class Comment(models.Model):
    # comment_id表示该回复自己的id
    # master_id表示父消息id，可以指向一个Topic代表外层回复；可以指向一个Comment代表嵌套回复；父id被删除则级联删除
    comment_id = models.OneToOneField('MessageId', on_delete=models.CASCADE, to_field='id', primary_key=True, related_name='comment_id')
    master_id = models.ForeignKey('MessageId', on_delete=models.CASCADE, to_field='id', related_name='master_id')
    sender = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='id')
    content = models.TextField()
    anonymity = models.BooleanField()


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    # 当被举报话题被删除时置空，表示被举报话题已不存在
    message_id = models.ForeignKey('MessageId', on_delete=models.SET_NULL, null=True, to_field='id')
    reporter = models.ForeignKey('Account', on_delete=models.CASCADE, to_field='id')
    reason = models.TextField()
    time = models.DateTimeField()
    SUCCESS = 'success'
    FAILURE = 'failure'
    PENDING = 'pending'
    REPORT_STATUS = [
        (SUCCESS, '举报成功'),
        (FAILURE, '举报驳回'),
        (PENDING, '正在处理'),
    ]
    status = models.CharField(max_length=10, choices=REPORT_STATUS, default=PENDING)
