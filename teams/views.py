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
        except (NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError) as error:
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


class TeamParamView(APIView):
    def get(sef, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, 404
            )

        team_dic = model_to_dict(team)
        return Response(team_dic, 200)

    def patch(sef, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, 404
            )

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)

        return Response(team_dict, 200)

    def delete(sef, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, 404
            )

        team.delete()

        return Response(status=204)
