import json
from src.image.image_processor import ImageProcessor
from src.models.llm_processor import UrlLlmProcessor
import logging

logger = logging.getLogger(__name__)


class BingoPipeline:
    def __init__(self, model_id: str, temperature: float):
        self.llm = UrlLlmProcessor(model_id=model_id, temperature=temperature)

    def create_bingo_card(self, cell_card_amount: int, texts: str):
        # Количество клеточек в бинго.
        variant_amount = cell_card_amount * cell_card_amount
        logger.info(f"Creating bingo card for {texts} with {variant_amount} variants.")
        # prompt_string = (
        #     f"Есть игра - в ней создают таблицу с разными событиями или свойствами определенной темы, например Чем занятся весной - спать весь день, гулять по слякоти и т.д. Или объект и его свойства, например собака - лаять на предметы, смотреть в стену и т.д."
        #     f"Придумай {variant_amount} вариантов на тему {texts}. Они должны быть смешными, с иронией. Они должны быть короткими и понятными. Они не должны быть взяты из примера."
        #     f"Ответ дай как список из {variant_amount} вариантов через запятую, без пояснений, только варианты на РУССКОМ языке."
        # )
        prompt_string = (
            f"Сгенерируй юмористическое 'бинго' с короткими, забавными и ироничными утверждениями на тему '{texts}'. "
            "Ответ должен быть на русском языке, "
            f"ровно {variant_amount} вариантов, перечисленных через запятую в одной строке, "
            "без нумерации, без пояснений и без дополнительного текста. Не длиннее 4 слов каждый вариант. "
        )

        response = self.llm.get_completions_for_promt(prompt_string)
        logger.info(f"First answer = {response["answer"]}")

        # Попробуем не чистить и взять как есть.
        splitted_response = response["answer"].split(", ")
        if len(splitted_response) != variant_amount:
            # Пробуем почистить несколько раз, но сложно.
            messages_list = [
                {
                    "role": "system",
                    "content": (
                        f"Ты форматируешь текст. Убери все цифры из текста, убери лишние пояснения и оставь только фразы через запятую. "
                        f"ответ только на русском языке (если он на другом языке - переведи на русский и оставь только русский вариант). "
                        "Доступный ответ ТОЛЬКО объект type(list). "
                        f"Длинна списка должна быть {variant_amount}."
                    ),
                },
                {
                    "role": "user",
                    "content": response["answer"],
                },
            ]
            errors = 0
            max_errors = 5
            while True:
                try:
                    clean_response = self.llm.get_completions_for_messages(
                        messages_list
                    )
                    logger.info(f"Clean response: {clean_response["answer"]}")
                    # Пробуем перевести в список.
                    bingo_text_list = json.loads(clean_response["answer"])
                    assert len(bingo_text_list) == variant_amount
                    break
                except:
                    errors += 1
                    logger.info(f"Error in cleaning. Try {errors}.")
                    if errors > max_errors:
                        raise Exception(f"Too many errors ({max_errors})")
        else:
            bingo_text_list = splitted_response
        logger.info(f"List: {bingo_text_list} (len={len(bingo_text_list)})")
        # Пробуем сгенерировать карту.
        ImageProcessor.generate_card(
            cell_card_amount=cell_card_amount,
            texts=bingo_text_list[0:variant_amount],
            filename=f"bingo_{texts}.png",
            title=texts,
        )
