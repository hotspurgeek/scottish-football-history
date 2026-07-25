from django.db import models

class DataSource(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    reliability_score = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="1-5 scale"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Venue(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    opened_year = models.IntegerField(blank=True, null=True)
    closed_year = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        ordering = ['name']


class Team(models.Model):
    name = models.CharField(max_length=255)
    founded_year = models.IntegerField(blank=True, null=True)
    dissolved_year = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    home_venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, blank=True, null=True)
    historical_names = models.TextField(blank=True, null=True, help_text="Comma-separated")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Competition(models.Model):
    COMPETITION_TYPES = [
        ('league', 'League'),
        ('cup', 'Cup'),
        ('international', 'International'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=COMPETITION_TYPES)
    country = models.CharField(max_length=100, blank=True, null=True)
    started_year = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Season(models.Model):
    season_year = models.CharField(max_length=10)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    number_of_matches = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.competition.name} {self.season_year}"

    class Meta:
        ordering = ['-season_year']
        unique_together = ['season_year', 'competition']


class Referee(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    death_year = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class Player(models.Model):
    POSITIONS = [
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward'),
        ('OTHER', 'Other'),
    ]
    FOOT = [
        ('L', 'Left'),
        ('R', 'Right'),
        ('B', 'Both'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=50, choices=POSITIONS, blank=True, null=True)
    height_cm = models.IntegerField(blank=True, null=True)
    preferred_foot = models.CharField(max_length=10, choices=FOOT, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    data_source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class Manager(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    death_year = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class TeamManager(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='managers')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    total_matches = models.IntegerField(blank=True, null=True)
    wins = models.IntegerField(blank=True, null=True)
    draws = models.IntegerField(blank=True, null=True)
    losses = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.manager} at {self.team} ({self.start_date})"

    class Meta:
        ordering = ['-start_date']


class PlayerClubHistory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='club_history')
    club = models.ForeignKey(Team, on_delete=models.CASCADE)
    join_date = models.DateField()
    leave_date = models.DateField(blank=True, null=True)
    shirt_number = models.IntegerField(blank=True, null=True)
    appearances = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} at {self.club}"

    class Meta:
        ordering = ['-join_date']


class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='transfers')
    from_club = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True, related_name='transfers_out')
    to_club = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='transfers_in')
    transfer_date = models.DateField()
    fee_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fee_currency = models.CharField(max_length=10, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    data_source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player}: {self.from_club} → {self.to_club}"

    class Meta:
        ordering = ['-transfer_date']


class InternationalCap(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='international_caps')
    country = models.CharField(max_length=100, default='Scotland')
    caps = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    first_cap_date = models.DateField(blank=True, null=True)
    last_cap_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} ({self.country})"

    class Meta:
        ordering = ['country']


class Match(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='matches')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    match_date = models.DateField()
    match_time = models.TimeField(blank=True, null=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, blank=True, null=True)
    home_goals = models.IntegerField(blank=True, null=True)
    away_goals = models.IntegerField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)
    referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, blank=True, null=True)
    weather_conditions = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    data_source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.match_date})"

    class Meta:
        ordering = ['-match_date']


class Lineup(models.Model):
    POSITIONS = [
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward'),
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='lineups')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    shirt_number = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=50, choices=POSITIONS, blank=True, null=True)
    is_starter = models.BooleanField(default=True)
    minutes_played = models.IntegerField(blank=True, null=True)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} - {self.match}"

    class Meta:
        ordering = ['shirt_number']


class Goal(models.Model):
    GOAL_TYPES = [
        ('open_play', 'Open Play'),
        ('penalty', 'Penalty'),
        ('own_goal', 'Own Goal'),
        ('free_kick', 'Free Kick'),
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='goals')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    goal_time = models.IntegerField(blank=True, null=True, help_text="Minutes")
    goal_type = models.CharField(max_length=50, choices=GOAL_TYPES, blank=True, null=True)
    assisted_by = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='assists_made')
    own_goal = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} ({self.match})"

    class Meta:
        ordering = ['goal_time']


class LeagueStanding(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='standings')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.IntegerField(blank=True, null=True)
    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team} - {self.season}"

    class Meta:
        ordering = ['position']
        unique_together = ['season', 'team']
