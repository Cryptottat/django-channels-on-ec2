from django.contrib import admin

# Register your models here.
from .models import GameInfo, UnoverInfo, TypeInfo, ScoreInfo

class AdminGameInfo(admin.ModelAdmin):
    model = GameInfo
    list_display = (

        'sport_name',
        'country_name',
        'league_name',
        'game_time',
        'betting_result',
        'home',
        'home_count',
        'away',
        'away_count',
        'home_away_win',
        'home_away_tie',
        'home_away_lose',
        'unique_key',
    )


# Register your models here.
admin.site.register(GameInfo, AdminGameInfo)


class AdminUnoverInfo(admin.ModelAdmin):
    model = UnoverInfo
    list_display = (
        'sport_name',
        'country_name',
        'league_name',
        'game_score',
        'score',
        'over',
        'under',
        'unover_result',
        'unique_key',
    )


# Register your models here.
admin.site.register(UnoverInfo, AdminUnoverInfo)

class AdminTypeInfo(admin.ModelAdmin):
    model = TypeInfo
    list_display = (
        'sport_name',
        'country_name',
        'league_name',
    )


# Register your models here.
admin.site.register(TypeInfo, AdminTypeInfo)

class AdminScoreInfo(admin.ModelAdmin):
    model = ScoreInfo
    list_display = (
        'sport_name',
        'country_name',
        'league_name',
        'score',
    )


# Register your models here.
admin.site.register(ScoreInfo, AdminScoreInfo)
