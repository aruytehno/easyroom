import random
from PIL import Image, ImageDraw


class RoomLayoutGenerator:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.room_width = width - 100
        self.room_height = height - 100
        self.image = Image.new('RGB', (width, height), 'white')
        self.draw = ImageDraw.Draw(self.image)

        # Цвета для элементов
        self.colors = {
            'wall': '#2c3e50',
            'door': '#8b4513',
            'window': '#3498db',
            'furniture': '#e74c3c',
            'text': '#000000'
        }

    def draw_room(self):
        # Рисуем стены комнаты
        room_x = 50
        room_y = 50
        self.draw.rectangle(
            [room_x, room_y, room_x + self.room_width, room_y + self.room_height],
            outline=self.colors['wall'], width=3, fill='#ecf0f1'
        )
        return room_x, room_y

    def draw_door(self, room_x, room_y):
        # Случайное размещение двери на одной из стен
        wall = random.choice(['top', 'bottom', 'left', 'right'])
        door_width = 40
        door_height = 60

        if wall == 'top':
            door_x = random.randint(room_x + 20, room_x + self.room_width - door_width - 20)
            door_y = room_y
            self.draw.rectangle([door_x, door_y, door_x + door_width, door_y + door_height],
                                fill=self.colors['door'], outline='black', width=1)

        elif wall == 'bottom':
            door_x = random.randint(room_x + 20, room_x + self.room_width - door_width - 20)
            door_y = room_y + self.room_height - door_height
            self.draw.rectangle([door_x, door_y, door_x + door_width, door_y + door_height],
                                fill=self.colors['door'], outline='black', width=1)

        elif wall == 'left':
            door_x = room_x
            door_y = random.randint(room_y + 20, room_y + self.room_height - door_height - 20)
            self.draw.rectangle([door_x, door_y, door_x + door_height, door_y + door_width],
                                fill=self.colors['door'], outline='black', width=1)

        else:  # right
            door_x = room_x + self.room_width - door_height
            door_y = random.randint(room_y + 20, room_y + self.room_height - door_width - 20)
            self.draw.rectangle([door_x, door_y, door_x + door_height, door_y + door_width],
                                fill=self.colors['door'], outline='black', width=1)

        # Ручка двери
        handle_x = door_x + door_width // 2 + 5 if wall in ['top', 'bottom'] else door_x + door_height // 2 + 5
        handle_y = door_y + door_height // 2
        self.draw.ellipse([handle_x - 3, handle_y - 3, handle_x + 3, handle_y + 3], fill='gold')

    def draw_window(self, room_x, room_y):
        # Случайное размещение окна (не на той же стене, что и дверь, для реалистичности)
        wall = random.choice(['top', 'bottom', 'left', 'right'])
        window_length = 60

        if wall == 'top':
            window_x = random.randint(room_x + 60, room_x + self.room_width - window_length - 60)
            window_y = room_y
            self.draw.rectangle([window_x, window_y, window_x + window_length, window_y + 15],
                                fill=self.colors['window'], outline='black', width=1)

        elif wall == 'bottom':
            window_x = random.randint(room_x + 60, room_x + self.room_width - window_length - 60)
            window_y = room_y + self.room_height - 15
            self.draw.rectangle([window_x, window_y, window_x + window_length, window_y + 15],
                                fill=self.colors['window'], outline='black', width=1)

        elif wall == 'left':
            window_x = room_x
            window_y = random.randint(room_y + 60, room_y + self.room_height - window_length - 60)
            self.draw.rectangle([window_x, window_y, window_x + 15, window_y + window_length],
                                fill=self.colors['window'], outline='black', width=1)

        else:  # right
            window_x = room_x + self.room_width - 15
            window_y = random.randint(room_y + 60, room_y + self.room_height - window_length - 60)
            self.draw.rectangle([window_x, window_y, window_x + 15, window_y + window_length],
                                fill=self.colors['window'], outline='black', width=1)

        # Разделители окна
        if wall in ['top', 'bottom']:
            self.draw.line([window_x + window_length // 2, window_y,
                            window_x + window_length // 2, window_y + 15], fill='white', width=1)
        else:
            self.draw.line([window_x, window_y + window_length // 2,
                            window_x + 15, window_y + window_length // 2], fill='white', width=1)

    def draw_furniture(self, room_x, room_y):
        # Случайное количество предметов мебели (от 2 до 6)
        furniture_types = ['table', 'chair', 'bed', 'sofa', 'wardrobe']
        num_items = random.randint(2, 6)

        for i in range(num_items):
            item_type = random.choice(furniture_types)
            item_width = random.randint(40, 120)
            item_height = random.randint(40, 120)

            # Случайная позиция внутри комнаты (с отступом от стен)
            item_x = random.randint(room_x + 20, room_x + self.room_width - item_width - 20)
            item_y = random.randint(room_y + 20, room_y + self.room_height - item_height - 20)

            # Рисуем мебель
            self.draw.rectangle([item_x, item_y, item_x + item_width, item_y + item_height],
                                fill=self.colors['furniture'], outline='black', width=2)

            # Подпись типа мебели
            self.draw.text((item_x + 5, item_y + 5), item_type[:3].upper(),
                           fill=self.colors['text'], font=None)

    def generate(self):
        # Рисуем комнату
        room_x, room_y = self.draw_room()

        # Рисуем дверь
        self.draw_door(room_x, room_y)

        # Рисуем окно
        self.draw_window(room_x, room_y)

        # Рисуем мебель
        self.draw_furniture(room_x, room_y)

        # Добавляем заголовок
        self.draw.text((self.width // 2 - 100, 20), "Room Layout",
                       fill=self.colors['text'], font=None)

        return self.image

    def show(self):
        self.image.show()

    def save(self, filename="room_layout.png"):
        self.image.save(filename)
        print(f"Сохранено как {filename}")


def main():
    # Создаем генератор
    generator = RoomLayoutGenerator()

    # Генерируем планировку
    layout = generator.generate()

    # Показываем результат
    generator.show()

    # Сохраняем в файл
    generator.save()

    print("Планировка сгенерирована!")
    print("- Комната с четырьмя стенами")
    print("- Дверь в случайном месте")
    print("- Окно в случайном месте")
    print("- Случайное количество мебели")


if __name__ == "__main__":
    main()