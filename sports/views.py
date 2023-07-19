from django.shortcuts import render, redirect,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GameInfo, UnoverInfo, TypeInfo,ScoreInfo
from decimal import Decimal as dcm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
@csrf_exempt
def get_checkbox(request):
    print('aaaaaaaaaaaaaaaaaaaaaaaaa')
    if request.GET:
        print(request.GET)
        query_dict = dict(request.GET)
        req_type = query_dict['request_type']
        sport_name = query_dict['sport_name'][0].lower()
        if not 'ch' in query_dict:
            print(sport_name)
            type_list = TypeInfo.objects.filter(sport_name=sport_name).values()
            score_list = ScoreInfo.objects.filter(sport_name=sport_name).all().values()
            print('score_list:', score_list)
            score_set = set()
            for score_info in score_list:
                score_set.add(dcm(score_info['score']))
            score_list = list(score_set)
            score_list.sort()
            return render(request, 'sports/sports_detail.html', {'type_list': type_list, 'sport_name': sport_name, 'score_list': score_list})
        ch = query_dict['ch']
        print('--------')
        print(req_type)
        print(ch)
        print('---------')
        if req_type[0] == '배당 조회':
            win_odds = float(query_dict['win_odds'][0])
            tie_odds = float(query_dict['tie_odds'][0])
            lose_odds = float(query_dict['lose_odds'][0])
            gap_odds = float(query_dict['gap_odds'][0])
            ignore_tie = False
            if tie_odds == 0:
                ignore_tie = True
            value_list = []
            for info in ch:
                print('info:',info)
                inf = info.split('%')
                country = inf[0]
                print('country:',country)
                league = inf[1]
                print('league:',league)
                if ignore_tie:
                    value = list(GameInfo.objects.filter(
                        country_name=country,
                        league_name=league,
                        home_away_win__gte=win_odds - gap_odds,
                        home_away_win__lte=win_odds + gap_odds,
                        home_away_lose__gte=lose_odds - gap_odds,
                        home_away_lose__lte=lose_odds + gap_odds,
                    ).values())
                else:
                    value = list(GameInfo.objects.filter(
                        country_name=country,
                        league_name=league,
                        home_away_win__gte=win_odds - gap_odds,
                        home_away_win__lte=win_odds + gap_odds,
                        home_away_lose__gte=lose_odds - gap_odds,
                        home_away_lose__lte=lose_odds + gap_odds,
                        home_away_tie__gte = tie_odds - gap_odds,
                        home_away_tie__lte = tie_odds + gap_odds,
                    ).values())
                value_list.extend(value)
            print('value_list:',value_list)
            total_win = 0
            total_tie = 0
            total_lose = 0
            for result in value_list:
                if result['betting_result'] == 'home':
                    total_win +=1
                elif result['betting_result'] == 'tie':
                    total_tie += 1
                elif result['betting_result'] == 'away':
                    total_lose += 1
            total_added = total_win+total_tie+total_lose
            percent_win = 0
            percent_tie = 0
            percent_lose = 0
            if total_added != 0:
                percent_win = total_win/total_added*100
                percent_tie = total_tie / total_added * 100
                percent_lose = total_lose / total_added * 100
            result_dict = {'win':f"{total_win}({percent_win:.1f}%)",'tie':f"{total_tie}({percent_tie:.1f}%)",'lose':f"{total_lose}({percent_lose:.1f}%)"}
            return render(request, 'sports/odds_result.html', {'total': result_dict,'result_list':value_list})
        elif req_type[0] == '언오버 조회':
            over = float(query_dict['over_unover'][0])
            score = query_dict['score'][0]
            under = float(query_dict['under_unover'][0])
            unover_gap = float(query_dict['gap_unover'][0])
            value_list = []
            for info in ch:
                print('info:', info)
                inf = info.split('%')
                country = inf[0]
                print('country:', country)
                league = inf[1]
                print('league:', league)
                value = list(UnoverInfo.objects.filter(
                    country_name=country,
                    league_name=league,
                    score=score,
                    over__gte=over - unover_gap,
                    over__lte=over + unover_gap,
                    under__gte=under - unover_gap,
                    under__lte=under + unover_gap,
                ).values())
                value_list.extend(value)
            total_searched = len(value_list)
            total_under = 0
            total_over = 0
            total_target = 0
            added_game_score = 0
            for result in value_list:
                if result['unover_result'] == 'under':
                    total_under +=1
                elif result['unover_result'] == 'over':
                    total_over += 1
                elif result['unover_result'] == 'target':
                    total_target += 1
                added_game_score += result['game_score']
            total_added = total_under + total_over + total_target
            percent_under = 0
            percent_over = 0
            percent_target = 0
            if total_added != 0:
                percent_under = total_under / total_added * 100
                percent_over = total_over / total_added * 100
                percent_target = total_target / total_added * 100
            input_dict = {'over':over, 'score':score, 'under':under}
            avg_game_score = f'{added_game_score/total_searched:.2f}'
            result_dict = {'over': f"{total_over}({percent_over:.1f}%)", 'target': f"{total_target}({percent_target:.1f}%)", 'under': f"{total_under}({percent_under:.1f}%)"}
            return render(request, 'sports/unover_result.html', {'total': result_dict,'input':input_dict, 'total_searched': total_searched,'avg_game_score':avg_game_score})

    type_list = TypeInfo.objects.all().values()
    sport_name_list = list(set([x['sport_name'][0].upper() + x['sport_name'][1:] for x in type_list]))
    return render(request, 'sports/sports_index.html', {'sport_name_list': sport_name_list})

