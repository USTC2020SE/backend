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
]

router = routers.DefaultRouter()

router.register('account', AccountView)
router.register('msgid', MessageIdView)
router.register('topic', TopicView)
router.register('topicpic', TopicPictureView)
router.register('comment', CommentView)
router.register('report', ReportView)

urlpatterns += router.urls
