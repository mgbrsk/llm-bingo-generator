from PIL import Image, ImageDraw, ImageFont


class ImageProcessor:
    def __init__(self):
        pass

    @staticmethod
    def _get_text_size(text, font, draw):
        bbox = draw.textbbox((0, 0), text, font=font)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])

    @staticmethod
    def _word_wrap(text, font, max_width, draw):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = word if not current_line else (current_line + " " + word)
            line_w, _ = ImageProcessor._get_text_size(test_line, font, draw)

            if line_w <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    @staticmethod
    def generate_card(
        cell_card_amount,
        texts,
        filename="bingo_card.png",
        cell_size=150,
        margin=20,
        title="Title",
        title_padding=10,
        line_spacing=4,
    ):
        """
        Генерирует PNG с сеткой (cell_card_amount x cell_card_amount), заголовком и
        надписями в каждой ячейке, учитывая перенос слов по строкам.

        Args:
            cell_card_amount (int): размер сетки (n x n).
            texts (list): список текстов (должен иметь n*n элементов).
            filename (str): имя выходного файла (PNG).
            cell_size (int): размер одной ячейки в пикселях.
            margin (int): общий отступ (рамка) по краям изображения в пикселях.
            title (str): текст заголовка.
            title_padding (int): расстояние между заголовком и началом сетки.
            line_spacing (int): расстояние между строками внутри одной ячейки.
        """
        if len(texts) != cell_card_amount * cell_card_amount:
            raise ValueError(
                f"Длина списка texts должна быть {cell_card_amount * cell_card_amount}, "
                f" получено {len(texts)}. {texts=}"
            )

        # Подбор размера заголовка.
        temp_img = Image.new("RGB", (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)

        # Пытаемся загрузить шрифт; если не находим, берём встроенный PIL-шрифт
        try:
            font = ImageFont.truetype("arial.ttf", 18)
        except OSError:
            font = ImageFont.load_default()

        # Размеры заголовка
        title_bbox = temp_draw.textbbox((0, 0), title, font=font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]

        # Размер внутренней сетки
        grid_width = cell_card_amount * cell_size
        grid_height = cell_card_amount * cell_size

        # Итоговый размер
        total_width = margin * 2 + grid_width
        total_height = margin + title_height + title_padding + grid_height + margin

        # Создаём итоговое изображение
        img = Image.new("RGB", (total_width, total_height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Заголовок
        title_x = (total_width - title_width) / 2
        title_y = margin
        draw.text((title_x, title_y), title, font=font, fill=(0, 0, 0))

        # Координаты сетки
        grid_top = margin + title_height + title_padding
        grid_left = margin
        line_color = (0, 0, 0)

        # Линии сетки
        for i in range(cell_card_amount + 1):
            # Горизонтальные
            y = grid_top + i * cell_size
            draw.line(
                (grid_left, y, grid_left + grid_width, y), fill=line_color, width=2
            )

            # Вертикальные
            x = grid_left + i * cell_size
            draw.line(
                (x, grid_top, x, grid_top + grid_height), fill=line_color, width=2
            )

        for row in range(cell_card_amount):
            for col in range(cell_card_amount):
                text = texts[row * cell_card_amount + col]

                x1 = grid_left + col * cell_size
                y1 = grid_top + row * cell_size

                # Перенос слов.
                max_text_width = cell_size - 10
                lines = ImageProcessor._word_wrap(text, font, max_text_width, draw)

                # Считаем общую высоту всего многострочного текста
                line_heights = []
                for line in lines:
                    lw, lh = ImageProcessor._get_text_size(line, font, draw)
                    line_heights.append(lh)
                total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)

                current_y = y1 + (cell_size - total_text_height) / 2

                # Выравнивание
                for _, line in enumerate(lines):
                    lw, lh = ImageProcessor._get_text_size(line, font, draw)
                    line_x = x1 + (cell_size - lw) / 2
                    draw.text((line_x, current_y), line, font=font, fill=(0, 0, 0))

                    current_y += lh + line_spacing

        # Сохраняем картинку
        img.save(filename)
        print(f"Бинго-карта сохранена в файле '{filename}'.")
