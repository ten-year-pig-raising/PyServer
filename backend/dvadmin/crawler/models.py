from django.db import models

from dvadmin.system.models import Users
# Create your models here.
from dvadmin.utils.models import CoreModel


# 邀请码model
class InvitationCodeModel(CoreModel):
    code = models.CharField(max_length=255, verbose_name="邀请码")
    # user = models.ForeignKey(to=Users,
    #                          verbose_name="所属用户",
    #                          on_delete=models.PROTECT,
    #                          db_constraint=False,
    #                          null=True,
    #                          blank=True,
    #                          help_text="关联部门用户", )
    code_type = models.CharField(max_length=255, verbose_name="邀请码类型")
    valid_start_time = models.DateTimeField(verbose_name="开始生效时间")
    valid_end_time = models.DateTimeField(verbose_name="结束生效时间")

    class Meta:
        db_table = "invitation_code"
        verbose_name = '邀请码'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


# 注册用户
class RegisterUserModel(CoreModel):
    alias_name = models.CharField(max_length=255, verbose_name="别名", help_text="别名", null=True,
                                  blank=True)
    username = models.CharField(max_length=255, verbose_name="姓名", help_text="姓名", null=True,
                                blank=True)
    telephone = models.CharField(max_length=255, verbose_name="手机号", help_text="手机号", null=True,
                                 blank=True)
    avatar = models.CharField(max_length=255, verbose_name="头像照片地址", help_text="头像照片地址", null=True,
                              blank=True)
    union_id = models.CharField(max_length=255, verbose_name="微信unionId", help_text="微信unionId", null=True,
                                blank=True)
    openid = models.CharField(max_length=255, verbose_name="微信openid", help_text="微信openid", null=True,
                              blank=True)

    class Meta:
        db_table = "bz_register_user"
        verbose_name = '注册用户'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


