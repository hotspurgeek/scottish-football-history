from django.contrib import admin
from .models import (
    DataSource, Venue, Team, Competition, Season, Referee, Player,
    Manager, TeamManager, PlayerClubHistory, Transfer, InternationalCap,
    Match, Lineup, Goal, LeagueStanding
)

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'reliability_score', 'created_at']
    search_fields = ['name']
    list_filter = ['reliability_score']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'capacity', 'opened_year']
    search_fields = ['name', 'city']
    list_filter = ['country']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'founded_year', 'home_venue']
    search_fields = ['name', 'city']
    list_filter = ['country', 'founded_year']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'country', 'started_year']
    search_fields = ['name']
    list_filter = ['type', 'country']


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['season_year', 'competition', 'start_date', 'end_date']
    search_fields = ['season_year']
    list_filter = ['competition', 'season_year']


@admin.register(Referee)
class RefereeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'nationality', 'birth_year']
    search_fields = ['first_name', 'last_name']
    list_filter = ['nationality']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'nationality', 'position', 'birth_date']
    search_fields = ['first_name', 'last_name']
    list_filter = ['position', 'nationality', 'birth_date']


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'nationality', 'birth_year']
    search_fields = ['first_name', 'last_name']
    list_filter = ['nationality']


@admin.register(TeamManager)
class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ['manager', 'team', 'start_date', 'end_date', 'total_matches']
    search_fields = ['manager__last_name', 'team__name']
    list_filter = ['team', 'start_date']


@admin.register(PlayerClubHistory)
class PlayerClubHistoryAdmin(admin.ModelAdmin):
    list_display = ['player', 'club', 'join_date', 'leave_date', 'appearances', 'goals']
    search_fields = ['player__last_name', 'club__name']
    list_filter = ['club', 'join_date']


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['player', 'from_club', 'to_club', 'transfer_date', 'fee_amount']
    search_fields = ['player__last_name', 'from_club__name', 'to_club__name']
    list_filter = ['transfer_date', 'to_club']


@admin.register(InternationalCap)
class InternationalCapAdmin(admin.ModelAdmin):
    list_display = ['player', 'country', 'caps', 'goals', 'first_cap_date']
    search_fields = ['player__last_name', 'country']
    list_filter = ['country']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_date', 'home_team', 'away_team', 'home_goals', 'away_goals', 'competition']
    search_fields = ['home_team__name', 'away_team__name']
    list_filter = ['match_date', 'competition', 'season']
    date_hierarchy = 'match_date'


@admin.register(Lineup)
class LineupAdmin(admin.ModelAdmin):
    list_display = ['player', 'match', 'team', 'shirt_number', 'position', 'is_starter']
    search_fields = ['player__last_name', 'match__home_team__name']
    list_filter = ['match', 'is_starter', 'position']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['player', 'match', 'goal_time', 'goal_type', 'assisted_by']
    search_fields = ['player__last_name', 'match__home_team__name']
    list_filter = ['goal_type', 'match__match_date']


@admin.register(LeagueStanding)
class LeagueStandingAdmin(admin.ModelAdmin):
    list_display = ['season', 'position', 'team', 'played', 'wins', 'draws', 'losses', 'points']
    search_fields = ['team__name', 'season__season_year']
    list_filter = ['season', 'position']
