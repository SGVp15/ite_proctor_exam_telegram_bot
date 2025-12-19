import re


class Question:
    def __init__(self,
                 id_question: str = '',
                 text_question: str = '',
                 ans_a: str = '',
                 ans_b: str = '',
                 ans_c: str = '',
                 ans_d: str = '',
                 image: str = '',
                 box_question: int = 0,
                 category: str = '',
                 exam: str = '',
                 ):
        self.id_question: str = id_question
        self.text_question: str = text_question
        self.ans_a: str = ans_a
        self.ans_b: str = ans_b
        self.ans_c: str = ans_c
        self.ans_d: str = ans_d
        self.image: str = image
        self.box_question: int = box_question
        self.category: str = category
        self.exam: str = exam

    def __str__(self):
        return (f'{self.text_question}\t'
                f'{self.ans_a}\t'''
                f'{self.ans_b}\t'''
                f'{self.ans_c}\t'''
                f'{self.ans_d}\t'''
                f'{self.image}\t')

    def __eq__(self, other):
        def clean(s):
            s = re.sub(r'\s','',s)
            return s
        if not isinstance(other, Question):
            return NotImplemented

        # 2. Сравниваем текст вопроса
        question_text_equal = clean(self.text_question) == clean(other.text_question)

        # 3. Сравниваем варианты ответов как множества
        # Создаём множества из вариантов ответов для каждого объекта

        self_answers = {clean(self.ans_a), clean(self.ans_b), clean(self.ans_c), clean(self.ans_d)}
        other_answers = {clean(other.ans_a), clean(other.ans_b), clean(other.ans_c), clean(other.ans_d)}

        # Варианты ответов равны, если множества равны
        # (т.е. содержат одинаковые строки, независимо от того, какой из них был ans_a, ans_b, и т.д.)
        answers_set_equal = self_answers == other_answers

        # Вопросы равны, если равны текст вопроса И множество ответов
        return question_text_equal and answers_set_equal
