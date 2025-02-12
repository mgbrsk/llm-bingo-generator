from PIL import Image, ImageDraw, ImageFont


class ImageProcessor:
    def __init__(self):
        pass

    def generate_card(
        cell_card_amount,
        texts,
        filename="bingo_card.png",
        cell_size=150,
        margin=20,
        title="Title",
        title_padding=10,
    ):
        """
                Генерирует изображение PNG с сеткой cell_card_amount x cell_card_amount
                с заголовком и надписями в каждой ячейке.
        W
                Args:
                    n (int): размер сетки (n x n).
                    texts (list): список текстов (должен иметь n*n элементов).
                    filename (str): имя файла.
                    cell_size (int): размер одной ячейки в пикселях.
                    margin (int): рамка по краям изображения в пикселях.
                    title (str): текст заголовка, который будет нарисован над сеткой.
                    title_padding (int): расстояние между заголовком и началом сетки.
        """
        if len(texts) != cell_card_amount * cell_card_amount:
            raise ValueError(
                f"Длина списка texts должна быть {cell_card_amount * cell_card_amount}, а получено {len(texts)}."
            )

        # Размер сетки
        grid_width = cell_card_amount * cell_size
        grid_height = cell_card_amount * cell_size

        # Подбираем размер заголовка
        temp_img = Image.new("RGB", (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)

        try:
            font = ImageFont.truetype("arial.ttf", 18)
        except OSError:
            font = ImageFont.load_default()

        # Размер заголовка в итоге.
        title_bbox = temp_draw.textbbox((0, 0), title, font=font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]

        total_width = margin * 2 + grid_width
        total_height = margin + title_height + title_padding + grid_height + margin

        img = Image.new("RGB", (total_width, total_height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Заголовок.
        title_x = (total_width - title_width) / 2
        title_y = margin
        draw.text((title_x, title_y), title, font=font, fill=(0, 0, 0))

        # Отрисовка сетки.
        grid_top = margin + title_height + title_padding
        grid_left = margin

        # Линии сетки
        for i in range(cell_card_amount + 1):
            # Горизонтальная линия
            y = grid_top + i * cell_size
            draw.line(
                (grid_left, y, grid_left + grid_width, y), fill=(0, 0, 0), width=2
            )

            # Вертикальная линия.
            x = grid_left + i * cell_size
            draw.line((x, grid_top, x, grid_top + grid_height), fill=(0, 0, 0), width=2)

        # Текст ячеек.
        for row in range(cell_card_amount):
            for col in range(cell_card_amount):
                text = texts[row * cell_card_amount + col]

                # Координаты верхнего левого угла ячейки.
                x1 = grid_left + col * cell_size
                y1 = grid_top + row * cell_size

                # Определяем размеры текста для центрирования.
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]

                text_x = x1 + (cell_size - text_w) / 2
                text_y = y1 + (cell_size - text_h) / 2

                draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

        # Сохраняем картинку.
        img.save(filename)
        print(f"Бинго-карта сохранена в файле '{filename}'.")
