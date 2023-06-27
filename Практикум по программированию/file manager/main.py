import os
import shutil
import json

root_path = os.getcwd()


def read_workspace_from_settings():
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file)
            workspace_path = settings.get('workspace_path')
            return workspace_path
    except FileNotFoundError:
        print("Файл настроек не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла настроек: {e}")

    return None


def initialize_workspace():
    if not os.path.exists('settings.json'):
        print("Файл настроек не найден.")
        return

    workspace_path = read_workspace_from_settings()
    if workspace_path is not None and os.path.isdir(workspace_path):
        os.chdir(workspace_path)
        print(f"Рабочая папка установлена: {root_path}")
    else:
        print("Указанный путь к рабочей папке недействителен.")


def create_folder(name):
    try:
        folder_path = os.path.join(os.getcwd(), name)  # Получаем полный путь к новой папке
        if not os.path.abspath(folder_path).startswith(root_path):
            print("Вы не можете создать папку за пределами рабочей папки.")
            return
        os.mkdir(folder_path)  # Создаем папку по указанному пути
        print(f"Папка '{name}' успешно создана.")
    except FileExistsError:
        print(f"Папка '{name}' уже существует.")
    except Exception as e:
        print(f"Ошибка при создании папки '{name}': {e}")


def delete_folder(name):
    try:
        folder_path = os.path.join(os.getcwd(), name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            if not os.path.abspath(folder_path).startswith(root_path):
                print("Вы не можете удалить папку за пределами рабочей папки.")
                return
            os.rmdir(folder_path)
            print(f"Папка '{name}' успешно удалена.")
        else:
            print(f"Папка '{name}' не найдена.")
    except OSError as e:
        print(f"Ошибка при удалении папки '{name}': {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def change_directory(path):
    try:
        new_path = os.path.join(os.getcwd(), path)  # Получаем новый путь
        if not os.path.abspath(new_path).startswith(root_path):
            print("Вы не можете выйти за пределы рабочей папки.")
            return
        os.chdir(new_path)  # Изменяем текущую рабочую папку на указанную
        print(f"Текущая папка: {os.getcwd()}")
    except FileNotFoundError:
        print(f"Папка '{path}' не найдена.")
    except NotADirectoryError:
        print(f"'{path}' не является директорией.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def go_up():
    try:
        current_dir = os.getcwd()  # Получаем текущую рабочую папку
        parent_dir = os.path.dirname(current_dir)  # Получаем путь к родительской папке
        if not os.path.abspath(parent_dir).startswith(root_path):
            print("Вы не можете выйти за пределы рабочей папки.")
            return
        os.chdir(parent_dir)  # Изменяем текущую рабочую папку на родительскую папку
        print(f"Текущая папка: {os.getcwd()}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def create_file(file_name):
    try:
        file_path = os.path.join(os.getcwd(), file_name)  # Получаем полный путь к файлу
        if not os.path.abspath(file_path).startswith(root_path):
            print("Вы не можете создать файл за пределами рабочей папки.")
            return
        with open(file_path, 'w'):  # Открываем файл в режиме записи ('w'), создавая его при необходимости
            pass  # Пустой блок, файл будет создан и сразу закрыт
        print(f"Файл '{file_name}' успешно создан.")
    except FileExistsError:
        print(f"Файл '{file_name}' уже существует.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def write_to_file(file_name, text):
    try:
        file_path = os.path.join(os.getcwd(), file_name)  # Получаем полный путь к файлу
        if not os.path.abspath(file_path).startswith(root_path):
            print("Вы не можете изменять файл за пределами рабочей папки.")
            return
        with open(file_path, 'w') as file:  # Открываем файл в режиме записи ('w')
            file.write(text)  # Записываем текст в файл
        print(f"Текст успешно записан в файл '{file_name}'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def view_file(file_name):
    try:
        file_path = os.path.join(os.getcwd(), file_name)  # Получаем полный путь к файлу
        if not os.path.abspath(file_path).startswith(root_path):
            print("Вы не можете просматривать файл за пределами рабочей папки.")
            return
        with open(file_path, 'r') as file:  # Открываем файл в режиме чтения ('r')
            content = file.read()  # Читаем содержимое файла
        print(f"Содержимое файла '{file_name}':\n{content}")
    except FileNotFoundError:
        print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def delete_file(file_name):
    try:
        file_path = os.path.join(os.getcwd(), file_name)  # Получаем полный путь к файлу
        if not os.path.abspath(file_path).startswith(root_path):
            print("Вы не можете удалять файл за пределами рабочей папки.")
            return
        os.remove(file_path)  # Удаляем файл
        print(f"Файл '{file_name}' успешно удален.")
    except FileNotFoundError:
        print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def copy_file(source_folder, destination_folder, file_name):
    try:
        source_path = os.path.join(os.getcwd(), source_folder, file_name)
        destination_path = os.path.join(os.getcwd(), destination_folder, file_name)
        if (
            not os.path.abspath(source_path).startswith(root_path)
            or not os.path.abspath(destination_path).startswith(root_path)
        ):
            print("Вы не можете копировать файл за пределами рабочей папки.")
            return
        shutil.copy2(source_path, destination_path)
        print(f"Файл '{file_name}' успешно скопирован из папки '{source_folder}' в папку '{destination_folder}'.")
    except FileNotFoundError:
        print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def move_file(source_folder, destination_folder, file_name):
    try:
        source_path = os.path.join(os.getcwd(), source_folder, file_name)
        destination_path = os.path.join(os.getcwd(), destination_folder, file_name)
        if (
            not os.path.abspath(source_path).startswith(root_path)
            or not os.path.abspath(destination_path).startswith(root_path)
        ):
            print("Вы не можете перемещать файл за пределами рабочей папки.")
            return
        shutil.move(source_path, destination_path)
        print(f"Файл '{file_name}' успешно перемещен из папки '{source_folder}' в папку '{destination_folder}'.")
    except FileNotFoundError:
        print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def rename_file(old_name, new_name):
    try:
        old_path = os.path.join(os.getcwd(), old_name)
        new_path = os.path.join(os.getcwd(), new_name)
        if (
            not os.path.abspath(old_path).startswith(root_path)
            or not os.path.abspath(new_path).startswith(root_path)
        ):
            print("Вы не можете переименовывать файл за пределами рабочей папки.")
            return
        os.rename(old_path, new_path)
        print(f"Файл '{old_name}' успешно переименован в '{new_name}'.")
    except FileNotFoundError:
        print(f"Файл '{old_name}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


initialize_workspace()

while True:
    command = input("Введите команду: ")
    print(f"Вы ввели команду: {command}")

    if command == "Создать папку":
        folder_name = input("Введите имя папки: ")
        print(f"Вы ввели имя папки: {folder_name}")
        create_folder(folder_name)

    elif command == "Удалить папку":
        folder_name = input("Введите имя папки: ")
        print(f"Вы ввели имя папки: {folder_name}")
        delete_folder(folder_name)

    elif command == "Открыть папку":
        folder_name = input("Введите имя папки: ")
        print(f"Вы ввели имя папки: {folder_name}")
        change_directory(folder_name)

    elif command == "Выйти из папки":
        go_up()

    elif command == "Создать файл":
        file_name = input("Введите имя файла: ")
        print(f"Вы ввели имя файла: {file_name}")
        create_file(file_name)

    elif command == "Записать в файл":
        file_name = input("Введите имя файла: ")
        text = input("Введите текст для записи: ")
        print(f"Вы ввели имя файла: {file_name}")
        print(f"Вы ввели текст: {text}")
        write_to_file(file_name, text)

    elif command == "Просмотреть файл":
        file_name = input("Введите имя файла: ")
        print(f"Вы ввели имя файла: {file_name}")
        view_file(file_name)

    elif command == "Удалить файл":
        file_name = input("Введите имя файла: ")
        print(f"Вы ввели имя файла: {file_name}")
        delete_file(file_name)

    elif command == "Скопировать файл":
        source_folder = input("Введите имя папки источника: ")
        destination_folder = input("Введите имя целевой папки: ")
        file_name = input("Введите имя файла: ")
        print(f"Вы ввели имя папки источника: {source_folder}")
        print(f"Вы ввели имя целевой папки: {destination_folder}")
        print(f"Вы ввели имя файла: {file_name}")
        copy_file(source_folder, destination_folder, file_name)

    elif command == "Переместить файл":
        source_folder = input("Введите имя папки источника: ")
        destination_folder = input("Введите имя целевой папки: ")
        file_name = input("Введите имя файла: ")
        print(f"Вы ввели имя папки источника: {source_folder}")
        print(f"Вы ввели имя целевой папки: {destination_folder}")
        print(f"Вы ввели имя файла: {file_name}")
        move_file(source_folder, destination_folder, file_name)

    elif command == "Переименовать файл":
        old_name = input("Введите старое имя файла: ")
        new_name = input("Введите новое имя файла: ")
        print(f"Вы ввели старое имя файла: {old_name}")
        print(f"Вы ввели новое имя файла: {new_name}")
        rename_file(old_name, new_name)

    elif command == "Выйти":
        print("До свидания!")
        break

    else:
        print("Неизвестная команда. Пожалуйста, попробуйте снова.")
