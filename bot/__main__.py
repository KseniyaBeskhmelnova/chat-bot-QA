from bot.dispatcher import Dispatcher
from bot.handlers import get_handlers
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.infrastructure.messenger_telegram import MessengerTelegram
from bot.infrastructure.storage_postgres import StoragePostgres
import bot.long_polling


def main() -> None:
    try:
        storage: Storage = StoragePostgres()
        messenger: Messenger = MessengerTelegram()

        dispatcher = Dispatcher(storage, messenger)
        dispatcher.add_handlers(*get_handlers())
        print("✅ Bot is running")
        bot.long_polling.start_long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
