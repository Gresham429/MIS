import random
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone


class OrdinaryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar/', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True, null=True)
    email_verified = models.BooleanField(default=False)  # 邮箱是否已验证
    email_verification_code = models.CharField(max_length=100, blank=True, null=True)  # 邮箱验证的验证码
    email_verification_code_expiry = models.DateTimeField(blank=True, null=True)  # 邮箱验证码的过期时间
    
    class Meta:
        verbose_name_plural = "ordinaryuser"

    def send_verification_email(self, email):
        # 生成随机验证码（这里使用6位数字作为验证码）
        verification_code = ''.join(random.choices('0123456789', k=6))
        self.email_verification_code = verification_code
        print(verification_code)

        # 生成过期时间，这里设置为验证码有效期为10分钟
        self.email_verification_code_expiry = timezone.now() + timezone.timedelta(minutes=10)

        # 保存验证码信息到数据库
        self.save()

        # 发送邮件
        subject = '邮箱验证'
        message = f'您的验证码是：{verification_code}。\n请在{self.email_verification_code_expiry}内完成验证'
        from_email = '1543732388@qq.com'  # 发件人邮箱
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

    def verify_email(self, verification_code):
        # 验证验证码是否匹配并未过期
        if (self.email_verification_code == verification_code and self.email_verification_code_expiry > timezone.now()):
            self.email_verified = True
            self.save()
            return True
        return False