# 商铺
class ShopModel(CoreModel):
    shop_name = models.CharField(max_length=255, verbose_name="商铺名称", help_text="商铺名称", null=True,
                                 blank=True)
    shop_code = models.CharField(max_length=255, verbose_name="商铺ID", help_text="商铺ID")
    login_name = models.CharField(max_length=255, verbose_name="登录账户", help_text="登录账户", null=True,
                                  blank=True)
    password = models.CharField(max_length=255, verbose_name="登录密码", help_text="登录密码", null=True,
                                blank=True)
    login_phone = models.CharField(max_length=255, verbose_name="登录手机号", help_text="登录手机号", null=True,
                                   blank=True)
    verification_code = models.CharField(max_length=255, verbose_name="验证码", help_text="验证码", null=True,
                                         blank=True)
    login_type = models.CharField(max_length=255, verbose_name="登录类型", help_text="登录类型", null=True,
                                  blank=True)
    is_bind = models.BooleanField(verbose_name="是否绑定", help_text="是否绑定", null=True,
                                  blank=True)
    shop_type = models.CharField(max_length=100, verbose_name="商铺类型", help_text="商铺类型")
    front_img = models.CharField(max_length=1000, verbose_name="商铺图片", help_text="商铺图片", null=True,
                                 blank=True)
    shop_addr = models.CharField(max_length=255, verbose_name="商家地址", help_text="商家地址", null=True,
                                 blank=True)
    shop_score = models.FloatField(max_length=10, verbose_name="店铺评分", help_text="店铺评分", null=True)
    invitation_code = models.CharField(max_length=255, verbose_name="邀请码", help_text="邀请码", null=True, blank=True)
    inviter = models.ForeignKey(to=Users, related_query_name='inviter', related_name='inviter', null=True,
                                verbose_name='邀请人', help_text="邀请人", on_delete=models.SET_NULL,
                                db_constraint=False)
    register_user = models.ForeignKey(to=RegisterUserModel, related_query_name='register_user', null=True,
                                      verbose_name='所属用户', help_text="所属用户", on_delete=models.SET_NULL,
                                      db_constraint=False)
    shipping_time = models.CharField(max_length=255, verbose_name="配送时间", help_text="配送时间", null=True,
                                     blank=True)
    service_end_time = models.DateTimeField(verbose_name="服务到期时间", help_text="服务到期时间", null=True,
                                            blank=True)
    delivery_start_time = models.DateTimeField(verbose_name="开始配送时间", help_text="开始配送时间", null=True,
                                               blank=True)
    delivery_end_time = models.DateTimeField(verbose_name="结束配送时间", help_text="结束配送时间", null=True,
                                             blank=True)

    session_cookie = models.TextField(max_length=5000, verbose_name="账号cookie", help_text="账号cookie", null=True,
                                      blank=True)
    session_order = models.TextField(max_length=2000, verbose_name="订单参数", help_text="订单参数", null=True,
                                     blank=True)
    session_comment = models.TextField(max_length=1000, verbose_name="评论参数", help_text="评论参数", null=True,
                                       blank=True)

    session_expired = models.BooleanField(verbose_name="session是否过期", help_text="session是否过期", null=True,
                                          blank=True)

    last_order_md5 = models.CharField(max_length=100, verbose_name="上一次订单", help_text="上一次订单", null=True,
                                      blank=True)
    last_comment_md5 = models.CharField(max_length=100, verbose_name="上一次评价", help_text="上一次评价", null=True,
                                        blank=True)

    class Meta:
        db_table = "bz_shop"
        verbose_name = '商铺'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class ShopServiceModel(CoreModel):
    service_name = models.CharField(max_length=255, verbose_name="服务名称", help_text="服务名称", null=True,
                                    blank=True)
    service_code = models.CharField(max_length=255, verbose_name="服务code", help_text="服务code", null=True,
                                    blank=True)
    is_open = models.BooleanField(verbose_name="是否开启", help_text="是否开启")
    record = models.FloatField(max_length=10, verbose_name="记录", help_text="记录", null=True,
                               blank=True)
    service_config = models.TextField(max_length=5000, verbose_name="服务配置信息", help_text="服务配置信息", null=True,
                                      blank=True)
    shop = models.ForeignKey(to=ShopModel, related_query_name='shop', related_name='shop', null=True,
                             verbose_name='邀请人', help_text="邀请人", on_delete=models.CASCADE,
                             db_constraint=False)

    class Meta:
        db_table = "bz_shop_service"
        verbose_name = '商铺功能'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class SystemVarModel(models.Model):
    # group = models.CharField(max_length=500, verbose_name="组", help_text="组")
    key = models.CharField(max_length=500, verbose_name="key", help_text="key")
    value = models.CharField(max_length=5000, verbose_name="值", help_text="值")
    expires_time = models.DateTimeField(max_length=5000, verbose_name="过期时间", help_text="过期时间", null=True)

    class Meta:
        db_table = "bz_system_var"
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name


class ShopCommentModel(models.Model):
    rate_id = models.CharField(max_length=100, verbose_name="评价订单ID", help_text="评价订单ID", null=True, blank=True)
    order_id = models.CharField(max_length=100, verbose_name="订单ID", help_text="订单ID", null=True, blank=True)
    user_name = models.CharField(max_length=100, verbose_name="评价人名称", help_text="评价人名称", null=True,
                                 blank=True)
    comment_time = models.DateTimeField(verbose_name="评价时间", help_text="评价时间", null=True, blank=True)
    score = models.CharField(max_length=500, verbose_name="评分", help_text="评分", null=True, blank=True)
    content = models.CharField(max_length=500, verbose_name="评价内容", help_text="评价内容", null=True, blank=True)
    shop_reply_content = models.CharField(max_length=500, verbose_name="商家回复内容", help_text="商家回复内容",
                                          null=True, blank=True)

    shop_id = models.ForeignKey(to=ShopModel, related_query_name='c_shop_id', related_name='c_shop_id', null=True,
                                verbose_name='邀请人', help_text="邀请人", on_delete=models.SET_NULL,
                                db_constraint=False)
    shop_type = models.CharField(max_length=100, verbose_name="店铺类型", help_text="店铺类型", null=True, blank=True)
    shop_name = models.CharField(max_length=100, verbose_name="店铺名称", help_text="店铺名称", null=True,
                                 blank=True)

    class Meta:
        db_table = "bz_shop_comment"
        verbose_name = '店铺评价'
        verbose_name_plural = verbose_name


