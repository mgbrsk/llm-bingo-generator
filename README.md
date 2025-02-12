# LLM генератор бинго

Work in process  
Создаёт png картинки заданного размера и заполняет текстом на заданную тему.

Пример использования:

```python
from src.pipelines.bingo_pipeline import BingoPipeline
pipeline = BingoPipeline(model_id="deepseek-r1-distill-qwen-7b", temperature=0.7)
pipeline.create_bingo_card(2, "Чем заняться весной")
```
