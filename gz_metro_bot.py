from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import metro
import logging
import metro_time_dic
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def command_data_replace(msg):
    num = 0
    for i in range(len(msg)):
        if msg[i] == ' ':
            num = i
            break
    msg = msg.replace(msg[:num + 1], '')
    if '@gz_metro_bot' in msg:
        msg = msg.replace('@gz_metro_bot', '')
    return msg

def search_line(bot, update):
    msg = command_data_replace(update.message.text)
    startStation = ''
    endStation = ''
    num = 0
    for i in range(len(msg)):
        if msg[i] == ' ':
            num = i
            break
    if num == 0:
        bot.sendMessage(chat_id = update.message.chat_id, text = "用法: /search_line 起始地铁站 [space] 终点地铁站")
        return
    else:
        startStation = msg[:num]
        endStation = msg[num + 1:]
    msg = metro.get_metro(startStation, endStation)
    bot.sendMessage(chat_id = update.message.chat_id, text = msg)

def time_line(bot, update):
    msg = command_data_replace(update.message.text)
    try:
        result = metro_time_dic.get_lineId(msg)
        result = metro_time_dic.json_result(result)
        result = metro_time_dic.format_result(result)
    except:
        result = '用法: /time_line + 线路，例如: /time_line 三北线'
    finally:
        bot.sendMessage(chat_id = update.message.chat_id, text = result)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater('KEY')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("search_line", search_line))
    dp.add_handler(CommandHandler("time_line", time_line))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


