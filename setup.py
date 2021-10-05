from configparser import ConfigParser
import os

config = ConfigParser()

def validate_choice(answer, options, lang=None):
    if answer in options:
        return answer
    else:
        if not lang:
            lang = 0
        print((f"Choice isn't valid. Please, select an option in range of {options}", f"Выбранный вариант не поддерживается. Пожалуйста, введите число в диапазоне {options}")[lang])
        answer = int(input("> ")) if isinstance(answer, int) else input("> ")
        return validate_choice(answer, options, lang=lang)


def main():
    print("Select a language. It will be used later on in the bot/Выберите язык. Он впоследствии будет использован в боте")
    print("[1]: English\n[2]: Русский")
    lang = validate_choice(int(input("> ")), [1, 2]) - 1
    print(("Selected language: English", "Выбранный язык: Русский")[lang])
    print(("Enter your discord bot token: ", "Введите токен дискорд бота: ")[lang])
    token = input("> ")
    print(("Make sure your token is valid, otherwise you'll have to change it manually in the config.ini file",
           "Убедитесь в том, что токен валидный, иначе его придется менять вручную в файле config.ini")[lang])
    print(("Now select a prefix for your commands, like ! or $. Making your prefix a letter may cause some issues",
           "Теперь выберите "
           "префикс для Ваших команд, например ! или $. Назначение префикса буквой может вызвать некоторые проблемы")[lang])
    prefix = input("> ")

    config["Bot"] = {
        'token': token,
        'prefix': prefix,
        'lang': lang
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(("You're good to go! You can launch the bot via running the main.py file", "Настройка завершена! Вы можете запустить бота запустив файл main.py")[lang])
    print(("Invite the bot to your server with this link: {}")[lang])

main()