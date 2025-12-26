import subprocess
import sys
import os


def run_blender_script(blender_path, script_path):
    """
    Запускает скрипт в Blender из командной строки
    """
    # Команда для запуска
    cmd = [
        blender_path,
        "--background",
        "--python", script_path
    ]

    try:
        print(f"Запуск Blender с скриптом: {script_path}")

        # Используем правильную кодировку для Windows
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',  # Игнорировать ошибки кодировки
            check=True
        )

        print("Вывод Blender:")
        print(result.stdout)
        if result.stderr:
            print("Ошибки:")
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Пути к файлам
    blender_exe = r"C:\blender-2.91.0-windows64\blender.exe"
    test_script = r"C:\Users\simbiom\PycharmProjects\easyroom\test_scene.py"

    # Проверка существования файлов
    if not os.path.exists(blender_exe):
        print(f"Ошибка: Blender не найден по пути: {blender_exe}")
        sys.exit(1)

    if not os.path.exists(test_script):
        print(f"Ошибка: Скрипт не найден по пути: {test_script}")
        sys.exit(1)

    # Запуск
    run_blender_script(blender_exe, test_script)