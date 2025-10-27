import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards.order_keyboards import size_keyboard


class PizzaSelection(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_NAME":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        pizza_name = callback_data.replace("pizza_", "").replace("_", " ").title()
        bot.database_client.update_user_data(telegram_id, {"pizza_name": pizza_name})
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_SIZE")
        bot.telegram_client.answer_callback_query(update["callback_query"]["id"])

        chat_id = update["callback_query"]["message"]["chat"]["id"]

        bot.telegram_client.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"],
        )

        bot.telegram_client.sendMessage(
            chat_id=chat_id,
            text="📐Please, select pizza size:",
            reply_markup=size_keyboard(),
        )
        return HandlerStatus.STOP
