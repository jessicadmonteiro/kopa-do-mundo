from rest_framework.views import APIView
from rest_framework.response import Response
from teams.models import Team
from django.forms.models import model_to_dict
from teams.exceptions import (
    NegativeTitlesError,
    InvalidYearCupError,
    ImpossibleTitlesError
)
from teams.utils import data_processing


class TeamView(APIView):
    def post(self, request):
        team_data = request.data

        try:
            data_processing(team_data)
        except NegativeTitlesError as error:
            return Response(
                {"error": error.message}, 400
            )
        except InvalidYearCupError as error:
            return Response(
                {"error": error.message}, 400
            )
        except ImpossibleTitlesError as error:
            return Response(
                {"error": error.message}, 400
            )

        team = Team.objects.create(**team_data)
        return Response(model_to_dict(team), 201)

    def get(self, request):
        teams = Team.objects.all()
        teams_dict = []

        for team in teams:
            t = model_to_dict(team)
            teams_dict.append(t)

        return Response(teams_dict, 200)
