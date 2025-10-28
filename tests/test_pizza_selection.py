from bot.dispatcher import Dispatcher
from bot.handlers.pizza_selection import PizzaSelectionHandler
from tests.mocks import Mock


def test_pizza_selection_handler():
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "123",
            "from": {"id": 12345},
            "message": {
                "message_id": 10,
                "chat": {"id": 12345},
            },
            "data": "pizza_pepperoni",
        },
    }

    update_user_order_json_called = False
    update_user_state_called = False
    send_message_calls = []

    def update_user_order_json(telegram_id: int, data: dict) -> None:
        assert telegram_id == 12345
        assert data == {"pizza_name": "Pepperoni"}
        nonlocal update_user_order_json_called
        update_user_order_json_called = True

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 12345
        assert state == "WAIT_FOR_PIZZA_SIZE"
        nonlocal update_user_state_called
        update_user_state_called = True

    def send_message(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 12345
        assert "select pizza size" in text
        send_message_calls.append({"text": text, "kwargs": kwargs})
        return {"ok": True}

    def answer_callback_query(callback_query_id: str) -> None:
        assert callback_query_id == "123"

    def delete_message(chat_id: int, message_id: int) -> None:
        assert chat_id == 12345
        assert message_id == 10

    mock_storage = Mock(
        {
            "update_user_order_json": update_user_order_json,
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
    dispatcher.add_handlers(PizzaSelectionHandler())

    dispatcher._storage.get_user = lambda tid: {
        "state": "WAIT_FOR_PIZZA_NAME",
        "order_json": "{}",
    }

    dispatcher.dispatch(test_update)

    assert update_user_order_json_called
    assert update_user_state_called
    assert len(send_message_calls) == 1
