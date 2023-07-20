from django.db import models

# Create your models here.
class AutoUser(models.Model):
    user_id = models.CharField(max_length=30, unique = True, null=False, default='')
    user_pw = models.CharField(max_length=30, null=False, default='')
    name = models.CharField(verbose_name="이름", max_length=20, null=False, default='type users name')
    phone = models.CharField(max_length=255, null=False, default='010-1111-1111')
    class Meta:
        db_table = 'login_user'
        verbose_name = 'Auto'