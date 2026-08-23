from src.Common.NetworkManager import NetworkManager
from src.Sofascore.SofascoreParser import SofascoreParser
from src.Sofascore.SofascoreRequestFactory import SofascoreRequestFactory


class SofascoreCrawler:

    def __init__(self, factory: SofascoreRequestFactory, parser: SofascoreParser):
        self._factory = factory
        self._parser = parser

    def home_page(self, session: NetworkManager, lang: str = 'pt'):
        response = self._factory.build_home_page(session, lang)
        return self._parser.parse_home_page(response)

    def country_alpha(self, session: NetworkManager):
        response = self._factory.build_country_alpha(session)
        return self._parser.parse_country_alpha(response)

    def country_sport_priorities(self, session: NetworkManager):
        response = self._factory.build_country_sport_priorities(session)
        return self._parser.parse_country_sport_priorities(response)

    def country_sport_priorities_by_country(self, session: NetworkManager, country: str):
        response = self._factory.build_country_sport_priorities_by_country(session, country)
        return self._parser.parse_country_sport_priorities_by_country(response)

    def popular_entities(self, session: NetworkManager, country: str):
        response = self._factory.build_popular_entities(session, country)
        return self._parser.parse_popular_entities(response)

    def sport_event_count(self, session: NetworkManager, timezone_offset: int = -10800):
        response = self._factory.build_sport_event_count(session, timezone_offset)
        return self._parser.parse_sport_event_count(response)

    def branding_providers(self, session: NetworkManager, country: str, platform: str = 'web'):
        response = self._factory.build_branding_providers(session, country, platform)
        return self._parser.parse_branding_providers(response)

    def sport_categories_all(self, session: NetworkManager, sport: str):
        response = self._factory.build_sport_categories_all(session, sport)
        return self._parser.parse_sport_categories_all(response)

    def sport_categories(self, session: NetworkManager, sport: str):
        response = self._factory.build_sport_categories(session, sport)
        return self._parser.parse_sport_categories(response)

    def sport_categories_by_date(self, session: NetworkManager, sport: str, date: str,
                                  timezone_offset: int = -10800):
        response = self._factory.build_sport_categories_by_date(session, sport, date, timezone_offset)
        return self._parser.parse_sport_categories_by_date(response)

    def sport_live_categories(self, session: NetworkManager, sport: str):
        response = self._factory.build_sport_live_categories(session, sport)
        return self._parser.parse_sport_live_categories(response)

    def category_unique_tournaments(self, session: NetworkManager, category_id):
        response = self._factory.build_category_unique_tournaments(session, category_id)
        return self._parser.parse_category_unique_tournaments(response)

    def category_unique_tournament_event_count(self, session: NetworkManager, category_id, date: str,
                                                timezone_offset: int = -10800):
        response = self._factory.build_category_unique_tournament_event_count(
            session, category_id, date, timezone_offset)
        return self._parser.parse_category_unique_tournament_event_count(response)

    def category_live_unique_tournaments(self, session: NetworkManager, category_id):
        response = self._factory.build_category_live_unique_tournaments(session, category_id)
        return self._parser.parse_category_live_unique_tournaments(response)

    def category_scheduled_events(self, session: NetworkManager, category_id, date: str):
        response = self._factory.build_category_scheduled_events(session, category_id, date)
        return self._parser.parse_category_scheduled_events(response)

    def sport_live_tournaments(self, session: NetworkManager, sport: str):
        response = self._factory.build_sport_live_tournaments(session, sport)
        return self._parser.parse_sport_live_tournaments(response)

    def sport_scheduled_tournaments(self, session: NetworkManager, sport: str, date: str, page: int):
        response = self._factory.build_sport_scheduled_tournaments(session, sport, date, page)
        return self._parser.parse_sport_scheduled_tournaments(response)

    def sport_mma_main_events(self, session: NetworkManager, date: str):
        response = self._factory.build_sport_mma_main_events(session, date)
        return self._parser.parse_sport_mma_main_events(response)

    def sport_trending_top_players(self, session: NetworkManager, sport: str):
        response = self._factory.build_sport_trending_top_players(session, sport)
        return self._parser.parse_sport_trending_top_players(response)

    def seo_content_sport(self, session: NetworkManager, sport: str, lang: str = 'pt'):
        response = self._factory.build_seo_content_sport(session, sport, lang)
        return self._parser.parse_seo_content_sport(response)

    def default_unique_tournaments(self, session: NetworkManager, country: str, sport: str):
        response = self._factory.build_default_unique_tournaments(session, country, sport)
        return self._parser.parse_default_unique_tournaments(response)

    def top_unique_tournaments(self, session: NetworkManager, country: str, sport: str):
        response = self._factory.build_top_unique_tournaments(session, country, sport)
        return self._parser.parse_top_unique_tournaments(response)

    def trending_events(self, session: NetworkManager, country: str, sport: str = 'all'):
        response = self._factory.build_trending_events(session, country, sport)
        return self._parser.parse_trending_events(response)

    def newly_added_events(self, session: NetworkManager):
        response = self._factory.build_newly_added_events(session)
        return self._parser.parse_newly_added_events(response)

    def odds_providers(self, session: NetworkManager, country: str, context: str = 'web'):
        response = self._factory.build_odds_providers(session, country, context)
        return self._parser.parse_odds_providers(response)

    def odds_featured_events(self, session: NetworkManager, provider_id, sport: str):
        response = self._factory.build_odds_featured_events(session, provider_id, sport)
        return self._parser.parse_odds_featured_events(response)

    def news_posts(self, session: NetworkManager, lang: str = 'pt', page: int = 1, per_page: int = 12,
                    categories: str = 'sport-pt'):
        response = self._factory.build_news_posts(session, lang, page, per_page, categories)
        return self._parser.parse_news_posts(response)

    def news_tournament_posts(self, session: NetworkManager, tournament_id, page: int = 1, lang: str = 'pt'):
        response = self._factory.build_news_tournament_posts(session, tournament_id, page, lang)
        return self._parser.parse_news_tournament_posts(response)

    def news_team_posts(self, session: NetworkManager, team_id, page: int = 1, lang: str = 'pt'):
        response = self._factory.build_news_team_posts(session, team_id, page, lang)
        return self._parser.parse_news_team_posts(response)

    def news_event_posts(self, session: NetworkManager, event_id, page: int = 1, lang: str = 'pt'):
        response = self._factory.build_news_event_posts(session, event_id, page, lang)
        return self._parser.parse_news_event_posts(response)

    def transfers(self, session: NetworkManager, page: int = 1, sort: str = '-transferFee'):
        response = self._factory.build_transfers(session, page, sort)
        return self._parser.parse_transfers(response)

    def unique_tournament(self, session: NetworkManager, unique_tournament_id):
        response = self._factory.build_unique_tournament(session, unique_tournament_id)
        return self._parser.parse_unique_tournament(response)

    def unique_tournament_seasons(self, session: NetworkManager, unique_tournament_id):
        response = self._factory.build_unique_tournament_seasons(session, unique_tournament_id)
        return self._parser.parse_unique_tournament_seasons(response)

    def unique_tournament_winners(self, session: NetworkManager, unique_tournament_id):
        response = self._factory.build_unique_tournament_winners(session, unique_tournament_id)
        return self._parser.parse_unique_tournament_winners(response)

    def unique_tournament_meta(self, session: NetworkManager, unique_tournament_id):
        response = self._factory.build_unique_tournament_meta(session, unique_tournament_id)
        return self._parser.parse_unique_tournament_meta(response)

    def seo_content_unique_tournament(self, session: NetworkManager, unique_tournament_id, lang: str = 'pt'):
        response = self._factory.build_seo_content_unique_tournament(session, unique_tournament_id, lang)
        return self._parser.parse_seo_content_unique_tournament(response)

    def unique_tournament_featured_events(self, session: NetworkManager, unique_tournament_id):
        response = self._factory.build_unique_tournament_featured_events(session, unique_tournament_id)
        return self._parser.parse_unique_tournament_featured_events(response)

    def unique_tournament_media(self, session: NetworkManager, unique_tournament_id):
        response = self._factory.build_unique_tournament_media(session, unique_tournament_id)
        return self._parser.parse_unique_tournament_media(response)

    def unique_tournament_scheduled_events(self, session: NetworkManager, unique_tournament_id, date: str):
        response = self._factory.build_unique_tournament_scheduled_events(session, unique_tournament_id, date)
        return self._parser.parse_unique_tournament_scheduled_events(response)

    def unique_tournament_main_events_next(self, session: NetworkManager, unique_tournament_id, page: int = 0):
        response = self._factory.build_unique_tournament_main_events_next(session, unique_tournament_id, page)
        return self._parser.parse_unique_tournament_main_events_next(response)

    def unique_tournament_events_live(self, session: NetworkManager, unique_tournament_id, page: int = 0):
        response = self._factory.build_unique_tournament_events_live(session, unique_tournament_id, page)
        return self._parser.parse_unique_tournament_events_live(response)

    def rankings_unique_tournament_summary(self, session: NetworkManager, unique_tournament_id):
        response = self._factory.build_rankings_unique_tournament_summary(session, unique_tournament_id)
        return self._parser.parse_rankings_unique_tournament_summary(response)

    def unique_tournament_months_with_events(self, session: NetworkManager, unique_tournament_id,
                                              timezone_offset: int = -10800):
        response = self._factory.build_unique_tournament_months_with_events(
            session, unique_tournament_id, timezone_offset)
        return self._parser.parse_unique_tournament_months_with_events(response)

    def season_info(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_info(session, unique_tournament_id, season_id)
        return self._parser.parse_season_info(response)

    def season_standings(self, session: NetworkManager, unique_tournament_id, season_id, kind: str = 'total'):
        response = self._factory.build_season_standings(session, unique_tournament_id, season_id, kind)
        return self._parser.parse_season_standings(response)

    def season_rounds(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_rounds(session, unique_tournament_id, season_id)
        return self._parser.parse_season_rounds(response)

    def season_events_round(self, session: NetworkManager, unique_tournament_id, season_id, round_):
        response = self._factory.build_season_events_round(session, unique_tournament_id, season_id, round_)
        return self._parser.parse_season_events_round(response)

    def season_events_round_final(self, session: NetworkManager, unique_tournament_id, season_id, round_):
        response = self._factory.build_season_events_round_final(session, unique_tournament_id, season_id, round_)
        return self._parser.parse_season_events_round_final(response)

    def season_events_next(self, session: NetworkManager, unique_tournament_id, season_id, page: int = 0):
        response = self._factory.build_season_events_next(session, unique_tournament_id, season_id, page)
        return self._parser.parse_season_events_next(response)

    def season_events_last(self, session: NetworkManager, unique_tournament_id, season_id, page: int = 0):
        response = self._factory.build_season_events_last(session, unique_tournament_id, season_id, page)
        return self._parser.parse_season_events_last(response)

    def season_cuptrees(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_cuptrees(session, unique_tournament_id, season_id)
        return self._parser.parse_season_cuptrees(response)

    def season_groups(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_groups(session, unique_tournament_id, season_id)
        return self._parser.parse_season_groups(response)

    def season_venues(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_venues(session, unique_tournament_id, season_id)
        return self._parser.parse_season_venues(response)

    def season_editors(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_editors(session, unique_tournament_id, season_id)
        return self._parser.parse_season_editors(response)

    def season_power_rankings_rounds(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_power_rankings_rounds(session, unique_tournament_id, season_id)
        return self._parser.parse_season_power_rankings_rounds(response)

    def season_statistics_info(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_statistics_info(session, unique_tournament_id, season_id)
        return self._parser.parse_season_statistics_info(response)

    def season_player_statistics(self, session: NetworkManager, unique_tournament_id, season_id, limit: int = 20,
                                  order: str = '-rating', accumulation: str = 'total', group: str = 'summary'):
        response = self._factory.build_season_player_statistics(
            session, unique_tournament_id, season_id, limit, order, accumulation, group)
        return self._parser.parse_season_player_statistics(response)

    def season_player_statistics_types(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_player_statistics_types(session, unique_tournament_id, season_id)
        return self._parser.parse_season_player_statistics_types(response)

    def season_team_statistics_types(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_team_statistics_types(session, unique_tournament_id, season_id)
        return self._parser.parse_season_team_statistics_types(response)

    def season_top_players_overall(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_top_players_overall(session, unique_tournament_id, season_id)
        return self._parser.parse_season_top_players_overall(response)

    def season_top_teams_overall(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_top_teams_overall(session, unique_tournament_id, season_id)
        return self._parser.parse_season_top_teams_overall(response)

    def season_top_players_per_game(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_top_players_per_game(session, unique_tournament_id, season_id)
        return self._parser.parse_season_top_players_per_game(response)

    def season_player_of_the_season(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_player_of_the_season(session, unique_tournament_id, season_id)
        return self._parser.parse_season_player_of_the_season(response)

    def season_player_of_the_season_race(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_player_of_the_season_race(session, unique_tournament_id, season_id)
        return self._parser.parse_season_player_of_the_season_race(response)

    def season_team_of_the_period_periods(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_team_of_the_period_periods(session, unique_tournament_id, season_id)
        return self._parser.parse_season_team_of_the_period_periods(response)

    def team_of_the_period(self, session: NetworkManager, period_id):
        response = self._factory.build_team_of_the_period(session, period_id)
        return self._parser.parse_team_of_the_period(response)

    def season_team_events_total(self, session: NetworkManager, unique_tournament_id, season_id):
        response = self._factory.build_season_team_events_total(session, unique_tournament_id, season_id)
        return self._parser.parse_season_team_events_total(response)

    def season_team_performance_graph(self, session: NetworkManager, unique_tournament_id, season_id, team_id):
        response = self._factory.build_season_team_performance_graph(
            session, unique_tournament_id, season_id, team_id)
        return self._parser.parse_season_team_performance_graph(response)

    def tournament_standings(self, session: NetworkManager, tournament_id, season_id, kind: str = 'total'):
        response = self._factory.build_tournament_standings(session, tournament_id, season_id, kind)
        return self._parser.parse_tournament_standings(response)

    def tournament_team_events_total(self, session: NetworkManager, tournament_id, season_id):
        response = self._factory.build_tournament_team_events_total(session, tournament_id, season_id)
        return self._parser.parse_tournament_team_events_total(response)

    def team(self, session: NetworkManager, team_id):
        response = self._factory.build_team(session, team_id)
        return self._parser.parse_team(response)

    def seo_content_team(self, session: NetworkManager, team_id, lang: str = 'pt'):
        response = self._factory.build_seo_content_team(session, team_id, lang)
        return self._parser.parse_seo_content_team(response)

    def team_players(self, session: NetworkManager, team_id):
        response = self._factory.build_team_players(session, team_id)
        return self._parser.parse_team_players(response)

    def team_rankings(self, session: NetworkManager, team_id):
        response = self._factory.build_team_rankings(session, team_id)
        return self._parser.parse_team_rankings(response)

    def team_unique_tournaments(self, session: NetworkManager, team_id):
        response = self._factory.build_team_unique_tournaments(session, team_id)
        return self._parser.parse_team_unique_tournaments(response)

    def team_unique_tournaments_all(self, session: NetworkManager, team_id):
        response = self._factory.build_team_unique_tournaments_all(session, team_id)
        return self._parser.parse_team_unique_tournaments_all(response)

    def team_transfers(self, session: NetworkManager, team_id):
        response = self._factory.build_team_transfers(session, team_id)
        return self._parser.parse_team_transfers(response)

    def team_achievements(self, session: NetworkManager, team_id):
        response = self._factory.build_team_achievements(session, team_id)
        return self._parser.parse_team_achievements(response)

    def team_events_next(self, session: NetworkManager, team_id, page: int = 0):
        response = self._factory.build_team_events_next(session, team_id, page)
        return self._parser.parse_team_events_next(response)

    def team_events_last(self, session: NetworkManager, team_id, page: int = 0):
        response = self._factory.build_team_events_last(session, team_id, page)
        return self._parser.parse_team_events_last(response)

    def team_events_by_month(self, session: NetworkManager, team_id, month: str, year: str):
        response = self._factory.build_team_events_by_month(session, team_id, month, year)
        return self._parser.parse_team_events_by_month(response)

    def team_featured_event(self, session: NetworkManager, team_id):
        response = self._factory.build_team_featured_event(session, team_id)
        return self._parser.parse_team_featured_event(response)

    def team_performance(self, session: NetworkManager, team_id):
        response = self._factory.build_team_performance(session, team_id)
        return self._parser.parse_team_performance(response)

    def team_media_summary(self, session: NetworkManager, team_id, country: str = 'BR'):
        response = self._factory.build_team_media_summary(session, team_id, country)
        return self._parser.parse_team_media_summary(response)

    def team_media_videos(self, session: NetworkManager, team_id):
        response = self._factory.build_team_media_videos(session, team_id)
        return self._parser.parse_team_media_videos(response)

    def team_official_tweets(self, session: NetworkManager, team_id):
        response = self._factory.build_team_official_tweets(session, team_id)
        return self._parser.parse_team_official_tweets(response)

    def team_offer_banner(self, session: NetworkManager, team_id, country: str = 'BR', lang: str = 'pt'):
        response = self._factory.build_team_offer_banner(session, team_id, country, lang)
        return self._parser.parse_team_offer_banner(response)

    def team_standings_seasons(self, session: NetworkManager, team_id):
        response = self._factory.build_team_standings_seasons(session, team_id)
        return self._parser.parse_team_standings_seasons(response)

    def team_player_statistics_seasons(self, session: NetworkManager, team_id):
        response = self._factory.build_team_player_statistics_seasons(session, team_id)
        return self._parser.parse_team_player_statistics_seasons(response)

    def team_team_statistics_seasons(self, session: NetworkManager, team_id):
        response = self._factory.build_team_team_statistics_seasons(session, team_id)
        return self._parser.parse_team_team_statistics_seasons(response)

    def team_tournament_season_statistics(self, session: NetworkManager, team_id, unique_tournament_id, season_id):
        response = self._factory.build_team_tournament_season_statistics(
            session, team_id, unique_tournament_id, season_id)
        return self._parser.parse_team_tournament_season_statistics(response)

    def team_tournament_season_ranks(self, session: NetworkManager, team_id, unique_tournament_id, season_id):
        response = self._factory.build_team_tournament_season_ranks(
            session, team_id, unique_tournament_id, season_id)
        return self._parser.parse_team_tournament_season_ranks(response)

    def team_season_best_result(self, session: NetworkManager, team_id, season_id):
        response = self._factory.build_team_season_best_result(session, team_id, season_id)
        return self._parser.parse_team_season_best_result(response)

    def event(self, session: NetworkManager, event_id):
        response = self._factory.build_event(session, event_id)
        return self._parser.parse_event(response)

    def event_odds_all(self, session: NetworkManager, event_id, provider_id=1):
        response = self._factory.build_event_odds_all(session, event_id, provider_id)
        return self._parser.parse_event_odds_all(response)

    def event_odds_featured(self, session: NetworkManager, event_id, provider_id=100):
        response = self._factory.build_event_odds_featured(session, event_id, provider_id)
        return self._parser.parse_event_odds_featured(response)

    def event_incidents(self, session: NetworkManager, event_id):
        response = self._factory.build_event_incidents(session, event_id)
        return self._parser.parse_event_incidents(response)

    def event_h2h(self, session: NetworkManager, event_id):
        response = self._factory.build_event_h2h(session, event_id)
        return self._parser.parse_event_h2h(response)

    def event_h2h_events(self, session: NetworkManager, event_id):
        response = self._factory.build_event_h2h_events(session, event_id)
        return self._parser.parse_event_h2h_events(response)

    def event_pregame_form(self, session: NetworkManager, event_id):
        response = self._factory.build_event_pregame_form(session, event_id)
        return self._parser.parse_event_pregame_form(response)

    def event_tv_channels(self, session: NetworkManager, event_id):
        response = self._factory.build_event_tv_channels(session, event_id)
        return self._parser.parse_event_tv_channels(response)

    def event_votes(self, session: NetworkManager, event_id):
        response = self._factory.build_event_votes(session, event_id)
        return self._parser.parse_event_votes(response)

    def event_graph_sequence(self, session: NetworkManager, event_id):
        response = self._factory.build_event_graph_sequence(session, event_id)
        return self._parser.parse_event_graph_sequence(response)

    def event_graph_win_probability(self, session: NetworkManager, event_id):
        response = self._factory.build_event_graph_win_probability(session, event_id)
        return self._parser.parse_event_graph_win_probability(response)

    def event_statistics(self, session: NetworkManager, event_id):
        response = self._factory.build_event_statistics(session, event_id)
        return self._parser.parse_event_statistics(response)

    def event_lineups(self, session: NetworkManager, event_id):
        response = self._factory.build_event_lineups(session, event_id)
        return self._parser.parse_event_lineups(response)

    def event_highlights(self, session: NetworkManager, event_id):
        response = self._factory.build_event_highlights(session, event_id)
        return self._parser.parse_event_highlights(response)

    def event_sport_video_highlights(self, session: NetworkManager, event_id, country: str = 'BR'):
        response = self._factory.build_event_sport_video_highlights(session, event_id, country)
        return self._parser.parse_event_sport_video_highlights(response)

    def event_official_tweets(self, session: NetworkManager, event_id):
        response = self._factory.build_event_official_tweets(session, event_id)
        return self._parser.parse_event_official_tweets(response)

    def event_at_bats(self, session: NetworkManager, event_id):
        response = self._factory.build_event_at_bats(session, event_id)
        return self._parser.parse_event_at_bats(response)

    def event_live_match_tracker(self, session: NetworkManager, event_id):
        response = self._factory.build_event_live_match_tracker(session, event_id)
        return self._parser.parse_event_live_match_tracker(response)

    def event_media_summary(self, session: NetworkManager, event_id, country: str = 'BR'):
        response = self._factory.build_event_media_summary(session, event_id, country)
        return self._parser.parse_event_media_summary(response)

    def translation_description(self, session: NetworkManager, resource_id, lang: str = 'pt'):
        response = self._factory.build_translation_description(session, resource_id, lang)
        return self._parser.parse_translation_description(response)

    def next_data_home(self, session: NetworkManager, lang: str = 'pt'):
        response = self._factory.build_next_data_home(session, lang)
        return self._parser.parse_next_data_home(response)

    def next_data_sport(self, session: NetworkManager, sport: str, lang: str = 'pt'):
        response = self._factory.build_next_data_sport(session, sport, lang)
        return self._parser.parse_next_data_sport(response)

    def next_data_sport_category(self, session: NetworkManager, sport: str, category_slug: str, lang: str = 'pt'):
        response = self._factory.build_next_data_sport_category(session, sport, category_slug, lang)
        return self._parser.parse_next_data_sport_category(response)

    def next_data_tournament(self, session: NetworkManager, sport: str, category_slug: str, tournament_slug: str,
                              unique_tournament_id, lang: str = 'pt'):
        response = self._factory.build_next_data_tournament(
            session, sport, category_slug, tournament_slug, unique_tournament_id, lang)
        return self._parser.parse_next_data_tournament(response)

    def next_data_team(self, session: NetworkManager, sport: str, team_slug: str, team_id, lang: str = 'pt'):
        response = self._factory.build_next_data_team(session, sport, team_slug, team_id, lang)
        return self._parser.parse_next_data_team(response)
