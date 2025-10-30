MESSAGES = {
    'ru' : {
        'start' : 'Старт',
        'help' : 'Помощь',
        'models' : 'Список доступных моделей...',
        'change_model' : 'Сменить модель',
        'new_model' : 'Модель успешно изменена на {new_model}',
        'menu' : 'Меню',
        'my_profile' : 'Ваш профиль\nID: <tg-spoiler>{id}</tg-spoiler>\nТекущая модель: {current_model}\nКоличество сообщений: {message_count}\nЗарегистрирован: {created_str}',
        'statistics' : 'Глобальная статистика:\nЗарегистрированных пользователей: {total_users}\nВсего сообщений: {total_messages}\nПопулярная модель: {popular_model}',
        'danger_zone' : 'Опасная зона. Будьте аккуратнее с выбором.',
        'delete' : 'Вы хотите удалить {delete}. Вы уверены в своем выборе?',
        'mes_deleted' : 'История ваших сообщение успешна удалена',
        'acc_deleted' : 'Ваш аккаунт упешно удален. Чтобы продолжить пользоваться функциями бота нужно зарегистрироваться через команду /start',
        'command_rate_limit' : '⏳ Подождите секунду перед использованием следующей команды',
        'callback_rate_limit' : '⏳ Подождите секунду перед использованием следующей кнопки',
        'remaining_time' : '⏳ Следующий запрос через {remaining_time} секунд',
        'request_processing' : '🔄 Ваш предыдущий запрос еще обрабатывается. Пожалуйста, дождитесь конца обработки предыдущего запроса.',
    },
}

WARNINGS = {
    'ru' : {
        # middleware/registration_middleware.py
        'not_registered' : 'Вы не зарегистрированы. Зарегистрируйтесь, используя команду /start',
    }
}

ERRORS = {
    'ru' : {
        # services/api_requests.py
        'unexpected' : '❌ Непредвиденная ошибка. Пожалуйста, направьте ошибку разработчику и он как можно скорее ее исправит.',
        'timeout' : '❌ Таймаут: запрос обрабатывался слишком долго. Попробуйте сменить модель или подождать и отрпавить запрос снова. Скорее всего, модель в данный момент времени перегружена пользователями и не может ответить на запрос.',
        'api_err' : '❌ Произошла ошибка API. Скорее всего, что-то произошло с API. Направьте эту ошибку разработчику и он как можно скорее ее исправит.',
        # middleware/error_logging_middleware.py
        'error_in_handler' : '❌ Произошла ошибка. Пожалуйста, направьте ее разработчику.'
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
