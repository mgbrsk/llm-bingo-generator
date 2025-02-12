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
def main(model_id: str, temperature: float, cell_card_amount: int, texts: str):
    bingo_pipeline = BingoPipeline(model_id=model_id, temperature=temperature)
    bingo_pipeline.create_bingo_card(cell_card_amount=cell_card_amount, texts=texts)


if __name__ == "__main__":
    main()
