from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DataSourceViewSet, VenueViewSet, TeamViewSet, CompetitionViewSet,
    SeasonViewSet, RefereeViewSet, PlayerViewSet, ManagerViewSet,
    TeamManagerViewSet, PlayerClubHistoryViewSet, TransferViewSet,
    InternationalCapViewSet, MatchViewSet, LineupViewSet, GoalViewSet,
    LeagueStandingViewSet
)

router = DefaultRouter()
router.register(r'data-sources', DataSourceViewSet)
router.register(r'venues', VenueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'competitions', CompetitionViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'referees', RefereeViewSet)
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'managers', ManagerViewSet)
router.register(r'team-managers', TeamManagerViewSet)
router.register(r'player-club-history', PlayerClubHistoryViewSet)
router.register(r'transfers', TransferViewSet)
router.register(r'international-caps', InternationalCapViewSet)
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'lineups', LineupViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'league-standings', LeagueStandingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
