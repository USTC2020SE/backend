from django.urls import path
from rest_framework import routers
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="接口文档",
        default_version='v1',
        license=openapi.License(name="BSD License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r'docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'login/', Login.as_view()),
    path(r'signup/', Signup.as_view()),
    path(r'info/', getUserInfo.as_view()),
    # path(r'^infou/(?P<account_id>\d+)/$', updateUserInfo.as_view()),
    path(r'topic/', getTopic.as_view()),
    # path(r'topicu/', updateTopic.as_view()),
    path(r'reply/', getReply.as_view()),
    path(r'replyc/', createReply.as_view()),
    # path(r'replyu/', updateReply.as_view()),
    path(r'remind/', getRemind.as_view()),
    path(r'remindc/', createRemind.as_view()),
    path(r'msgs/', getMsgsFromUser.as_view()),
    path(r'focususer/', getFocusFromUser.as_view()),
    path(r'focususerc/', createFocusFromUser.as_view()),
    path(r'collect/', collectReply.as_view()),
    path(r'c1/', createCategory1.as_view()),
    path(r'c2/', createCategory2.as_view()),
    path(r'userremind/', getRemindFromUser.as_view()),
    path(r'category/', getCategory.as_view()),
    path(r'categorytopic/', getTopicFromCategory.as_view()),
    path(r'topicc/', createTopic.as_view()),
    path(r'focusc/', createFocusFromTopic.as_view()),
    path(r'reportc/', createReportFromMsg.as_view()),
    path(r'attitude/', createAttitudeFromMsg.as_view()),
    path(r'msgreply/', getReplyFromMsg.as_view()),
    path(r'reportdeal/', dealReport.as_view()),
    path(r'super/', Super.as_view())
]

router = routers.DefaultRouter()
router.register('infou', updateUserInfo)
router.register('topicu', updateTopic)
router.register('replyu', updateReply)
urlpatterns += router.urls
