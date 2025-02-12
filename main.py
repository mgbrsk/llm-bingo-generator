import logging
from src.pipelines.bingo_pipeline import BingoPipeline

import click


@click.command()
@click.option(
    "--model_id",
    default="deepseek-r1-distill-qwen-7b",
    help="Модель, которую будем использовать.",
)
@click.option("--temperature", default=0.7, type=float, help="Температура модели.")
@click.option(
    "--cell_card_amount",
    default=5,
    type=int,
    help="Количество ячеек в строке/столбце карты.",
)
@click.option(
    "--texts",
    default="кот",
    help="Текст по которому генерируется карта.",
)
@click.option("--log_level", default="INFO", help="Уровень логирования.")
def main(
    model_id: str, temperature: float, cell_card_amount: int, texts: str, log_level: str
):
    # Инициализация логгера
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Недопустимый уровень логирования: {log_level}")
    logging.basicConfig(level=numeric_level)

    logging.info("Run BingoPipeline pipeline.")

    bingo_pipeline = BingoPipeline(model_id=model_id, temperature=temperature)
    bingo_pipeline.create_bingo_card(cell_card_amount=cell_card_amount, texts=texts)


if __name__ == "__main__":
    main()
