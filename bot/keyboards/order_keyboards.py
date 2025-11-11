from typing import List, Dict, Any


def build_inline_keyboard(buttons: List[Dict[str, str]]) -> Dict[str, Any]:
    return {"inline_keyboard": [[btn] for btn in buttons]}


def pizza_type_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "🧀 Margherita", "callback_data": "pizza_margherita"},
                {"text": "🌶️ Pepperoni", "callback_data": "pizza_pepperoni"},
            ],
            [
                {
                    "text": "🌿 Quattro Stagioni",
                    "callback_data": "pizza_quattro_stagioni",
                },
                {"text": "🍍 Hawaiian", "callback_data": "pizza_hawaiian"},
            ],
        ]
    }


def size_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "👶 Small (25cm)", "callback_data": "size_small"},
                {"text": "🧒 Medium (30cm)", "callback_data": "size_medium"},
            ],
            [
                {"text": "👨 Large (35cm)", "callback_data": "size_large"},
                {"text": "💪 Extra Large (40cm)", "callback_data": "size_extra_large"},
            ],
        ]
    }


def drink_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "🥤 Coca-Cola", "callback_data": "drink_coca_cola"},
                {"text": "🥤 Pepsi", "callback_data": "drink_pepsi"},
            ],
            [
                {"text": "🧃 Orange Juice", "callback_data": "drink_orange_juice"},
                {"text": "💧 Water", "callback_data": "drink_water"},
            ],
            [{"text": "🙅‍♂️ No drinks", "callback_data": "drink_none"}],
        ]
    }


def confirm_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "✅ Confirm Order", "callback_data": "order_approve"},
                {"text": "🔁 Start Again", "callback_data": "order_restart"},
            ]
        ]
    }
