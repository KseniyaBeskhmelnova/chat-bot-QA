from bot.domain.messenger import Messenger
from bot.domain.order_state import OrderState
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards.order_keyboards import pizza_type_keyboard


class OrderApprovalRestartHandler(Handler):
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

        if state != OrderState.WAIT_FOR_ORDER_APPROVE:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data == "order_restart"

    def handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]

        messenger.answer_callback_query(update["callback_query"]["id"])
        messenger.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        storage.clear_user_order_json(telegram_id)

        storage.update_user_state(telegram_id, OrderState.WAIT_FOR_PIZZA_NAME)

        messenger.send_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="🔄 Let's start over!\n\nChoose your pizza:",
            reply_markup=pizza_type_keyboard(),
        )

        return HandlerStatus.STOP
