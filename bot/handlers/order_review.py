import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards.order_keyboards import pizza_type_keyboard


class OrderReview(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False
        if state != "ORDER_REVIEW":
            return False
        callback_data = update["callback_query"]["data"]
        return callback_data in ("action_confirm", "action_restart")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        message_id = update["callback_query"]["message"]["message_id"]

        bot.telegram_client.answer_callback_query(update["callback_query"]["id"])
        bot.telegram_client.deleteMessage(chat_id=chat_id, message_id=message_id)

        if callback_data == "action_confirm":
            order_json["status"] = "confirmed"
            bot.database_client.update_user_data(telegram_id, order_json)
            bot.database_client.update_user_state(telegram_id, "IDLE")

            bot.telegram_client.sendMessage(
                chat_id=chat_id,
                text="🎉 <b>Order confirmed!</b>\n\nYour pizza is being prepared!🍕\nCourier will contact you soon!☎",
                parse_mode="HTML",
            )

        elif callback_data == "action_restart":
            bot.database_client.update_user_data(telegram_id, {})
            bot.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            bot.telegram_client.sendMessage(
                chat_id=chat_id,
                text="🔄 Let's start over!\n\nChoose your pizza:",
                reply_markup=pizza_type_keyboard(),
            )

        return HandlerStatus.STOP
