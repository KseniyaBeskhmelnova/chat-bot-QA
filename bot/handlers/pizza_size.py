import asyncio

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards.order_keyboards import drink_keyboard
from bot.domain.order_state import OrderState


class PizzaSizeHandler(Handler):
    def can_handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != OrderState.WAIT_FOR_PIZZA_SIZE:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

    async def handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        size_mapping = {
            "size_small": "Small (25cm)",
            "size_medium": "Medium (30cm)",
            "size_large": "Large (35cm)",
            "size_extra_large": "Extra Large (40cm)",
        }

        pizza_size = size_mapping.get(callback_data)
        order_json["pizza_size"] = pizza_size

        callback_query_id = update["callback_query"]["id"]

        await asyncio.gather(
            storage.update_user_order_json(telegram_id, order_json),
            storage.update_user_state(telegram_id, OrderState.WAIT_FOR_DRINKS),
            messenger.answer_callback_query(callback_query_id),
        )

        await asyncio.gather(
            messenger.delete_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                message_id=update["callback_query"]["message"]["message_id"],
            ),
            messenger.send_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="🍾Please, choose a drink:",
                reply_markup=drink_keyboard(),
            ),
        )
        return HandlerStatus.STOP
