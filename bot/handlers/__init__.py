from bot.handlers.handler import Handler
from bot.handlers.db_logger import DatabaseLogger
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.message_start import MessageStart
from bot.handlers.pizza_selection import PizzaSelection
from bot.handlers.pizza_size import PizzaSize
from bot.handlers.order_confirmation import OrderConfirmation
from bot.handlers.order_review import OrderReview


def get_handlers() -> list[Handler]:
    return [
        DatabaseLogger(),
        EnsureUserExists(),
        MessageStart(),
        PizzaSelection(),
        PizzaSize(),
        OrderConfirmation(),
        OrderReview(),
    ]
