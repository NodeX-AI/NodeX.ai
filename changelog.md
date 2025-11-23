<li><a href="#журнал-изменений-проекта-nodexai">Changelog in Russian</a></li>
<li><a href="#nodexai-project-changelog">Changelog in English</a></li>

# Журнал изменений проекта NodeX.ai
## `v0.5 (БЕТА)` - 31.10.2025
**В этой версии бот работает практически стабильно, но не доработан.**
### С чего проект был начат:
* **Поддержка лишь двух моделей:** Gemma3 и DeepSeek R1T2 Chimera.
* **Система ограничения спама (rate_limit) через redis.** 
* **База данных Postgresql c первой миграцией.** Первая миграция выглядела так:
```
CREATE TABLE users (
    telegram_id BIGINT UNIQUE NOT NULL PRIMARY KEY,
    current_model VARCHAR(50) DEFAULT 'gemma',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(telegram_id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    model_used VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

* **Поддержка middleware и декораторов**

## `v1.0 (Первый релиз)` - 02.11.2025
**Первый релиз бота. Бот был готов в продакшн.**
### Чтобы было изменено:
* **Изменены обработчики команд и коллбеков**, в сравнении с v0.5 (БЕТА).
* **Были добавлены:** документация, политики ограничения ответственности и конфиденциальности, пользовательское соглашение и правила использования сервиса.

## `v1.5` - 09.11.2025
Улучшенная версия. Добавлена функция распознавания изображений.
### Добавлено:
* **Функция распознавания изображений.** Бот в этой версии может описать изображение, которое пользователь ему отправил.
### Изменено:
* **Были изменены документы в директории /legal**

## `v2.0` - 16.11.2025
Значительные улучшения в безопасности сервиса и добавление новых функций.

### Добавлено:
* **Промпт для изображений.** Теперь при помощи промпта пользователь задает настройки распознавания изображения модели. Он может попросить ее решить то или иное уравнение.
* **Была добавлена новая более отказоустойчивая модель.** Grok 4 Fast от компании xAI, принадлежащей Илону Маску!
### Изменено:
* **Значительные изменения в безопасности сервиса.** Сервис стал намного безопаснее для пользвоателя.

# NodeX.ai project changelog
## `v0.5 (BETA)` - October 31, 2025
**In this version, the bot is almost stable, but not yet finalized.**
### How the project started:
* **Support for only two models:** Gemma3 and DeepSeek R1T2 Chimera.
* **Spam limiting system (rate_limit) via redis.**
* **Postgresql database with first migration.** The first migration looked like this:
```
CREATE TABLE users (
telegram_id BIGINT UNIQUE NOT NULL PRIMARY KEY,
current_model VARCHAR(50) DEFAULT 'gemma',
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
id BIGSERIAL PRIMARY KEY,
user_id BIGINT NOT NULL REFERENCES users(telegram_id) ON DELETE CASCADE,
message_text TEXT NOT NULL,
ai_response TEXT NOT NULL,
model_used VARCHAR(50) NOT NULL,
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

* **Middleware and decorator support**

## `v1.0 (First release)` - 02.11.2025

**First release of the bot. The bot was ready for production.**
### Changes:
* **Command and callback handlers** have been changed, compared to v0.5 (BETA).
* **Added:** Documentation, disclaimer and privacy policies, user agreement, and terms of service.

## `v1.5` - 11/09/2025
Improved version. Image recognition functionality has been added.
### Added:
* **Image recognition functionality.** In this version, the bot can describe images sent to it by the user.
### Changed:
* **Documents in the /legal directory have been changed**

## `v2.0` - 11/16/2025
Significant security improvements and the addition of new features.

### Added:
* **Prompt for images.** The user can now use a prompt to configure the model's image recognition settings. They can ask it to solve a particular equation.
* **A new, more robust model has been added.** Grok 4 Fast from xAI, a company owned by Elon Musk!
### Changed:
* **Significant changes to service security.** The service has become much safer for users.