from bot.handlers.order_approval_restart import OrderApprovalRestartHandler
from tests.mocks import Mock
from bot.keyboards.order_keyboards import pizza_type_keyboard
from bot.dispatcher import Dispatcher


def test_order_approval_restart_handler():
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "123",
            "from": {"id": 12345},
            "message": {
                "message_id": 10,
                "chat": {"id": 12345},
            },
            "data": "order_restart",
        },
    }

    clear_user_order_json_called = False
    update_user_state_called = False
    send_message_calls = []

    def clear_user_order_json(telegram_id: int) -> None:
        assert telegram_id == 12345
        nonlocal clear_user_order_json_called
        clear_user_order_json_called = True

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 12345
        assert state == "WAIT_FOR_PIZZA_NAME"
        nonlocal update_user_state_called
        update_user_state_called = True

    def send_message(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 12345
        assert "Let's start over!" in text
        assert "Choose your pizza:" in text
        assert "reply_markup" in kwargs
        send_message_calls.append({"text": text, "kwargs": kwargs})
        return {"ok": True}

    def answer_callback_query(callback_query_id: str) -> None:
        assert callback_query_id == "123"

    def delete_message(chat_id: int, message_id: int) -> None:
        assert chat_id == 12345
        assert message_id == 10

    mock_storage = Mock(
        {
            "clear_user_order_json": clear_user_order_json,
            "update_user_state": update_user_state,
        }
    )
    mock_messenger = Mock(
        {
            "send_message": send_message,
            "answer_callback_query": answer_callback_query,
            "delete_message": delete_message,
        }
    )

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    dispatcher.add_handlers(OrderApprovalRestartHandler())

    dispatcher._storage.get_user = lambda tid: {
        "state": "WAIT_FOR_ORDER_APPROVE",
        "order_json": '{"pizza_name": "Pepperoni", "pizza_size": "Medium (30cm)", "drink": "Coca-Cola"}',
    }

    dispatcher.dispatch(test_update)

    assert clear_user_order_json_called
    assert update_user_state_called
    assert len(send_message_calls) == 1
    assert send_message_calls[0]["kwargs"]["reply_markup"] == pizza_type_keyboard()
