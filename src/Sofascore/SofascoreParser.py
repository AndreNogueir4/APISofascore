from requests import Response


class SofascoreParser:
    def _json(self, response: Response):
        if response is None or response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def _text(self, response: Response):
        if response is None or response.status_code == 404:
            return None
        response.raise_for_status()
        return response.text

    def _key(self, response: Response, key: str):
        data = self._json(response)
        return data.get(key) if data is not None else None

    def parse_home_page(self, response: Response):
        return self._text(response)

    def parse_country_alpha(self, response: Response):
        return self._json(response)

    def parse_country_sport_priorities(self, response: Response):
        return self._key(response, 'countrySportPriorities')

    def parse_country_sport_priorities_by_country(self, response: Response):
        return self._key(response, 'countrySportPriorities')

    def parse_popular_entities(self, response: Response):
        return self._json(response)

    def parse_sport_event_count(self, response: Response):
        return self._json(response)

    def parse_branding_providers(self, response: Response):
        return self._key(response, 'config')

    def parse_sport_categories_all(self, response: Response):
        return self._key(response, 'categories')

    def parse_sport_categories(self, response: Response):
        return self._key(response, 'categories')

    def parse_sport_categories_by_date(self, response: Response):
        return self._key(response, 'categories')

    def parse_sport_live_categories(self, response: Response):
        return self._key(response, 'liveCategories')

    def parse_category_unique_tournaments(self, response: Response):
        return self._json(response)

    def parse_category_unique_tournament_event_count(self, response: Response):
        return self._json(response)

    def parse_category_live_unique_tournaments(self, response: Response):
        return self._json(response)

    def parse_category_scheduled_events(self, response: Response):
        return self._key(response, 'events')

    def parse_sport_live_tournaments(self, response: Response):
        return self._key(response, 'liveTournaments')

    def parse_sport_scheduled_tournaments(self, response: Response):
        return self._json(response)

    def parse_sport_mma_main_events(self, response: Response):
        return self._key(response, 'events')

    def parse_sport_trending_top_players(self, response: Response):
        return self._key(response, 'topPlayers')

    def parse_seo_content_sport(self, response: Response):
        return self._key(response, 'content')

    def parse_default_unique_tournaments(self, response: Response):
        return self._key(response, 'uniqueTournaments')

    def parse_top_unique_tournaments(self, response: Response):
        return self._key(response, 'uniqueTournaments')

    def parse_trending_events(self, response: Response):
        return self._key(response, 'events')

    def parse_newly_added_events(self, response: Response):
        return self._key(response, 'events')

    def parse_odds_providers(self, response: Response):
        return self._key(response, 'providers')

    def parse_odds_featured_events(self, response: Response):
        return self._key(response, 'featuredEvents')

    def parse_news_posts(self, response: Response):
        return self._json(response)

    def parse_news_tournament_posts(self, response: Response):
        return self._json(response)

    def parse_news_team_posts(self, response: Response):
        return self._json(response)

    def parse_news_event_posts(self, response: Response):
        return self._json(response)

    def parse_transfers(self, response: Response):
        return self._key(response, 'transfers')

    def parse_unique_tournament(self, response: Response):
        return self._key(response, 'uniqueTournament')

    def parse_unique_tournament_seasons(self, response: Response):
        return self._key(response, 'seasons')

    def parse_unique_tournament_winners(self, response: Response):
        return self._json(response)

    def parse_unique_tournament_meta(self, response: Response):
        return self._key(response, 'meta')

    def parse_seo_content_unique_tournament(self, response: Response):
        return self._key(response, 'content')

    def parse_unique_tournament_featured_events(self, response: Response):
        return self._key(response, 'featuredEvents')

    def parse_unique_tournament_media(self, response: Response):
        return self._key(response, 'media')

    def parse_unique_tournament_scheduled_events(self, response: Response):
        return self._key(response, 'events')

    def parse_unique_tournament_main_events_next(self, response: Response):
        return self._json(response)

    def parse_unique_tournament_events_live(self, response: Response):
        return self._json(response)

    def parse_rankings_unique_tournament_summary(self, response: Response):
        return self._json(response)

    def parse_unique_tournament_months_with_events(self, response: Response):
        return self._key(response, 'monthsWithEvents')

    def parse_season_info(self, response: Response):
        return self._key(response, 'info')

    def parse_season_standings(self, response: Response):
        return self._key(response, 'standings')

    def parse_season_rounds(self, response: Response):
        return self._json(response)

    def parse_season_events_round(self, response: Response):
        return self._json(response)

    def parse_season_events_round_final(self, response: Response):
        return self._json(response)

    def parse_season_events_next(self, response: Response):
        return self._json(response)

    def parse_season_events_last(self, response: Response):
        return self._json(response)

    def parse_season_cuptrees(self, response: Response):
        return self._key(response, 'cupTrees')

    def parse_season_groups(self, response: Response):
        return self._json(response)

    def parse_season_venues(self, response: Response):
        return self._json(response)

    def parse_season_editors(self, response: Response):
        return self._json(response)

    def parse_season_power_rankings_rounds(self, response: Response):
        return self._json(response)

    def parse_season_statistics_info(self, response: Response):
        return self._json(response)

    def parse_season_player_statistics(self, response: Response):
        return self._json(response)

    def parse_season_player_statistics_types(self, response: Response):
        return self._key(response, 'types')

    def parse_season_team_statistics_types(self, response: Response):
        return self._key(response, 'types')

    def parse_season_top_players_overall(self, response: Response):
        return self._json(response)

    def parse_season_top_teams_overall(self, response: Response):
        return self._json(response)

    def parse_season_top_players_per_game(self, response: Response):
        return self._json(response)

    def parse_season_player_of_the_season(self, response: Response):
        return self._json(response)

    def parse_season_player_of_the_season_race(self, response: Response):
        return self._json(response)

    def parse_season_team_of_the_period_periods(self, response: Response):
        return self._key(response, 'periods')

    def parse_team_of_the_period(self, response: Response):
        return self._json(response)

    def parse_season_team_events_total(self, response: Response):
        return self._key(response, 'tournamentTeamEvents')

    def parse_season_team_performance_graph(self, response: Response):
        return self._key(response, 'graphData')

    def parse_tournament_standings(self, response: Response):
        return self._key(response, 'standings')

    def parse_tournament_team_events_total(self, response: Response):
        return self._key(response, 'teamEvents')

    def parse_team(self, response: Response):
        return self._json(response)

    def parse_seo_content_team(self, response: Response):
        return self._key(response, 'content')

    def parse_team_players(self, response: Response):
        return self._json(response)

    def parse_team_rankings(self, response: Response):
        return self._json(response)

    def parse_team_unique_tournaments(self, response: Response):
        return self._key(response, 'uniqueTournaments')

    def parse_team_unique_tournaments_all(self, response: Response):
        return self._key(response, 'uniqueTournaments')

    def parse_team_transfers(self, response: Response):
        return self._json(response)

    def parse_team_achievements(self, response: Response):
        return self._json(response)

    def parse_team_events_next(self, response: Response):
        return self._json(response)

    def parse_team_events_last(self, response: Response):
        return self._json(response)

    def parse_team_events_by_month(self, response: Response):
        return self._json(response)

    def parse_team_featured_event(self, response: Response):
        return self._key(response, 'featuredEvent')

    def parse_team_performance(self, response: Response):
        return self._json(response)

    def parse_team_media_summary(self, response: Response):
        return self._json(response)

    def parse_team_media_videos(self, response: Response):
        return self._key(response, 'videos')

    def parse_team_official_tweets(self, response: Response):
        return self._key(response, 'tweets')

    def parse_team_offer_banner(self, response: Response):
        return self._key(response, 'banners')

    def parse_team_standings_seasons(self, response: Response):
        return self._json(response)

    def parse_team_player_statistics_seasons(self, response: Response):
        return self._json(response)

    def parse_team_team_statistics_seasons(self, response: Response):
        return self._json(response)

    def parse_team_tournament_season_statistics(self, response: Response):
        return self._key(response, 'statistics')

    def parse_team_tournament_season_ranks(self, response: Response):
        return self._json(response)

    def parse_team_season_best_result(self, response: Response):
        return self._json(response)

    def parse_event(self, response: Response):
        return self._key(response, 'event')

    def parse_event_odds_all(self, response: Response):
        return self._json(response)

    def parse_event_odds_featured(self, response: Response):
        return self._json(response)

    def parse_event_incidents(self, response: Response):
        return self._key(response, 'incidents')

    def parse_event_h2h(self, response: Response):
        return self._json(response)

    def parse_event_h2h_events(self, response: Response):
        return self._key(response, 'events')

    def parse_event_pregame_form(self, response: Response):
        return self._json(response)

    def parse_event_tv_channels(self, response: Response):
        return self._key(response, 'countryChannels')

    def parse_event_votes(self, response: Response):
        return self._json(response)

    def parse_event_graph_sequence(self, response: Response):
        return self._key(response, 'graphPoints')

    def parse_event_graph_win_probability(self, response: Response):
        return self._json(response)

    def parse_event_statistics(self, response: Response):
        return self._json(response)

    def parse_event_lineups(self, response: Response):
        return self._json(response)

    def parse_event_highlights(self, response: Response):
        return self._json(response)

    def parse_event_sport_video_highlights(self, response: Response):
        return self._json(response)

    def parse_event_official_tweets(self, response: Response):
        return self._key(response, 'tweets')

    def parse_event_at_bats(self, response: Response):
        return self._json(response)

    def parse_event_live_match_tracker(self, response: Response):
        return self._json(response)

    def parse_event_media_summary(self, response: Response):
        return self._json(response)

    def parse_translation_description(self, response: Response):
        return self._key(response, 'translation')

    def parse_next_data_home(self, response: Response):
        return self._key(response, 'pageProps')

    def parse_next_data_sport(self, response: Response):
        return self._key(response, 'pageProps')

    def parse_next_data_sport_category(self, response: Response):
        return self._key(response, 'pageProps')

    def parse_next_data_tournament(self, response: Response):
        return self._key(response, 'pageProps')

    def parse_next_data_team(self, response: Response):
        return self._key(response, 'pageProps')
