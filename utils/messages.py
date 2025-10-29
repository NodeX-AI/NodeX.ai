MESSAGES = {
    'ru' : {
        'start' : 'Старт',
        'help' : 'Помощь',
        'models' : 'Список доступных моделей...',
        'change_model' : 'Сменить модель',
        'new_model' : 'Модель успешно изменена на {new_model}',
        'command_rate_limit' : '⏳ Подождите секунду перед использованием следующей команды',
        'remaining_time' : '⏳ Следующий запрос через {remaining_time} секунд',
        'request_processing' : '🔄 Ваш предыдущий запрос еще обрабатывается. Пожалуйста, дождитесь конца обработки предыдущего запроса.',
    },
}

ERRORS = {
    'ru' : {
        # api_requests.py
        'unexpected' : '❌ Непредвиденная ошибка. Пожалуйста, направьте ошибку разработчику и он как можно скорее ее исправит.',
        'timeout' : '❌ Таймаут: запрос обрабатывался слишком долго. Попробуйте сменить модель или подождать и отрпавить запрос снова. Скорее всего, модель в данный момент времени перегружена пользователями и не может ответить на запрос.',
        'api_err' : '❌ Произошла ошибка API. Скорее всего, что-то произошло с API. Направьте эту ошибку разработчику и он как можно скорее ее исправит.',
    }
}

def get_error(error_key: str, **kwargs) -> str:
    language = 'ru'
    text = ERRORS[language][error_key]
    return text.format(**kwargs) if kwargs else text

def get_text(text_key: str, **kwargs) -> str:
    language = 'ru'
    text = MESSAGES[language][text_key]
    return text.format(**kwargs) if kwargs else text
