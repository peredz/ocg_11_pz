# README

## Обзор
Это Telegram-бот, предназначенный для предоставления советов о том, как избежать зависимости от цифровых устройств и технологий. Бот отвечает на различные команды и текстовые сообщения, предлагая советы и информацию, чтобы помочь пользователям эффективно управлять своим цифровым потреблением.

## Особенности
- **Приветственное сообщение:** Отправляет приветственное сообщение и отображает главное меню, когда пользователи запускают бота.
- **Текстовые ответы:** Предоставляет подробную информацию по различным темам, связанным с избеганием цифровой зависимости.
- **Пользовательская клавиатура:** Отображает пользовательскую клавиатуру с предопределенными опциями для удобной навигации.

## Установка
Для запуска этого бота вам нужно установить Python и библиотеку `pyTelegramBotAPI` (telebot).

1. Клонируйте этот репозиторий или загрузите файл скрипта.
2. Установите необходимую библиотеку:
   ```bash
   pip install pyTelegramBotAPI
   ```
3. Замените `TOKEN` на токен вашего бота, полученный от BotFather в Telegram.

## Использование
Запустите скрипт с помощью Python:
```bash
python bot_dla_ocg.py
```

## Команды и взаимодействие
- **/start или /help:** Отправляет приветственное сообщение и показывает главное меню.
- **Текстовые команды:** Бот отвечает на конкретные текстовые запросы подробными советами. Доступные команды:
  - Определение зависимости
  - Установление границ
  - Развитие других интересов
  - Осознанное использование
  - Социальные связи в реальной жизни
  - Цифровой детокс
  - Обращение за помощью
  - Полезные статьи

## Структура бота
### Основные обработчики
- `send_welcome(message)`: Обрабатывает команды `/start` и `/help`, отправляет приветственное сообщение и отображает главное меню.
- `msg(message)`: Обрабатывает текстовые сообщения, проверяет ввод и вызывает соответствующую функцию для отправки подробных советов.

### Вспомогательные функции
- `Definition_of_Dependency(message)`: Отправляет информацию о цифровой зависимости.
- `Setting_Boundaries(message)`: Отправляет советы по установлению границ для использования устройств.
- `Developing_Other_Interests(message)`: Объясняет важность развития других интересов.
- `Mindful_Usage(message)`: Предоставляет советы по осознанному использованию технологий.
- `Strengthening_Real_life_Social_Connections(message)`: Дает советы по укреплению социальных связей в реальной жизни.
- `Digital_Detox(message)`: Объясняет, что такое цифровой детокс и как его провести.
- `Seeking_PProfessional_Help(message)`: Советует, когда стоит обратиться за профессиональной помощью.
- `Usefull_articles(message)`: Делится ссылками на полезные статьи.
- `main_mess_show(message)`: Отображает главное меню с предопределенными опциями.

## Пример
Когда пользователь запускает бота с помощью команды `/start` или `/help`, бот отвечает:
```
Привет <Имя пользователя>
Это бот для советов по теме Как избегать зависимости от цифровых устройств и технологий
```
Затем бот показывает пользовательскую клавиатуру с опциями, такими как "Определение зависимости", "Установление границ" и т.д. Если пользователь выбирает "Определение зависимости", бот отвечает:
```
<b>Что такое зависимость от цифровых устройств?</b>

Чрезмерное использование смартфонов, компьютеров, планшетов и других гаджетов.
Невозможность контролировать время, проведенное за экраном.
Пренебрежение важными аспектами жизни (работа, учеба, личные отношения) ради использования цифровых устройств.
```

## Обработка ошибок
Бот включает базовый блок try-except для обработки любых неожиданных ошибок во время опроса.

```python
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        pass
```

## Лицензия
Этот проект лицензирован по лицензии MIT.

## Вклад
Вы можете форкнуть этот репозиторий и вносить изменения, отправляя pull requests. Для значительных изменений сначала откройте issue, чтобы обсудить, что вы хотите изменить.

## Контакт
Для любых вопросов или предложений, пожалуйста, свяжитесь с владельцем репозитория.