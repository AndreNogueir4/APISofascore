from requests import Response

from src.Common.NetworkManager import NetworkManager


class SofascoreRequestFactory:

    def __init__(self, x_requested_with: str = '2589dc', next_build_id: str = 'ht9wCJpl-6PQSlY85cZ-r'):
        self.root_url = 'https://www.sofascore.com'
        self.base_url = 'https://www.sofascore.com/api/v1'
        self.x_requested_with = x_requested_with
        self.next_build_id = next_build_id

    def _headers(self, extra: dict = None) -> dict:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'X-Requested-With': self.x_requested_with,
            'Referer': f'{self.root_url}/pt',
        }
        if extra:
            headers.update(extra)
        return headers

    def build_home_page(self, session: NetworkManager, lang: str = 'pt') -> Response:
        url = f'{self.root_url}/{lang}'
        return session.get(url, headers=self._headers())

    def build_country_alpha(self, session: NetworkManager) -> Response:
        url = f'{self.base_url}/country/alpha2'
        return session.get(url, headers=self._headers())

    def build_country_sport_priorities(self, session: NetworkManager) -> Response:
        url = f'{self.base_url}/config/country-sport-priorities/country'
        return session.get(url, headers=self._headers())

    def build_country_sport_priorities_by_country(self, session: NetworkManager, country: str) -> Response:
        url = f'{self.base_url}/config/country-sport-priorities/country/{country}'
        return session.get(url, headers=self._headers())

    def build_popular_entities(self, session: NetworkManager, country: str) -> Response:
        url = f'{self.base_url}/config/popular-entities/{country}'
        return session.get(url, headers=self._headers())

    def build_sport_event_count(self, session: NetworkManager, timezone_offset: int = -10800) -> Response:
        url = f'{self.base_url}/sport/{timezone_offset}/event-count'
        return session.get(url, headers=self._headers())

    def build_branding_providers(self, session: NetworkManager, country: str, platform: str = 'web') -> Response:
        url = f'{self.base_url}/branding/providers/{country}/{platform}'
        return session.get(url, headers=self._headers())

    def build_sport_categories_all(self, session: NetworkManager, sport: str) -> Response:
        url = f'{self.base_url}/sport/{sport}/categories/all'
        return session.get(url, headers=self._headers())

    def build_sport_categories(self, session: NetworkManager, sport: str) -> Response:
        url = f'{self.base_url}/sport/{sport}/categories'
        return session.get(url, headers=self._headers())

    def build_sport_categories_by_date(self, session: NetworkManager, sport: str, date: str,
                                        timezone_offset: int = -10800) -> Response:
        url = f'{self.base_url}/sport/{sport}/{date}/{timezone_offset}/categories'
        return session.get(url, headers=self._headers())

    def build_sport_live_categories(self, session: NetworkManager, sport: str) -> Response:
        url = f'{self.base_url}/sport/{sport}/live-categories'
        return session.get(url, headers=self._headers())

    def build_category_unique_tournaments(self, session: NetworkManager, category_id) -> Response:
        url = f'{self.base_url}/category/{category_id}/unique-tournaments'
        return session.get(url, headers=self._headers())

    def build_category_unique_tournament_event_count(self, session: NetworkManager, category_id, date: str,
                                                       timezone_offset: int = -10800) -> Response:
        url = f'{self.base_url}/category/{category_id}/{date}/{timezone_offset}/unique-tournament-event-count'
        return session.get(url, headers=self._headers())

    def build_category_live_unique_tournaments(self, session: NetworkManager, category_id) -> Response:
        url = f'{self.base_url}/category/{category_id}/live-unique-tournaments'
        return session.get(url, headers=self._headers())

    def build_category_scheduled_events(self, session: NetworkManager, category_id, date: str) -> Response:
        url = f'{self.base_url}/category/{category_id}/scheduled-events/{date}'
        return session.get(url, headers=self._headers())

    def build_sport_live_tournaments(self, session: NetworkManager, sport: str) -> Response:
        url = f'{self.base_url}/sport/{sport}/live-tournaments'
        return session.get(url, headers=self._headers())

    def build_sport_scheduled_tournaments(self, session: NetworkManager, sport: str, date: str, page: int) -> Response:
        url = f'{self.base_url}/sport/{sport}/scheduled-tournaments/{date}/page/{page}'
        return session.get(url, headers=self._headers())

    def build_sport_mma_main_events(self, session: NetworkManager, date: str) -> Response:
        url = f'{self.base_url}/sport/mma/main-events/{date}/extended'
        return session.get(url, headers=self._headers())

    def build_sport_trending_top_players(self, session: NetworkManager, sport: str) -> Response:
        url = f'{self.base_url}/sport/{sport}/trending-top-players'
        return session.get(url, headers=self._headers())

    def build_seo_content_sport(self, session: NetworkManager, sport: str, lang: str = 'pt') -> Response:
        url = f'{self.base_url}/seo/content/sport/{sport}/{lang}'
        return session.get(url, headers=self._headers())

    def build_default_unique_tournaments(self, session: NetworkManager, country: str, sport: str) -> Response:
        url = f'{self.base_url}/config/default-unique-tournaments/{country}/{sport}'
        return session.get(url, headers=self._headers())

    def build_top_unique_tournaments(self, session: NetworkManager, country: str, sport: str) -> Response:
        url = f'{self.base_url}/config/top-unique-tournaments/{country}/{sport}'
        return session.get(url, headers=self._headers())

    def build_trending_events(self, session: NetworkManager, country: str, sport: str = 'all') -> Response:
        url = f'{self.base_url}/trending/events/{country}/{sport}'
        return session.get(url, headers=self._headers())

    def build_newly_added_events(self, session: NetworkManager) -> Response:
        url = f'{self.base_url}/event/newly-added-events'
        return session.get(url, headers=self._headers())

    def build_odds_providers(self, session: NetworkManager, country: str, context: str = 'web') -> Response:
        # context: 'web' | 'web-odds' | 'web-featured'
        url = f'{self.base_url}/odds/providers/{country}/{context}'
        return session.get(url, headers=self._headers())

    def build_odds_featured_events(self, session: NetworkManager, provider_id, sport: str) -> Response:
        url = f'{self.base_url}/odds/{provider_id}/featured-events/{sport}'
        return session.get(url, headers=self._headers())

    def build_news_posts(self, session: NetworkManager, lang: str = 'pt', page: int = 1, per_page: int = 12,
                          categories: str = 'sport-pt') -> Response:
        url = f'{self.base_url}/sofascore-news/{lang}/posts'
        params = {'page': page, 'per_page': per_page, 'categories': categories}
        return session.get(url, headers=self._headers(), params=params)

    def build_news_tournament_posts(self, session: NetworkManager, tournament_id, page: int = 1,
                                     lang: str = 'pt') -> Response:
        url = f'{self.base_url}/sofascore-news/{lang}/tournament/{tournament_id}/posts/{page}'
        return session.get(url, headers=self._headers())

    def build_news_team_posts(self, session: NetworkManager, team_id, page: int = 1, lang: str = 'pt') -> Response:
        url = f'{self.base_url}/sofascore-news/{lang}/team/{team_id}/posts/{page}'
        return session.get(url, headers=self._headers())

    def build_news_event_posts(self, session: NetworkManager, event_id, page: int = 1, lang: str = 'pt') -> Response:
        url = f'{self.base_url}/sofascore-news/{lang}/event/{event_id}/posts/{page}'
        return session.get(url, headers=self._headers())

    def build_transfers(self, session: NetworkManager, page: int = 1, sort: str = '-transferFee') -> Response:
        url = f'{self.base_url}/transfer'
        params = {'page': page, 'sort': sort}
        return session.get(url, headers=self._headers(), params=params)

    def build_unique_tournament(self, session: NetworkManager, unique_tournament_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_seasons(self, session: NetworkManager, unique_tournament_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/seasons'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_winners(self, session: NetworkManager, unique_tournament_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/winners'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_meta(self, session: NetworkManager, unique_tournament_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/meta'
        return session.get(url, headers=self._headers())

    def build_seo_content_unique_tournament(self, session: NetworkManager, unique_tournament_id,
                                             lang: str = 'pt') -> Response:
        url = f'{self.base_url}/seo/content/unique-tournament/{unique_tournament_id}/{lang}'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_featured_events(self, session: NetworkManager, unique_tournament_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/featured-events'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_media(self, session: NetworkManager, unique_tournament_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/media'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_scheduled_events(self, session: NetworkManager, unique_tournament_id,
                                                  date: str) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/scheduled-events/{date}'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_main_events_next(self, session: NetworkManager, unique_tournament_id,
                                                  page: int = 0) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/main-events/next/{page}'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_events_live(self, session: NetworkManager, unique_tournament_id,
                                             page: int = 0) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/events/live/{page}'
        return session.get(url, headers=self._headers())

    def build_rankings_unique_tournament_summary(self, session: NetworkManager, unique_tournament_id) -> Response:
        url = f'{self.base_url}/rankings/unique-tournament/{unique_tournament_id}/summary'
        return session.get(url, headers=self._headers())

    def build_unique_tournament_months_with_events(self, session: NetworkManager, unique_tournament_id,
                                                    timezone_offset: int = -10800) -> Response:
        url = f'{self.base_url}/calendar/unique-tournament/{unique_tournament_id}/{timezone_offset}/months-with-events'
        return session.get(url, headers=self._headers())

    def build_season_info(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/info'
        return session.get(url, headers=self._headers())

    def build_season_standings(self, session: NetworkManager, unique_tournament_id, season_id,
                                kind: str = 'total') -> Response:
        # kind: 'total' | 'home' | 'away'
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/standings/{kind}'
        return session.get(url, headers=self._headers())

    def build_season_rounds(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/rounds'
        return session.get(url, headers=self._headers())

    def build_season_events_round(self, session: NetworkManager, unique_tournament_id, season_id, round_) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/events/round/{round_}'
        return session.get(url, headers=self._headers())

    def build_season_events_round_final(self, session: NetworkManager, unique_tournament_id, season_id,
                                         round_) -> Response:
        url = (f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}'
               f'/events/round/{round_}/slug/final')
        return session.get(url, headers=self._headers())

    def build_season_events_next(self, session: NetworkManager, unique_tournament_id, season_id,
                                  page: int = 0) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/events/next/{page}'
        return session.get(url, headers=self._headers())

    def build_season_events_last(self, session: NetworkManager, unique_tournament_id, season_id,
                                  page: int = 0) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/events/last/{page}'
        return session.get(url, headers=self._headers())

    def build_season_cuptrees(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/cuptrees'
        return session.get(url, headers=self._headers())

    def build_season_groups(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/groups'
        return session.get(url, headers=self._headers())

    def build_season_venues(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/venues'
        return session.get(url, headers=self._headers())

    def build_season_editors(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/editors'
        return session.get(url, headers=self._headers())

    def build_season_power_rankings_rounds(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/power-rankings/rounds'
        return session.get(url, headers=self._headers())

    def build_season_statistics_info(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/statistics/info'
        return session.get(url, headers=self._headers())

    def build_season_player_statistics(self, session: NetworkManager, unique_tournament_id, season_id,
                                        limit: int = 20, order: str = '-rating', accumulation: str = 'total',
                                        group: str = 'summary') -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/statistics'
        params = {'limit': limit, 'order': order, 'accumulation': accumulation, 'group': group}
        return session.get(url, headers=self._headers(), params=params)

    def build_season_player_statistics_types(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/player-statistics/types'
        return session.get(url, headers=self._headers())

    def build_season_team_statistics_types(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/team-statistics/types'
        return session.get(url, headers=self._headers())

    def build_season_top_players_overall(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/top-players/overall'
        return session.get(url, headers=self._headers())

    def build_season_top_teams_overall(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/top-teams/overall'
        return session.get(url, headers=self._headers())

    def build_season_top_players_per_game(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = (f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}'
               f'/top-players-per-game/all/overall')
        return session.get(url, headers=self._headers())

    def build_season_player_of_the_season(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/player-of-the-season'
        return session.get(url, headers=self._headers())

    def build_season_player_of_the_season_race(self, session: NetworkManager, unique_tournament_id,
                                                season_id) -> Response:
        url = (f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}'
               f'/player-of-the-season-race')
        return session.get(url, headers=self._headers())

    def build_season_team_of_the_period_periods(self, session: NetworkManager, unique_tournament_id,
                                                 season_id) -> Response:
        url = (f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}'
               f'/team-of-the-period/periods/rated')
        return session.get(url, headers=self._headers())

    def build_team_of_the_period(self, session: NetworkManager, period_id) -> Response:
        url = f'{self.base_url}/team-of-the-period/{period_id}'
        return session.get(url, headers=self._headers())

    def build_season_team_events_total(self, session: NetworkManager, unique_tournament_id, season_id) -> Response:
        url = f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}/team-events/total'
        return session.get(url, headers=self._headers())

    def build_season_team_performance_graph(self, session: NetworkManager, unique_tournament_id, season_id,
                                             team_id) -> Response:
        url = (f'{self.base_url}/unique-tournament/{unique_tournament_id}/season/{season_id}'
               f'/team/{team_id}/team-performance-graph-data')
        return session.get(url, headers=self._headers())

    def build_tournament_standings(self, session: NetworkManager, tournament_id, season_id,
                                    kind: str = 'total') -> Response:
        url = f'{self.base_url}/tournament/{tournament_id}/season/{season_id}/standings/{kind}'
        return session.get(url, headers=self._headers())

    def build_tournament_team_events_total(self, session: NetworkManager, tournament_id, season_id) -> Response:
        url = f'{self.base_url}/tournament/{tournament_id}/season/{season_id}/team-events/total'
        return session.get(url, headers=self._headers())

    def build_team(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}'
        return session.get(url, headers=self._headers())

    def build_seo_content_team(self, session: NetworkManager, team_id, lang: str = 'pt') -> Response:
        url = f'{self.base_url}/seo/content/team/{team_id}/{lang}'
        return session.get(url, headers=self._headers())

    def build_team_players(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/players'
        return session.get(url, headers=self._headers())

    def build_team_rankings(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/rankings'
        return session.get(url, headers=self._headers())

    def build_team_unique_tournaments(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/unique-tournaments'
        return session.get(url, headers=self._headers())

    def build_team_unique_tournaments_all(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/unique-tournaments/all'
        return session.get(url, headers=self._headers())

    def build_team_transfers(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/transfers'
        return session.get(url, headers=self._headers())

    def build_team_achievements(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/achievements'
        return session.get(url, headers=self._headers())

    def build_team_events_next(self, session: NetworkManager, team_id, page: int = 0) -> Response:
        url = f'{self.base_url}/team/{team_id}/events/next/{page}'
        return session.get(url, headers=self._headers())

    def build_team_events_last(self, session: NetworkManager, team_id, page: int = 0) -> Response:
        url = f'{self.base_url}/team/{team_id}/events/last/{page}'
        return session.get(url, headers=self._headers())

    def build_team_events_by_month(self, session: NetworkManager, team_id, month: str, year: str) -> Response:
        url = f'{self.base_url}/team/{team_id}/events/{month}-{year}'
        return session.get(url, headers=self._headers())

    def build_team_featured_event(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/featured-event'
        return session.get(url, headers=self._headers())

    def build_team_performance(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/performance'
        return session.get(url, headers=self._headers())

    def build_team_media_summary(self, session: NetworkManager, team_id, country: str = 'BR') -> Response:
        url = f'{self.base_url}/team/{team_id}/media/summary/country/{country}'
        return session.get(url, headers=self._headers())

    def build_team_media_videos(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/media/videos'
        return session.get(url, headers=self._headers())

    def build_team_official_tweets(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/official-tweets'
        return session.get(url, headers=self._headers())

    def build_team_offer_banner(self, session: NetworkManager, team_id, country: str = 'BR',
                                 lang: str = 'pt') -> Response:
        url = f'{self.base_url}/offers/banner/team/{team_id}/{country}/{lang}'
        return session.get(url, headers=self._headers())

    def build_team_standings_seasons(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/standings/seasons'
        return session.get(url, headers=self._headers())

    def build_team_player_statistics_seasons(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/player-statistics/seasons'
        return session.get(url, headers=self._headers())

    def build_team_team_statistics_seasons(self, session: NetworkManager, team_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/team-statistics/seasons'
        return session.get(url, headers=self._headers())

    def build_team_tournament_season_statistics(self, session: NetworkManager, team_id, unique_tournament_id,
                                                 season_id) -> Response:
        url = (f'{self.base_url}/team/{team_id}/unique-tournament/{unique_tournament_id}'
               f'/season/{season_id}/statistics/overall')
        return session.get(url, headers=self._headers())

    def build_team_tournament_season_ranks(self, session: NetworkManager, team_id, unique_tournament_id,
                                            season_id) -> Response:
        url = (f'{self.base_url}/team/{team_id}/unique-tournament/{unique_tournament_id}'
               f'/season/{season_id}/ranks/overall')
        return session.get(url, headers=self._headers())

    def build_team_season_best_result(self, session: NetworkManager, team_id, season_id) -> Response:
        url = f'{self.base_url}/team/{team_id}/season/{season_id}/best-result'
        return session.get(url, headers=self._headers())

    def build_event(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}'
        return session.get(url, headers=self._headers())

    def build_event_odds_all(self, session: NetworkManager, event_id, provider_id=1) -> Response:
        url = f'{self.base_url}/event/{event_id}/odds/{provider_id}/all'
        return session.get(url, headers=self._headers())

    def build_event_odds_featured(self, session: NetworkManager, event_id, provider_id=100) -> Response:
        url = f'{self.base_url}/event/{event_id}/odds/{provider_id}/featured'
        return session.get(url, headers=self._headers())

    def build_event_incidents(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/incidents'
        return session.get(url, headers=self._headers())

    def build_event_h2h(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/h2h'
        return session.get(url, headers=self._headers())

    def build_event_h2h_events(self, session: NetworkManager, event_id) -> Response:
        # event_id aqui pode ser o customId alfanumérico (ex.: "AJcsFJc")
        url = f'{self.base_url}/event/{event_id}/h2h/events'
        return session.get(url, headers=self._headers())

    def build_event_pregame_form(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/pregame-form'
        return session.get(url, headers=self._headers())

    def build_event_tv_channels(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/tv/event/{event_id}/country-channels'
        return session.get(url, headers=self._headers())

    def build_event_votes(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/votes'
        return session.get(url, headers=self._headers())

    def build_event_graph_sequence(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/graph/sequence'
        return session.get(url, headers=self._headers())

    def build_event_graph_win_probability(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/graph/win-probability'
        return session.get(url, headers=self._headers())

    def build_event_statistics(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/statistics'
        return session.get(url, headers=self._headers())

    def build_event_lineups(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/lineups'
        return session.get(url, headers=self._headers())

    def build_event_highlights(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/highlights'
        return session.get(url, headers=self._headers())

    def build_event_sport_video_highlights(self, session: NetworkManager, event_id, country: str = 'BR') -> Response:
        url = f'{self.base_url}/event/{event_id}/sport-video-highlights/country/{country}/extended'
        return session.get(url, headers=self._headers())

    def build_event_official_tweets(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/official-tweets'
        return session.get(url, headers=self._headers())

    def build_event_at_bats(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/at-bats'
        return session.get(url, headers=self._headers())

    def build_event_live_match_tracker(self, session: NetworkManager, event_id) -> Response:
        url = f'{self.base_url}/event/{event_id}/live-match-tracker'
        return session.get(url, headers=self._headers())

    def build_event_media_summary(self, session: NetworkManager, event_id, country: str = 'BR') -> Response:
        url = f'{self.base_url}/event/{event_id}/media/summary/country/{country}'
        return session.get(url, headers=self._headers())

    def build_translation_description(self, session: NetworkManager, resource_id, lang: str = 'pt') -> Response:
        url = f'{self.base_url}/translation/description/{resource_id}/language/{lang}'
        return session.get(url, headers=self._headers())

    def build_next_data_home(self, session: NetworkManager, lang: str = 'pt') -> Response:
        url = f'{self.root_url}/_next/data/{self.next_build_id}/{lang}.json'
        return session.get(url, headers=self._headers())

    def build_next_data_sport(self, session: NetworkManager, sport: str, lang: str = 'pt') -> Response:
        url = f'{self.root_url}/_next/data/{self.next_build_id}/{lang}/{sport}.json'
        return session.get(url, headers=self._headers())

    def build_next_data_sport_category(self, session: NetworkManager, sport: str, category_slug: str,
                                        lang: str = 'pt') -> Response:
        url = f'{self.root_url}/_next/data/{self.next_build_id}/{lang}/{sport}/{category_slug}.json'
        return session.get(url, headers=self._headers())

    def build_next_data_tournament(self, session: NetworkManager, sport: str, category_slug: str,
                                    tournament_slug: str, unique_tournament_id, lang: str = 'pt') -> Response:
        url = (f'{self.root_url}/_next/data/{self.next_build_id}/{lang}/{sport}/tournament'
               f'/{category_slug}/{tournament_slug}/{unique_tournament_id}.json')
        return session.get(url, headers=self._headers())

    def build_next_data_team(self, session: NetworkManager, sport: str, team_slug: str, team_id,
                              lang: str = 'pt') -> Response:
        url = f'{self.root_url}/_next/data/{self.next_build_id}/{lang}/{sport}/team/{team_slug}/{team_id}.json'
        return session.get(url, headers=self._headers())
