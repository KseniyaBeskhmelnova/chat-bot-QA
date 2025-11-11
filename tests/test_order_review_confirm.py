from bot.dispatcher import Dispatcher
from bot.handlers.order_approval_approved import OrderApprovalApprovedHandler
from tests.mocks import Mock


def test_order_approval_approved_handler():
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "123",
            "from": {"id": 12345},
            "message": {
                "message_id": 10,
                "chat": {"id": 12345},
            },
            "data": "order_approve",
        },
    }

    update_user_state_called = False
    send_invoice_called = False

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 12345
        assert state == "WAIT_FOR_PAYMENT"
        nonlocal update_user_state_called
        update_user_state_called = True

    def send_invoice(
        chat_id: int,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list,
    ) -> dict:
        assert chat_id == 12345
        assert title == "Pizza Order"
        assert "Pepperoni" in description
        assert "Medium" in description
        assert "Coca-Cola" in description
        assert provider_token is not None
        assert currency == "RUB"
        assert len(prices) == 2
        assert prices[0]["label"] == "Pizza: Pepperoni (Medium (30cm))"
        assert prices[0]["amount"] == 65000
        assert prices[1]["label"] == "Drink: Coca-Cola"
        assert prices[1]["amount"] == 5000
        nonlocal send_invoice_called
        send_invoice_called = True
        return {"ok": True}

    def answer_callback_query(callback_query_id: str) -> None:
        assert callback_query_id == "123"

    def delete_message(chat_id: int, message_id: int) -> None:
        assert chat_id == 12345
        assert message_id == 10

    mock_storage = Mock(
        {
            "update_user_state": update_user_state,
        }
    )
    mock_messenger = Mock(
        {
            "send_invoice": send_invoice,
            "answer_callback_query": answer_callback_query,
            "delete_message": delete_message,
        }
    )

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    dispatcher.add_handlers(OrderApprovalApprovedHandler())

    dispatcher._storage.get_user = lambda tid: {
        "state": "WAIT_FOR_ORDER_APPROVE",
        "order_json": '{"pizza_name": "Pepperoni", "pizza_size": "Medium (30cm)", "drink": "Coca-Cola"}',
    }

    dispatcher.dispatch(test_update)

    assert update_user_state_called
    assert send_invoice_called
