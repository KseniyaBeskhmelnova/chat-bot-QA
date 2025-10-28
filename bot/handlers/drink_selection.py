from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards.order_keyboards import confirm_keyboard


class DrinkHandler(Handler):
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

        if state != "WAIT_FOR_DRINKS":
            return False
        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

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

        messenger.answer_callback_query(update["callback_query"]["id"])
        messenger.delete_message(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "drink_none":
            drink = "No drinks"
        else:
            drink_mapping = {
                "drink_coca_cola": "Coca-Cola",
                "drink_pepsi": "Pepsi",
                "drink_orange_juice": "Orange Juice",
                "drink_water": "Water",
            }
            drink = drink_mapping.get(callback_data, "Unknown")

        order_json["drink"] = drink
        storage.update_user_order_json(telegram_id, order_json)

        storage.update_user_state(telegram_id, "ORDER_REVIEW")

        pizza_name = order_json.get("pizza_name", "Unknown")
        pizza_size = order_json.get("pizza_size", "Unknown")

        order_text = (
            "🛒 <b>Your order:</b>\n\n"
            f"🍕 <b>Pizza:</b> {pizza_name}\n"
            f"📐 <b>Size:</b> {pizza_size}\n"
            f"🍾 <b>Drink:</b> {drink}\n\n"
            "✅ Confirm your order?"
        )

        reply_markup = confirm_keyboard()

        messenger.send_message(
            chat_id=chat_id,
            text=order_text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

        return HandlerStatus.STOP
