from rest_framework import serializers
from .models import (
    DataSource, Venue, Team, Competition, Season, Referee, Player,
    Manager, TeamManager, PlayerClubHistory, Transfer, InternationalCap,
    Match, Lineup, Goal, LeagueStanding
)


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'description', 'reliability_score', 'created_at']


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'city', 'country', 'capacity', 'opened_year', 'closed_year', 'notes']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'founded_year', 'dissolved_year', 'city', 'country', 'home_venue', 'historical_names', 'notes']


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['id', 'name', 'type', 'country', 'started_year', 'notes']


class SeasonSerializer(serializers.ModelSerializer):
    competition_name = serializers.CharField(source='competition.name', read_only=True)

    class Meta:
        model = Season
        fields = ['id', 'season_year', 'start_date', 'end_date', 'competition', 'competition_name', 'number_of_matches', 'notes']


class RefereeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referee
        fields = ['id', 'first_name', 'last_name', 'birth_year', 'death_year', 'nationality', 'notes']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'death_date', 'nationality', 'position', 'height_cm', 'preferred_foot', 'notes']


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'first_name', 'last_name', 'birth_year', 'death_year', 'nationality']


class TeamManagerSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.__str__', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = TeamManager
        fields = ['id', 'team', 'team_name', 'manager', 'manager_name', 'start_date', 'end_date', 'total_matches', 'wins', 'draws', 'losses', 'notes']


class PlayerClubHistorySerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.__str__', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)

    class Meta:
        model = PlayerClubHistory
        fields = ['id', 'player', 'player_name', 'club', 'club_name', 'join_date', 'leave_date', 'shirt_number', 'appearances', 'goals', 'assists', 'notes']


class TransferSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.__str__', read_only=True)
    from_club_name = serializers.CharField(source='from_club.name', read_only=True)
    to_club_name = serializers.CharField(source='to_club.name', read_only=True)

    class Meta:
        model = Transfer
        fields = ['id', 'player', 'player_name', 'from_club', 'from_club_name', 'to_club', 'to_club_name', 'transfer_date', 'fee_amount', 'fee_currency', 'notes']


class InternationalCapSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.__str__', read_only=True)

    class Meta:
        model = InternationalCap
        fields = ['id', 'player', 'player_name', 'country', 'caps', 'goals', 'first_cap_date', 'last_cap_date', 'notes']


class GoalSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.__str__', read_only=True)
    assisted_by_name = serializers.CharField(source='assisted_by.__str__', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Goal
        fields = ['id', 'match', 'player', 'player_name', 'team', 'team_name', 'goal_time', 'goal_type', 'assisted_by', 'assisted_by_name', 'own_goal', 'notes']


class LineupSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.__str__', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Lineup
        fields = ['id', 'match', 'player', 'player_name', 'team', 'team_name', 'shirt_number', 'position', 'is_starter', 'minutes_played', 'goals', 'assists', 'yellow_cards', 'red_cards', 'notes']


class MatchDetailSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    season_year = serializers.CharField(source='season.season_year', read_only=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    referee_name = serializers.CharField(source='referee.__str__', read_only=True)
    goals = GoalSerializer(many=True, read_only=True)
    lineups = LineupSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = [
            'id', 'season', 'season_year', 'competition', 'competition_name', 'match_date', 'match_time',
            'home_team', 'home_team_name', 'away_team', 'away_team_name', 'home_goals', 'away_goals',
            'venue', 'venue_name', 'attendance', 'referee', 'referee_name', 'weather_conditions', 'notes', 'goals', 'lineups'
        ]


class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)
    competition_name = serializers.CharField(source='competition.name', read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'match_date', 'home_team', 'home_team_name', 'away_team', 'away_team_name', 'home_goals', 'away_goals', 'competition', 'competition_name']


class LeagueStandingSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    season_year = serializers.CharField(source='season.season_year', read_only=True)

    class Meta:
        model = LeagueStanding
        fields = ['id', 'season', 'season_year', 'team', 'team_name', 'position', 'played', 'wins', 'draws', 'losses', 'goals_for', 'goals_against', 'goal_difference', 'points', 'notes']


class PlayerDetailSerializer(serializers.ModelSerializer):
    club_history = PlayerClubHistorySerializer(many=True, read_only=True)
    transfers = TransferSerializer(many=True, read_only=True)
    international_caps = InternationalCapSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'death_date', 'nationality', 'position', 'height_cm', 'preferred_foot', 'notes', 'club_history', 'transfers', 'international_caps']
