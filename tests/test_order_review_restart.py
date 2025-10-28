from bot.dispatcher import Dispatcher
from bot.handlers.order_review import OrderReview
from tests.mocks import Mock


def test_order_review_restart():
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "123",
            "from": {"id": 12345},
            "message": {
                "message_id": 10,
                "chat": {"id": 12345},
            },
            "data": "action_restart",
        },
    }

    update_user_order_json_called = False
    update_user_state_called = False
    send_message_calls = []

    def update_user_order_json(telegram_id: int, data: dict) -> None:
        assert telegram_id == 12345
        assert data == {}
        nonlocal update_user_order_json_called
        update_user_order_json_called = True

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 12345
        assert state == "WAIT_FOR_PIZZA_NAME"
        nonlocal update_user_state_called
        update_user_state_called = True

    def send_message(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 12345
        assert "Let's start over!" in text
        assert "Choose your pizza:" in text
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
    dispatcher.add_handlers(OrderReview())

    dispatcher._storage.get_user = lambda tid: {
        "state": "ORDER_REVIEW",
        "order_json": '{"pizza_name": "Pepperoni", "pizza_size": "Medium", "drink": "Coca-Cola"}',
    }

    dispatcher.dispatch(test_update)

    assert update_user_order_json_called
    assert update_user_state_called
    assert len(send_message_calls) == 1
    assert "reply_markup" in send_message_calls[0]["kwargs"]
