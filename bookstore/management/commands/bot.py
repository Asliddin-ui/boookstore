#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Don't forget to enable inline mode with @BotFather

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from django.conf import settings
from django.core.management import BaseCommand
from asgiref.sync import sync_to_async
from bookstore.models import Books
from users.models import Users
from django.utils.translation import gettext_lazy as _
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Update, __version__ as TG_VER
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler, MessageHandler, filters

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


STATE = 'state'
STATE_REGISTRATION = 'registration'
STATE_LANGUAGE = 'language'
STATE_ADD = 'book-add'
STATE_ADD_NAME = 'book-add-name'
STATE_ADD_CONTENT = 'book-add-content'
STATE_ADD_PHOTO = 'book-add-photo'
STATE_ADD_PRICE = 'book-add-price'
STATE_ADD_STATUS = 'book-add-status'
STATE_ADD_PUBLISH_YEAR = 'book-add-publish_year'
STATE_ADD_COUNTRY = 'book-add-country'
STATE_ADD_CATEGORY = 'book-add-category'
STATE_ADD_LANGUAGE = 'book-add-language'
STATE_ADD_AUTHOR = 'book-add-author'
STATE_SAVE = "book-save"

ADD_QUESTIONS = {"hi": _("Salom botimizga xush kelibsiz!\nKitob qo'shish uchun /add buyrugini kiriting")
                ,"name":_("Kitob nomini kiriting!"), "content":_("Kitobga ta'rif bering!"),
                  "photo":_("Kitob rasmini jo'nating!"), "photo1":_("Kitob rasmini kiritasizmi?"),
                  "price":_("Kitob narxini kiriting!"), "status":_("Kitobning statusini tanlang!"),
                  "publish_year":_("Kitob chop qilingan yilni kiriting!"), "publish_year1":_("Chop qilingan yili bormi?"),
                  "category":_("Kitob kategoriyasi?"), "language":_("Kitob chop qilingan til?"),
                  "country":_("Chop qilingan davlati?"), "author":_("Kitob aftorini tanlang!"),
                  "author1":_("Yana Avtor qo'shasizmi?"), "save_agr":_("Ma'lumotlarni saqlaysizmi?"), "save": _("📁 Ma'lumotlarni saqlash"),
                  "data_success":_("Ma'lumotlarni muvofaqiyatli to'ldirdingiz!\nMalumotlarni saqlash uchun pastdagi tugmani bosing!"),
                 "success": _('Muvofaqiyatli!'), "choose_lang": _("Kerakli tilni tanlang!")
                }
PERM = {"nostart": _("Hurmatli foydalanuvchi oldin /start buyrug'ini kiriiting"),"common_format_err":_("Hurmatli foydalanuvchi siz noto'g'ri formatda"
                            " ma'lumot kirityapsiz iltimos malumotni to'g'ri kiriting"),
        "min_price_err":_("Kitob narxining eng kichik qiymati: 1000\n"
                        "Iltimos kattaroq summa kiriting!"),
        "price_type_err":_("Iltimos harf va belgi aralashtirmasdan\n"
                        "Faqat son kiriting! Misol uchun: 23500"),
        "year_type_err":_("Iltimos harf va belgi aralashtirmasdan\nFaqat raqamlar kiriting!"),
        "year_format_err":_("Iltimos yil YYYY formatda kiriting\nMisol uchun: \n2020"),
        "max_year_err":_("Siz kiritgan yil hozirgi yildan katta bo'lmasligi kerak!\nIltimos qayta urining"),
        "yes": _("Ha"), "no": _("Yo'q"), "nstat": _('Yangi'), "pstat": _('Qabul qilingan'), "rstat": _('Inkor qilingan')
        }
BOOK = {"common": _("Kotob ma'lumotlari"), "name": _("Kitob nomi"),
            "content": _("Kitob ta'rifi"), "price": _("Kitob narxi"),
            "status": _("Kitob statusi raqami"), "publish_year": _("Kitob chop qilingan yili"),
            "category": _("Kitob kategoriya"), "language": _("Kitob chiqarilgan til"),
            "country": _("Kitob chiqarilgan davlat"), "authors": _("Kitob aftorlari"),
            "uagr": _("Ko'rsatilgan ma'lumotlarni saqlaysizmi?"), "success_save": _("😅 Ma'lumot muvofaqiyatli saqlandi!\nYana qo'shishni hohlasangiz\n/add komondasini ustiga bosing!"),
        "success_delete": _("🤕 Ma'lumotlar o'chirildi!\nYana qo'shishni hohlasangiz\n/add komondasini ustiga bosing!"),"not_show": _("Ko'rsatilmagan")}



class Command(BaseCommand):
    
    # Define a few command handlers. These usually take the two arguments update and
    # context.
    async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued.""" 
        user_data = update.effective_user
        await update.message.reply_text(f'{ADD_QUESTIONS["hi"]}')

        context.user_data[STATE] = STATE_ADD

    async def lang_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Kitob ')


    async def inline_query(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the inline query. This is run when you type: @botusername <query>"""
        query = update.inline_query.query
        print(update.inline_query.from_user.id)
        results = []
        if not query:  # empty query should not be handled
            books = await sync_to_async(lambda : [row for row in Books.objects.all()])()
            for b in books:
                results.append(
                    InlineQueryResultArticle(
                        id=b.id,
                        title=b.name,
                        input_message_content=InputTextMessageContent(b.name),
                    )
                )
            await update.inline_query.answer(results)


        books = await sync_to_async(lambda : [row for row in Books.objects.values('id','name','category__name',
                                                                                  'language__lang','price','content','publish_year').filter(name__startswith=query)])()

        for b in books:
            results.append(
                InlineQueryResultArticle(
                    id=b['id'],
                    title=f"{b['name']}",
                    input_message_content=InputTextMessageContent(f"Kitob nomi: {b['name']}\nKategorya nomi: {b['category__name']}\nNarxi: {b['price']}")
                )
            )

        await update.inline_query.answer(results)


    def handle(self,*args,**options) -> None:
        """Run the bot."""
        # Create the Application and pass it your bot's token.
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # on different commands - answer in Telegram
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler('add', self.lang_handler))

        # on non command i.e message - echo the message on Telegram
        application.add_handler(InlineQueryHandler(self.inline_query))

        # Run the bot until the user presses Ctrl-C
        application.run_polling()

