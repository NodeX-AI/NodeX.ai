MESSAGES = {
    'ru' : {
        'start' : '<b>N​o​d​e​X.​a​i</b> — телеграм-бот с доступом к множеству различным моделям нейросетей.\n\n<b>Используя команду</b> /start <b>вы сразу соглашаетесь с:</b>\n • <a href="https://telegra.ph/Politika-konfidencialnosti-telegram-bota-NodeXai-11-01">Политикой конфеденциальности</a>\n • <a href="https://telegra.ph/OGRANICHENIE-OTVETSTVENNOSTI-telegram-bota-NodeXai-11-01">Политикой ограничения ответственности</a>\n • <a href="https://telegra.ph/POLZOVATELSKOE-SOGLASHENIE-telegarm-bota-NodeXai-11-01">Пользовательским соглашением</a>\n<i>Вы, как пользователь, имеете право отозвать соглашения путем удаления аккаунта через пункт в меню "Опасная зона"</i>\n • <a href="https://telegra.ph/Pravila-ispolzovaniya-telegram-bota-NodeXai-11-01">Правила использования сервиса</a>\n\n<b>Чтобы задать вопрос нейросети — напишите тектовое сообщение</b>\n<b>Меню:</b> /menu\n\n<b>Следите за новостями:</b> @NodeX_project\n<b>Основатель проекта:</b> @ghostfaccee',
        'info' : '<b>N​o​d​e​X.​a​i</b> — проект с открытым исходным кодом, основателем и разработчиком которого является @ghostfaccee.\n\n<b>У проекта имеется лицензия AGPL-3.0</b>, это значит, что он является свободным программным обеспечением, и все его производные версии, включая облачные сервисы, также должны распространяться с открытым кодом.\n\n<b>Этот бот является оригинальным и вы можете доверять ему</b>, так как он неразрывно связан с <a href="https://github.com/NodeX-AI/NodeX.ai">открытым официальным репозиторием</a>.\n\n<b>Ваша переписка с нейросетевой моделью надежно шифруется алгоритмом AES-256-GCM и сохраняется в базе данных</b> <a href="https://telegra.ph/Politika-konfidencialnosti-telegram-bota-NodeXai-11-01">(см. Политику конфиденциальности).</a>\n\n<b>Сервис предоставляется "как есть" (AS IS). Полные условия, включая ограничение ответственности и правила использования, изложены в</b> <a href="https://telegra.ph/POLZOVATELSKOE-SOGLASHENIE-telegarm-bota-NodeXai-11-01">Пользовательском соглашении</a> <b>и</b> <a href="https://telegra.ph/OGRANICHENIE-OTVETSTVENNOSTI-telegram-bota-NodeXai-11-01">Политике ограничения ответственности</a>\n\n<b>Вы в полном праве удалить свой аккаунт и отозвать принятые соглашения, используя раздел "Опасная зона" в меню: /menu</b>',
        'faq' : '<b>Ответы на часто задаваемые вопросы вы можете посмотреть по <a href="https://telegra.ph/CHaVo--Telegram-bot-NodeXai-11-01">ссылке</a></b>',
        'models' : '<b>Список доступных моделей:</b>\n • <b>Gemma 3</b> - современная базовая нейросеть от компании <i>Google DeepMind</i>.\n • <b>DeepSeek R1T2 Chimera</b> - нейросеть от компании <i>TNG Technology Consulting GmbH</i>, построенная на экспериментальной архитектуре, где разные блоки специализируются на разных типах задач.',
        'change_model' : '<b>Выберите модель:</b>',
        'new_model' : '<b>Модель успешно изменена на {new_model}</b>',
        'menu' : '<b>Меню:</b>',
        'my_profile' : '<b>Ваш профиль</b>\n • <b>ID:</b> <tg-spoiler>{id}</tg-spoiler>\n • <b>Текущая модель:</b> {current_model}\n • <b>Количество сообщений:</b> {message_count}\n • <b>Зарегистрирован:</b> {created_str}',
        'statistics' : '<b>Глобальная статистика:</b>\n • <b>Зарегистрированных пользователей:</b> {total_users}\n • <b>Всего сообщений:</b> {total_messages}\n • <b>Популярная модель:</b> {popular_model}',
        'danger_zone' : '<b>Опасная зона. Будьте аккуратнее с выбором.</b>',
        'delete' : '<b>Вы хотите удалить {delete}</b>. Вы уверены в своем выборе?',
        'mes_deleted' : '<b>История ваших сообщение успешна удалена</b>',
        'acc_deleted' : '<b>Ваш аккаунт упешно удален.</b> Чтобы продолжить пользоваться функциями бота нужно зарегистрироваться через команду /start',
        'command_rate_limit' : '⏳ <b>Подождите секунду перед использованием следующей команды</b>',
        'callback_rate_limit' : '⏳ <b>Подождите секунду перед использованием следующей кнопки</b>',
        'remaining_time' : '⏳ <b>Следующий запрос через {remaining_time} секунд</b>',
        'request_processing' : '🔄 <b>Ваш предыдущий запрос еще обрабатывается.</b> Пожалуйста, дождитесь конца обработки предыдущего запроса.',
    },
}

WARNINGS = {
    'ru' : {
        # middleware/registration_middleware.py
        'not_registered' : 'Вы не зарегистрированы. Зарегистрируйтесь, используя /start',
    }
}

ERRORS = {
    'ru' : {
        # services/api_requests.py
        'unexpected' : '❌ Непредвиденная ошибка. <a href="t.me/NodeX_project?direct">Пожалуйста, направьте ошибку разработчику</a>.',
        'timeout' : '❌ Таймаут: запрос обрабатывался слишком долго. Попробуйте сменить модель или подождать и отрпавить запрос снова. Скорее всего, модель в данный момент времени перегружена пользователями и не может ответить на запрос.',
        'api_err' : '❌ Произошла ошибка API. Скорее всего, что-то произошло с API или количество запросов данной модели за день было исчерпано. Вы можете попытаться сменить модель. <a href="t.me/NodeX_project?direct">Пожалуйста, направьте эту ошибку разработчику.</a>',
        # middleware/error_logging_middleware.py
        'error_in_handler' : '❌ Произошла ошибка. Пожалуйста, направьте ее разработчику по ссылке t.me/NodeX_project?direct'
    }
}

def get_warn(warn_key: str, **kwargs) -> str:
    language = 'ru'
    text = WARNINGS[language][warn_key]
    return text.format(**kwargs) if kwargs else text

def get_error(error_key: str, **kwargs) -> str:
    language = 'ru'
    text = ERRORS[language][error_key]
    return text.format(**kwargs) if kwargs else text

def get_text(text_key: str, **kwargs) -> str:
    language = 'ru'
    text = MESSAGES[language][text_key]
    return text.format(**kwargs) if kwargs else text