def detail(request,sport_name):
    sport_name=sport_name.lower()
    type_list = TypeInfo.objects.filter(sport_name=sport_name).values()
    score_list = ScoreInfo.objects.filter(sport_name=sport_name).all().values()
    print('score_list:',score_list)
    score_set = set()
    for score_info in score_list:
        score_set.add(dcm(score_info['score']))
    score_list = list(score_set)
    score_list.sort()
    return render(request, 'sports/sports_detail.html', {'type_list':type_list,'sport_name':sport_name,'score_list':score_list})

def index(request):
    type_list = TypeInfo.objects.all().values()
    print(type_list)
    sport_name_list = list(set([x['sport_name'][0].upper()+x['sport_name'][1:] for x in type_list]))
    # for i in type_list:
    #     value_list.append(i.values())
    print(sport_name_list)


    return render(request, 'sports/sports_index.html',{'sport_name_list':sport_name_list})


class Upload(APIView):
    def post(self, request):
        sport_name = request.data.get('sport_name', '')
        country_name = request.data.get('country_name', '')
        league_name = request.data.get('league_name', '')
        game_time = request.data.get('game_time', '')
        betting_result = request.data.get('betting_result', '')
        home = request.data.get('home', '')
        home_count = request.data.get('home_count', None)
        away = request.data.get('away', '')
        away_count = request.data.get('away_count', None)
        home_away_win = request.data.get('home_away_win', '')
        home_away_tie = request.data.get('home_away_tie', '')
        home_away_lose = request.data.get('home_away_lose', '')

        unover_info = request.data.get('unover_info', {})

        unique_key = sport_name + country_name + league_name + home + away + game_time

        type_info = TypeInfo.objects.filter(sport_name=sport_name,country_name=country_name,league_name=league_name).first()
        if type_info is None:
            TypeInfo.objects.create(
                sport_name=sport_name,
                country_name=country_name,
                league_name=league_name,
            )

        game_info = GameInfo.objects.filter(unique_key=unique_key).first()
        if game_info is None:
            GameInfo.objects.create(
                unique_key=unique_key,
                sport_name=sport_name,
                country_name=country_name,
                league_name=league_name,
                game_time=game_time,
                betting_result=betting_result,
                home=home,
                home_count=home_count,
                away=away,
                away_count=away_count,
                home_away_win=home_away_win,
                home_away_tie=home_away_tie,
                home_away_lose=home_away_lose,
            )

        for score,unover_dict in unover_info.items():
            under = unover_dict['under']
            over = unover_dict['over']
            unique_key = sport_name + country_name + league_name + score + home + away + game_time

            score_info = ScoreInfo.objects.filter(sport_name=sport_name,country_name=country_name,league_name=league_name,score=score).first()
            if score_info is None:
                ScoreInfo.objects.create(
                    sport_name=sport_name,
                    country_name=country_name,
                    league_name=league_name,
                    score=score,
                )

            unover_info = UnoverInfo.objects.filter(unique_key=unique_key).first()

            if unover_info is None:
                game_score = dcm(home_count) + dcm(away_count)
                unover_result='unknown'
                if dcm(score) > game_score:
                    unover_result = 'under'
                elif dcm(score) < game_score:
                    unover_result = 'over'
                elif dcm(score) == game_score:
                    unover_result = 'target'
                UnoverInfo.objects.create(
                    unique_key=unique_key,
                    sport_name=sport_name,
                    country_name=country_name,
                    league_name=league_name,
                    game_score=int(game_score),
                    score=score,
                    over=over,
                    under=under,
                    unover_result=unover_result,
                )
        success_dict = {'success':True}
        return Response(data=success_dict)
