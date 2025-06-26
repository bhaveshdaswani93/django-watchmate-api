from rest_framework.throttling import UserRateThrottle

class WatchListThrottle(UserRateThrottle):
    scope = 'watchlist'

class WatchListDetailThrottle(UserRateThrottle):
    scope = 'watchlist_detail'