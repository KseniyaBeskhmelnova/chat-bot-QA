from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards.order_keyboards import pizza_type_keyboard


class OrderReview(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False
        if state != "ORDER_REVIEW":
            return False
        callback_data = update["callback_query"]["data"]
        return callback_data in ("action_confirm", "action_restart")

    def handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        message_id = update["callback_query"]["message"]["message_id"]

        messenger.answer_callback_query(update["callback_query"]["id"])
        messenger.delete_message(chat_id=chat_id, message_id=message_id)

        if callback_data == "action_confirm":
            order_json["status"] = "confirmed"
            storage.update_user_order_json(telegram_id, order_json)
            storage.update_user_state(telegram_id, "IDLE")

            messenger.send_message(
                chat_id=chat_id,
                text="🎉 <b>Order confirmed!</b>\n\nYour pizza is being prepared!🍕\nCourier will contact you soon!☎",
                parse_mode="HTML",
            )

        elif callback_data == "action_restart":
            storage.update_user_order_json(telegram_id, {})
            storage.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            messenger.send_message(
                chat_id=chat_id,
                text="🔄 Let's start over!\n\nChoose your pizza:",
                reply_markup=pizza_type_keyboard(),
            )

        return HandlerStatus.STOP
