import json
from dotenv import load_dotenv
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .utils import func_args_preprocessing


class CoinGeckoAPI:
    __API_URL_BASE = 'https://api.coingecko.com/api/v3/'
    __PRO_API_URL_BASE = 'https://pro-api.coingecko.com/api/v3/'

    def __init__(self, api_key: str = '', retries=5):
        if api_key == '':
            api_key = os.environ.get('COINGECKO_API_KEY','')
        self.api_key = api_key
        if api_key:
            self.api_base_url = self.__PRO_API_URL_BASE
        else:
            self.api_base_url = self.__API_URL_BASE
        self.request_timeout = 120

        self.session = requests.Session()
        retries = Retry(total=retries, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def __request(self, url):
        try:
            response = self.session.get(url, timeout=self.request_timeout)
        except requests.exceptions.RequestException:
            raise

        try:
            response.raise_for_status()
            content = json.loads(response.content.decode('utf-8'))
            return content
        except Exception as e:
            try:
                content = json.loads(response.content.decode('utf-8'))
                raise ValueError(content)
            except json.decoder.JSONDecodeError:
                pass
            raise

    def __api_url_params(self, api_url, params, api_url_has_params=False):
        if self.api_key:
            params['x_cg_pro_api_key'] = self.api_key

        if params:
            api_url += '&' if api_url_has_params else '?'
            for key, value in params.items():
                if type(value) == bool:
                    value = str(value).lower()
                api_url += "{0}={1}&".format(key, value)
            api_url = api_url[:-1]
        return api_url

    # ---------- PING ----------#
    def ping(self, **kwargs):
        api_url = '{0}ping'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- SIMPLE ----------#
    @func_args_preprocessing
    def get_price(self, ids, vs_currencies, **kwargs):
        ids = ids.replace(' ', '')
        kwargs['ids'] = ids
        vs_currencies = vs_currencies.replace(' ', '')
        kwargs['vs_currencies'] = vs_currencies

        api_url = '{0}simple/price'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_token_price(self, id, contract_addresses, vs_currencies, **kwargs):
        contract_addresses = contract_addresses.replace(' ', '')
        kwargs['contract_addresses'] = contract_addresses
        vs_currencies = vs_currencies.replace(' ', '')
        kwargs['vs_currencies'] = vs_currencies

        api_url = '{0}simple/token_price/{1}'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_supported_vs_currencies(self, **kwargs):
        api_url = '{0}simple/supported_vs_currencies'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- COINS ----------#
    @func_args_preprocessing
    def get_coins(self, **kwargs):
        api_url = '{0}coins'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_top_gainers_losers(self, vs_currency, **kwargs):
        api_url = '{0}coins/top_gainers_losers?vs_currency={1}'.format(self.api_base_url, vs_currency)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coins_list_new(self, **kwargs):
        api_url = '{0}coins/list/new'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coins_list(self, **kwargs):
        api_url = '{0}coins/list'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coins_markets(self, vs_currency, **kwargs):
        kwargs['vs_currency'] = vs_currency
        api_url = '{0}coins/markets'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_by_id(self, id, **kwargs):
        api_url = '{0}coins/{1}'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_ticker_by_id(self, id, **kwargs):
        api_url = '{0}coins/{1}/tickers'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_history_by_id(self, id, date, **kwargs):
        kwargs['date'] = date
        api_url = '{0}coins/{1}/history'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_market_chart_by_id(self, id, vs_currency, days, **kwargs):
        api_url = '{0}coins/{1}/market_chart?vs_currency={2}&days={3}'.format(self.api_base_url, id, vs_currency, days)
        api_url = self.__api_url_params(api_url, kwargs, api_url_has_params=True)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_market_chart_range_by_id(self, id, vs_currency, from_timestamp, to_timestamp, **kwargs):
        api_url = '{0}coins/{1}/market_chart/range?vs_currency={2}&from={3}&to={4}'.format(self.api_base_url, id,
                                                                                           vs_currency, from_timestamp,
                                                                                           to_timestamp)
        api_url = self.__api_url_params(api_url, kwargs, api_url_has_params=True)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_ohlc_by_id(self, id, vs_currency, days, **kwargs):
        api_url = '{0}coins/{1}/ohlc?vs_currency={2}&days={3}'.format(self.api_base_url, id, vs_currency, days)
        api_url = self.__api_url_params(api_url, kwargs, api_url_has_params=True)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_ohlc_by_id_range(self, id, vs_currency, from_timestamp, to_timestamp, interval, **kwargs):
        kwargs['vs_currency'] = vs_currency
        kwargs['from'] = from_timestamp
        kwargs['to'] = to_timestamp
        kwargs['interval'] = interval

        api_url = '{0}coins/{1}/ohlc/range'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_circulating_supply_chart(self, id, days, **kwargs):
        kwargs['days'] = days
        api_url = '{0}coins/{1}/circulating_supply_chart'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_circulating_supply_chart_range(self, id, from_timestamp, to_timestamp, **kwargs):
        kwargs['from'] = from_timestamp
        kwargs['to'] = to_timestamp
        api_url = '{0}coins/{1}/circulating_supply_chart/range'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_total_supply_chart(self, id, days, **kwargs):
        kwargs['days'] = days
        api_url = '{0}coins/{1}/total_supply_chart'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_total_supply_chart_range(self, id, from_timestamp, to_timestamp, **kwargs):
        kwargs['from'] = from_timestamp
        kwargs['to'] = to_timestamp
        api_url = '{0}coins/{1}/total_supply_chart/range'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- Contract ----------#
    @func_args_preprocessing
    def get_coin_info_from_contract_address_by_id(self, id, contract_address, **kwargs):
        api_url = '{0}coins/{1}/contract/{2}'.format(self.api_base_url, id, contract_address)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_market_chart_from_contract_address_by_id(self, id, contract_address, vs_currency, days, **kwargs):
        api_url = '{0}coins/{1}/contract/{2}/market_chart?vs_currency={3}&days={4}'.format(self.api_base_url, id,
                                                                                           contract_address,
                                                                                           vs_currency, days)
        api_url = self.__api_url_params(api_url, kwargs, api_url_has_params=True)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coin_market_chart_range_from_contract_address_by_id(self, id, contract_address, vs_currency, from_timestamp,
                                                                to_timestamp, **kwargs):
        api_url = '{0}coins/{1}/contract/{2}/market_chart/range?vs_currency={3}&from={4}&to={5}'.format(
            self.api_base_url, id, contract_address, vs_currency, from_timestamp, to_timestamp)
        api_url = self.__api_url_params(api_url, kwargs, api_url_has_params=True)
        return self.__request(api_url)

    # ---------- ASSET PLATFORMS ----------#
    @func_args_preprocessing
    def get_asset_platforms(self, **kwargs):
        api_url = '{0}asset_platforms'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_asset_platform_by_id(self, id, **kwargs):
        api_url = '{0}token_lists/{1}/all.json'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- CATEGORIES ----------#
    @func_args_preprocessing
    def get_coins_categories_list(self, **kwargs):
        api_url = '{0}coins/categories/list'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_coins_categories(self, **kwargs):
        api_url = '{0}coins/categories'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- EXCHANGES ----------#
    @func_args_preprocessing
    def get_exchanges_list(self, **kwargs):
        api_url = '{0}exchanges'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_exchanges_id_name_list(self, **kwargs):
        api_url = '{0}exchanges/list'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_exchanges_by_id(self, id, **kwargs):
        api_url = '{0}exchanges/{1}'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_exchanges_tickers_by_id(self, id, **kwargs):
        api_url = '{0}exchanges/{1}/tickers'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_exchanges_volume_chart_by_id(self, id, days, **kwargs):
        kwargs['days'] = days
        api_url = '{0}exchanges/{1}/volume_chart'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_exchanges_volume_chart_by_id_within_time_range(self, id, from_timestamp, to_timestamp, **kwargs):
        kwargs['from'] = from_timestamp
        kwargs['to'] = to_timestamp
        api_url = '{0}exchanges/{1}/volume_chart/range'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- INDEXES ----------#
    @func_args_preprocessing
    def get_indexes(self, **kwargs):
        api_url = '{0}indexes'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_indexes_by_market_id_and_index_id(self, market_id, id, **kwargs):
        api_url = '{0}indexes/{1}/{2}'.format(self.api_base_url, market_id, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_indexes_list(self, **kwargs):
        api_url = '{0}indexes/list'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- DERIVATIVES ----------#
    @func_args_preprocessing
    def get_derivatives(self, **kwargs):
        api_url = '{0}derivatives'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_derivatives_exchanges(self, **kwargs):
        api_url = '{0}derivatives/exchanges'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_derivatives_exchanges_by_id(self, id, **kwargs):
        api_url = '{0}derivatives/exchanges/{1}'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_derivatives_exchanges_list(self, **kwargs):
        api_url = '{0}derivatives/exchanges/list'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- NFTS (BETA) ----------#
    @func_args_preprocessing
    def get_nfts_list(self, **kwargs):
        api_url = '{0}nfts/list'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_nfts_by_id(self, id, **kwargs):
        api_url = '{0}nfts/{1}'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_nfts_by_asset_platform_id_and_contract_address(self, asset_platform_id, contract_address, **kwargs):
        api_url = f'{self.api_base_url}nfts/{asset_platform_id}/contract/{contract_address}'
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_nfts_markets(self, **kwargs):
        api_url = '{0}nfts/markets'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_nfts_market_chart_by_id(self, id, days, **kwargs):
        kwargs['days'] = days
        api_url = '{0}nfts/{1}/market_chart'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_ntfs_market_chart_by_asset_platform_id_and_contract_address(self, asset_platform_id, contract_address, days,
                                                                        **kwargs):
        kwargs['days'] = days
        api_url = f'{self.api_base_url}nfts/{asset_platform_id}/contract/{contract_address}/market_chart'
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_nfts_tickers(self, id, **kwargs):
        api_url = '{0}nfts/{1}/tickers'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

        # ---------- GENERAL ----------#
    @ func_args_preprocessing
    def get_exchange_rates(self, **kwargs):
        api_url = '{0}exchange_rates'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_asset_platforms(self, **kwargs):
        api_url = '{0}asset_platforms'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_asset_platform_by_id(self, id, **kwargs):
        api_url = '{0}token_lists/{1}/all.json'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def search(self, query, **kwargs):
        api_url = '{0}search?query={1}'.format(self.api_base_url, query)
        api_url = self.__api_url_params(api_url, kwargs, api_url_has_params=True)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_search_trending(self, **kwargs):
        api_url = '{0}search/trending'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_global(self, **kwargs):
        api_url = '{0}global'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)['data']

    @func_args_preprocessing
    def get_global_decentralized_finance_defi(self, **kwargs):
        api_url = '{0}global/decentralized_finance_defi'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)['data']

    @func_args_preprocessing
    def get_global_market_cap_chart(self, days, **kwargs):
        kwargs['days'] = days
        api_url = '{0}global/market_cap_chart'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_companies_public_treasury_by_coin_id(self, coin_id, **kwargs):
        api_url = '{0}companies/public_treasury/{1}'.format(self.api_base_url, coin_id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    # ---------- ONCHAIN DEX ENDPOINTS (GeckoTerminal) ----------#
    @func_args_preprocessing
    def get_onchain_token_price(self, network, token_address, **kwargs):
        api_url = '{0}onchain/simple/networks/{1}/token_price/{2}'.format(self.api_base_url, network, token_address)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_networks(self, **kwargs):
        api_url = '{0}onchain/networks'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_dexes(self, network, **kwargs):
        api_url = '{0}onchain/networks/{1}/dexes'.format(self.api_base_url, network)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_trending_pools(self, **kwargs):
        api_url = '{0}onchain/networks/trending_pools'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_network_trending_pools(self, network, **kwargs):
        api_url = '{0}onchain/networks/{1}/trending_pools'.format(self.api_base_url, network)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_pool(self, network, pool_address, **kwargs):
        api_url = '{0}onchain/networks/{1}/pools/{2}'.format(self.api_base_url, network, pool_address)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_multi_pools(self, network, pool_addresses, **kwargs):
        api_url = '{0}onchain/networks/{1}/pools/multi/{2}'.format(self.api_base_url, network, pool_addresses)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_top_pools(self, network, **kwargs):
        api_url = '{0}onchain/networks/{1}/pools'.format(self.api_base_url, network)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_dex_top_pools(self, network, dex, **kwargs):
        api_url = '{0}onchain/networks/{1}/dexes/{2}/pools'.format(self.api_base_url, network, dex)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_new_pools(self, network, **kwargs):
        api_url = '{0}onchain/networks/{1}/new_pools'.format(self.api_base_url, network)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_all_new_pools(self, **kwargs):
        api_url = '{0}onchain/networks/new_pools'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def search_onchain_pools(self, **kwargs):
        api_url = '{0}onchain/search/pools'.format(self.api_base_url)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)

    @func_args_preprocessing
    def get_onchain_token_pools(self, network, token_address, **kwargs):
        api_url = '{0}onchain/networks/{1}/tokens/{2}/pools'.format(self.api_base_url, network, token_address)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)
