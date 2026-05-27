from app.models.base import Base
from app.models.trademark import Trademark, TrademarkClass
from app.models.watchlist import WatchlistEntry
from app.models.deadline import DeadlineAlert
from app.models.opposition import OppositionCase
from app.models.search_query import SearchQuery
from app.models.subscription import Subscription

__all__ = [
    "Base",
    "Trademark",
    "TrademarkClass",
    "WatchlistEntry",
    "DeadlineAlert",
    "OppositionCase",
    "SearchQuery",
    "Subscription",
]
