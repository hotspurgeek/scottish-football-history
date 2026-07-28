from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .pagination import StandardPagination
from .models import (
    DataSource, Venue, Team, Competition, Season, Referee, Player,
    Manager, TeamManager, PlayerClubHistory, Transfer, InternationalCap,
    Match, Lineup, Goal, LeagueStanding
)
from .serializers import (
    DataSourceSerializer, VenueSerializer, TeamSerializer, CompetitionSerializer,
    SeasonSerializer, RefereeSerializer, PlayerSerializer, ManagerSerializer,
    TeamManagerSerializer, PlayerClubHistorySerializer, TransferSerializer,
    InternationalCapSerializer, MatchSerializer, MatchDetailSerializer,
    LineupSerializer, GoalSerializer, LeagueStandingSerializer, PlayerDetailSerializer
)


class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    search_fields = ['name', 'city']
    filter_backends = [filters.SearchFilter]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    search_fields = ['name', 'city']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['country']
    pagination_class = StandardPagination


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    search_fields = ['name']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['type', 'country']


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    search_fields = ['season_year']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['competition', 'season_year']


class RefereeViewSet(viewsets.ModelViewSet):
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer
    search_fields = ['first_name', 'last_name']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['nationality']


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    search_fields = ['first_name', 'last_name']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['position', 'nationality']
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlayerDetailSerializer
        return PlayerSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    search_fields = ['first_name', 'last_name']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['nationality']


class TeamManagerViewSet(viewsets.ModelViewSet):
    queryset = TeamManager.objects.all()
    serializer_class = TeamManagerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team', 'manager']


class PlayerClubHistoryViewSet(viewsets.ModelViewSet):
    queryset = PlayerClubHistory.objects.all()
    serializer_class = PlayerClubHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['player', 'club']


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['player', 'from_club', 'to_club']
    pagination_class = StandardPagination


class InternationalCapViewSet(viewsets.ModelViewSet):
    queryset = InternationalCap.objects.all()
    serializer_class = InternationalCapSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['player', 'country']


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related('home_team', 'away_team', 'competition', 'season', 'venue', 'referee')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['home_team', 'away_team', 'competition', 'season', 'match_date']
    ordering_fields = ['match_date']
    ordering = ['-match_date']
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MatchDetailSerializer
        return MatchSerializer

    @action(detail=False, methods=['get'])
    def by_teams(self, request):
        """Get all matches between two specific teams"""
        team1_id = request.query_params.get('team1')
        team2_id = request.query_params.get('team2')
        
        if not team1_id or not team2_id:
            return Response({"error": "team1 and team2 parameters required"})
        
        matches = Match.objects.filter(
            (models.Q(home_team_id=team1_id) & models.Q(away_team_id=team2_id)) |
            (models.Q(home_team_id=team2_id) & models.Q(away_team_id=team1_id))
        ).order_by('-match_date')
        
        serializer = MatchDetailSerializer(matches, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_player(self, request):
        """Get all matches featuring a specific player"""
        player_id = request.query_params.get('player_id')
        
        if not player_id:
            return Response({"error": "player_id parameter required"})
        
        matches = Match.objects.filter(lineups__player_id=player_id).distinct().order_by('-match_date')
        serializer = MatchDetailSerializer(matches, many=True)
        return Response(serializer.data)


class LineupViewSet(viewsets.ModelViewSet):
    queryset = Lineup.objects.all()
    serializer_class = LineupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['match', 'player', 'team']


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['match', 'player', 'team']


class LeagueStandingViewSet(viewsets.ModelViewSet):
    queryset = LeagueStanding.objects.all()
    serializer_class = LeagueStandingSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['season', 'team']
    ordering_fields = ['position']
    ordering = ['position']
