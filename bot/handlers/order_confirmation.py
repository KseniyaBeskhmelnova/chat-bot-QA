import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards.order_keyboards import confirm_keyboard


class OrderConfirmation(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False
        if state != "WAIT_FOR_DRINKS":
            return False
        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        bot.database_client.update_user_data(telegram_id, order_json)
        callback_data = update["callback_query"]["data"]

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
        bot.database_client.update_user_data(telegram_id, order_json)
        bot.database_client.update_user_state(telegram_id, "ORDER_REVIEW")

        bot.telegram_client.answer_callback_query(update["callback_query"]["id"])

        chat_id = update["callback_query"]["message"]["chat"]["id"]
        message_id = update["callback_query"]["message"]["message_id"]

        bot.telegram_client.deleteMessage(chat_id=chat_id, message_id=message_id)

        pizza_name = order_json.get("pizza_name", "—")
        pizza_size = order_json.get("pizza_size", "—")
        selected_drink = order_json.get("drink", "—")

        order_text = (
            "🛒 <b>Your order:</b>\n\n"
            f"🍕 <b>Pizza:</b> {pizza_name}\n"
            f"📐 <b>Size:</b> {pizza_size}\n"
            f"🍾 <b>Drink:</b> {selected_drink}\n\n"
            "✅ Confirm your order?"
        )

        reply_markup = confirm_keyboard()

        bot.telegram_client.sendMessage(
            chat_id=chat_id,
            text=order_text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

        return HandlerStatus.STOP
