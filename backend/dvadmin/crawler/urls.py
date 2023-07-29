from rest_framework import routers
from dvadmin.crawler.views.invitation_code import InvitationCodeModelViewSet
from dvadmin.crawler.views.order import OrderModelViewSet
from dvadmin.crawler.views.register_user import RegisterUserModelViewSet
from dvadmin.crawler.views.shop import ShopModelViewSet
from dvadmin.crawler.views.shop_comments import ShopCommentsModelViewSet
from dvadmin.crawler.views.sub_msg_config import SubMsgConfigModelViewSet
from dvadmin.crawler.views.system_var import SystemVarModelViewSet
from dvadmin.crawler.views.normal_session import NormalSessionModelViewSet
from dvadmin.crawler.views.business_session import BusinessSessionModelViewSet

system_url = routers.SimpleRouter()
system_url.register(r'invitation_code', InvitationCodeModelViewSet)
system_url.register(r'register_user', RegisterUserModelViewSet)
system_url.register(r'shop', ShopModelViewSet)
system_url.register(r'system_var', SystemVarModelViewSet)
system_url.register(r'shop_comments', ShopCommentsModelViewSet)
system_url.register(r'normal_session', NormalSessionModelViewSet)
system_url.register(r'business_session', BusinessSessionModelViewSet)
system_url.register(r'sub_msg_config', SubMsgConfigModelViewSet)
system_url.register(r'order', OrderModelViewSet)

urlpatterns = [
]
urlpatterns += system_url.urls
