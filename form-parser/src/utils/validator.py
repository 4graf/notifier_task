"""
Валидатор слов - Validator.
"""
import re


class Validator:
    """
    Валидатор слов.

    :ivar _validation_rules: Правила валидации.
    """

    def __init__(self):
        """
        Конструктор Validator.
        """

        self._validation_rules = (
            self._validate_length,
            self._validate_symbols,
            self._validate_repetitions
        )

    def validate(self, word: str) -> bool | str:
        """
        Проверяет слово на корректность.

        :param word: Слово.
        :return: True, если слово корректно, иначе str с ошибкой.
        """

        template_error = 'Слово не допущено: '

        for validation in self._validation_rules:
            if isinstance(result := validation(word=word), str):
                return template_error + result

        return True

    @classmethod
    def _validate_length(cls, word: str) -> bool | str:
        """
        Валидация длины слова.

        :param word: Слово.
        :return: True, если слово корректно, иначе str с ошибкой.
        """

        length = len(word)
        if length <= 3:
            return f'Длина слова слишком мала и равна {length} символам.'
        return True

    @classmethod
    def _validate_symbols(cls, word: str) -> bool | str:
        """
        Валидация символов слова.

        :param word: Слово.
        :return: True, если слово корректно, иначе str с ошибкой.
        """

        symbol = re.search(r'[^A-Za-z0-9.]', word)
        if symbol:
            return f'Обнаружен недопустимый символ "{symbol.group(0)}".'
        return True

    @classmethod
    def _validate_repetitions(cls, word: str) -> bool | str:
        """
        Валидация наличия подряд идущих одинаковых символов в слове.

        :param word: Слово.
        :return: True, если слово корректно, иначе str с ошибкой.
        """

        repetition = re.search(r'(.)\1{1,}', word)
        if repetition:
            return f'Обнаружено 2 идущих подряд символа "{repetition.group(0)}".'
        return True
