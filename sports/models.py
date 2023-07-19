from django.db import models

# Create your models here.

class TypeInfo(models.Model):
    sport_name = models.CharField(max_length=20, null=False)
    country_name = models.CharField(max_length=20, null=False)
    league_name = models.CharField(max_length=20, null=False)

class ScoreInfo(models.Model):
    sport_name = models.CharField(max_length=20, null=False)
    country_name = models.CharField(max_length=20, null=False)
    league_name = models.CharField(max_length=20, null=False)
    score = models.CharField(max_length=20, null=False)


class GameInfo(models.Model):
    unique_key = models.CharField(max_length=200, null=False,unique=True)
    sport_name = models.CharField(max_length=20, null=False)
    country_name = models.CharField(max_length=20, null=False)
    league_name = models.CharField(max_length=20, null=False)
    game_time = models.CharField(max_length=20, null=False)
    betting_result = models.CharField(max_length=4, null=False)
    home = models.CharField(max_length=20, null=False)
    home_count = models.IntegerField(null=True, default=None)
    away = models.CharField(max_length=20, null=False)
    away_count = models.IntegerField(null=True, default=None)
    home_away_win = models.FloatField(null=True,default=None)
    home_away_tie = models.FloatField(null=True,default=None)
    home_away_lose = models.FloatField(null=True,default=None)
    class Meta:
        db_table = 'gameinfo'
        verbose_name = '게임정보'

class UnoverInfo(models.Model):
    unique_key = models.CharField(max_length=200, null=False)
    sport_name = models.CharField(max_length=20, null=False)
    country_name = models.CharField(max_length=20, null=False)
    league_name = models.CharField(max_length=20, null=False)
    game_score = models.IntegerField(null=False, default=0)  # 홈-어웨이 골 합계
    score = models.CharField(max_length=20, null=False)  # 기준점
    over = models.FloatField(null=True, default=None)
    under = models.FloatField(null=True, default=None)
    unover_result = models.CharField(max_length=7, null=False)