class NormalSessionModel(CoreModel):
    phone_number = models.CharField(max_length=100, verbose_name="手机号", help_text="手机号", null=True, blank=True)
    shop_type = models.CharField(max_length=100, verbose_name="店铺类型", help_text="店铺类型", null=True, blank=True)
    cookie = models.TextField(max_length=5000, verbose_name="cookie", help_text="cookie", null=True, blank=True)
    cookie_expires_in = models.DateTimeField(verbose_name="cookie过期时间", help_text="cookie过期时间", null=True,
                                             blank=True)

    class Meta:
        db_table = "bz_normal_session"
        verbose_name = '个人账号session信息'
        verbose_name_plural = verbose_name


class BusinessSessionModel(CoreModel):
    shop_code = models.CharField(max_length=100, verbose_name="店铺Code", help_text="店铺Code", null=True, blank=True)
    shop_type = models.CharField(max_length=100, verbose_name="店铺类型", help_text="店铺类型", null=True, blank=True)

    session_cookie = models.TextField(max_length=5000, verbose_name="账号cookie", help_text="账号cookie", null=True,
                                      blank=True)
    session_order = models.TextField(max_length=2000, verbose_name="订单参数", help_text="订单参数", null=True,
                                     blank=True)
    session_comment = models.TextField(max_length=1000, verbose_name="评论参数", help_text="评论参数", null=True,
                                       blank=True)
    session_expires_in = models.DateTimeField(verbose_name="session过期时间", help_text="session过期时间", null=True,
                                              blank=True)

    last_order_md5 = models.CharField(max_length=100, verbose_name="上一次订单", help_text="上一次订单", null=True,
                                      blank=True)
    last_comment_md5 = models.CharField(max_length=100, verbose_name="上一次评价", help_text="上一次评价", null=True,
                                        blank=True)

    # BusinessSession

    class Meta:
        db_table = "bz_business_session"
        verbose_name = '商家账号session信息'
        verbose_name_plural = verbose_name


class SubMsgConfigModel(CoreModel):
    sub_times = models.IntegerField(verbose_name="订阅次数", help_text="订阅次数", null=True, blank=True)
    register_user = models.ForeignKey(to=RegisterUserModel, related_query_name='register_user', null=True,
                                      verbose_name='所属用户', help_text="所属用户", on_delete=models.SET_NULL,
                                      db_constraint=False)

    class Meta:
        db_table = "bz_sub_msg_config"
        verbose_name = '用户订阅一次性消息配置'
        verbose_name_plural = verbose_name


class OrderModel(CoreModel):
    shop_code = models.CharField(max_length=100, verbose_name="店铺Code", help_text="店铺Code", null=True, blank=True)
    shop_type = models.CharField(max_length=100, verbose_name="店铺类型", help_text="店铺类型", null=True, blank=True)

    order_seq_id = models.CharField(max_length=100, verbose_name="订单序列号ID", help_text="订单序列号ID", null=True,
                                    blank=True)  # 订间的序列号ID, 表示是今天的第几单
    order_id = models.CharField(max_length=100, verbose_name="订单ID", help_text="订单ID", null=True,
                                blank=True)  # 订单ID

    order_time = models.DateTimeField(verbose_name="订单下单时间", help_text="订单下单时间", null=True,
                                      blank=True)  # 订单下单时间
    arrival_time = models.TextField(max_length=100, verbose_name="订单预计到达时间", help_text="订单预计到达时间",
                                    null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name="订单地址", help_text="订单地址", null=True, blank=True)

    recipient_name = models.CharField(max_length=100, verbose_name="顾客名", help_text="顾客名", null=True, blank=True)
    privacy_phone = models.CharField(max_length=100, verbose_name="隐私号码", help_text="隐私号码", null=True,
                                     blank=True)
    backup_privacy_phones = models.CharField(max_length=100, verbose_name="备用隐私号码", help_text="备用隐私号码",
                                             null=True, blank=True)
    recipient_phone = models.CharField(max_length=100, verbose_name="顾客电话", help_text="顾客电话", null=True,
                                       blank=True)

    menu_json = models.TextField(max_length=2000, verbose_name="菜单", help_text="菜单", null=True,
                                 blank=True)  # json格式:

    settle_json = models.TextField(max_length=2000, verbose_name="结算信息", help_text="结算信息", null=True,
                                   blank=True)  # json格式:

    class Meta:
        db_table = "bz_order"
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name
