# LLM генератор бинго

Work in process  
Создаёт png картинки заданного размера и заполняет текстом на заданную тему. Требует ллм (локальную или удалённую), доступную requests с методами /v1/completions и /v1/chat/completions (например поднятую через через LM Studio)

Пример использования:

```python
python main.py --cell_card_amount=4 --texts="Архитектура марса"
```
