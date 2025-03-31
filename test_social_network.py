import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from cuoora_social_network import *

class AnswerTest(unittest.TestCase):
    def setUp(self):
        self.answer = Answer(Question(User('pepe2', 'pepe2'), 'Sample Question', 'Description'), 
                            User('pepe', 'pepe'), 
                            'An answer'
                            )

    def test_votes_for_new_answer(self):
        self.assertEqual(len(self.answer.negative_votes()), 0)
        self.assertEqual(len(self.answer.positive_votes()), 0)

    def test_positive_votes(self):
        vote = Vote(User('pepe33', 'pepe33'), True)
        self.answer.add_vote(vote)
        self.assertEqual(len(self.answer.positive_votes()), 1)

        vote2 = Vote(User('pepe33', 'pepe33'), True)
        self.answer.add_vote(vote2)
        self.assertEqual(len(self.answer.positive_votes()), 2)

    def test_negative_votes(self):
        vote = Vote(User('pepe33', 'pepe33'), False)
        self.answer.add_vote(vote)
        self.assertEqual(len(self.answer.negative_votes()), 1)

        vote2 = Vote(User('pepe33', 'pepe33'), False)
        self.answer.add_vote(vote2)
        self.assertEqual(len(self.answer.negative_votes()), 2)

    def test_positive_and_negative_votes_interference(self):
        vote = Vote(User('pepe33', 'pepe33'), False)
        self.answer.add_vote(vote)
        self.assertEqual(len(self.answer.positive_votes()), 0)

        vote2 = Vote(User('pepe33', 'pepe33'), True)
        self.answer.add_vote(vote2)
        self.assertEqual(len(self.answer.positive_votes()), 1)

        vote3 = Vote(User('pepe33', 'pepe33'), True)
        self.answer.add_vote(vote3)
        self.assertEqual(len(self.answer.positive_votes()), 2)

        vote4 = Vote(User('pepe33', 'pepe33'), False)
        self.answer.add_vote(vote4)
        self.assertEqual(len(self.answer.positive_votes()), 2)

        self.assertEqual(len(self.answer.votes), 4)

    def test_add_votes_same_user(self):
        user = User('pepe33', 'pepe33')
        vote = Vote(user, True)
        self.answer.add_vote(vote)
        self.assertEqual(len(self.answer.positive_votes()), 1)
        vote2 = Vote(user, True)
        with self.assertRaises(ValueError):
            self.answer.add_vote(vote2)

class QuestionTest(unittest.TestCase):
    def setUp(self):
        self.user = User("test_user", "password")
        self.other_user = User("other_user", "password")
        self.question = Question(self.user, "¿Cuál es el mejor lenguaje de programación?", "Opiniones sobre lenguajes.")

        # Respuesta con 80% de votos positivos (8 positivos, 2 negativos)
        self.answer1 = Answer(self.question, self.user, "Python es el mejor.")
        for _ in range(8):
            vote = Vote(User("test_user", "password"), is_like=True)
            self.answer1.add_vote(vote)
        for _ in range(2):
            vote = Vote(User("test_user", "password"), is_like=False)
            self.answer1.add_vote(vote)

        # Respuesta con 60% de votos positivos (6 positivos, 4 negativos)
        self.answer2 = Answer(self.question, self.user, "Java es más versátil.")
        for _ in range(6):
            vote = Vote(User("test_user", "password"), is_like=True)
            self.answer2.add_vote(vote)
        for _ in range(4):
            vote = Vote(User("test_user", "password"), is_like=False)
            self.answer2.add_vote(vote)

        # Agregar respuestas al usuario
        self.user.answers.extend([self.answer1, self.answer2])

    def test_votes_for_new_question(self):
        self.assertEqual(len(self.question.negative_votes()), 0)
        self.assertEqual(len(self.question.positive_votes()), 0)

    def test_positive_votes(self):
        vote = Vote(User('pepe33', 'pepe33'), True)
        self.question.add_vote(vote)
        self.assertEqual(len(self.question.positive_votes()), 1)

        vote2 = Vote(User('pepe33', 'pepe33'), True)
        self.question.add_vote(vote2)
        self.assertEqual(len(self.question.positive_votes()), 2)

    def test_negative_votes(self):
        vote = Vote(User('pepe33', 'pepe33'), False)
        self.question.add_vote(vote)
        self.assertEqual(len(self.question.negative_votes()), 1)

        vote2 = Vote(User('pepe33', 'pepe33'), False)
        self.question.add_vote(vote2)
        self.assertEqual(len(self.question.negative_votes()), 2)

    def test_positive_and_negative_votes_interference(self):
        vote = Vote(User('pepe33', 'pepe33'), False)
        self.question.add_vote(vote)
        self.assertEqual(len(self.question.positive_votes()), 0)

        vote2 = Vote(User('pepe33', 'pepe33'), True)
        self.question.add_vote(vote2)
        self.assertEqual(len(self.question.positive_votes()), 1)

        vote3 = Vote(User('pepe33', 'pepe33'), True)
        self.question.add_vote(vote3)
        self.assertEqual(len(self.question.positive_votes()), 2)

        vote4 = Vote(User('pepe33', 'pepe33'), False)
        self.question.add_vote(vote4)
        self.assertEqual(len(self.question.positive_votes()), 2)

        self.assertEqual(len(self.question.votes), 4)

    def test_add_votes_same_user(self):
        user = User('pepe33', 'pepe33')
        vote = Vote(user, True)
        self.question.add_vote(vote)
        self.assertEqual(len(self.question.positive_votes()), 1)
        vote2 = Vote(user, True)
        with self.assertRaises(ValueError):
            self.question.add_vote(vote2)

    def test_add_topics_to_question(self):
        topic1 = Topic("Python", "A programming language")
        self.question.add_topic(topic1)
        self.assertIn(topic1, self.question.topics)
        self.assertEqual(len(self.question.topics), 1)

        topic2 = Topic("Machine Learning", "A subset of AI")
        self.question.add_topic(topic2)
        self.assertIn(topic2, self.question.topics)
        self.assertEqual(len(self.question.topics), 2)

    def test_add_duplicate_topics(self):
        topic = Topic("Python", "A programming language")
        self.question.add_topic(topic)
        with self.assertRaises(ValueError):
            self.question.add_topic(topic)
        self.assertEqual(len(self.question.topics), 1)

    def test_initialize_with_topics(self):
        topic1 = Topic("AI", "Artificial Intelligence")
        topic2 = Topic("Deep Learning", "A subset of Machine Learning")
        question_with_topics = Question(User('pepe', 'pepePWD'), 'Sample Question', 'Description', [topic1, topic2])
        self.assertIn(topic1, question_with_topics.topics)
        self.assertIn(topic2, question_with_topics.topics)
        self.assertEqual(len(question_with_topics.topics), 2)

    def test_best_answer(self):
        best_answer = self.question.get_best_answer()
        self.assertEqual(best_answer, self.answer1, "El método no retorna la mejor respuesta correctamente.")

    def test_best_answer_changed_by_positive_votes(self):
        best_answer = self.question.get_best_answer()
        self.assertEqual(best_answer, self.answer1, "El método no retorna la mejor respuesta correctamente.")

        for _ in range(5):
            vote = Vote(User("test_user", "password"), is_like=True)
            self.answer2.add_vote(vote)

        best_answer = self.question.get_best_answer()
        self.assertEqual(best_answer, self.answer2, "El método no retorna la mejor respuesta correctamente.")


    def test_best_answer_changed_by_negative_votes(self):
        best_answer = self.question.get_best_answer()
        self.assertEqual(best_answer, self.answer1, "El método no retorna la mejor respuesta correctamente.")

        for _ in range(5):
            vote = Vote(User("test_user", "password"), is_like=False)
            self.answer1.add_vote(vote)

        best_answer = self.question.get_best_answer()
        self.assertEqual(best_answer, self.answer2, "El método no retorna la mejor respuesta correctamente.")

class CuooraRetrieverTest(unittest.TestCase):

    def setUp(self):
        self.cuoora = CuOOra()
        self.user1 = User('user1', 'pass1')
        self.user2 = User('user2', 'pass2')
        self.user3 = User('user3', 'pass3')

        self.topic1 = Topic('Python', 'Programming in Python')
        self.topic2 = Topic('Django', 'Web development with Django')
        self.user1.add_topic(self.topic1)
        self.user2.add_topic(self.topic2)
        
        self.question1 = Question(self.user2, "What is Python?", "Python basics", [self.topic1])
        self.question2 = Question(self.user3, "Django best practices", "Optimizing Django apps", [self.topic2])

        yesterday = datetime.now() - timedelta(days=1)

        with patch("cuoora_social_network.datetime") as mock_datetime:
            mock_datetime.now.return_value = yesterday
            self.question3 = Question(self.user1, "Newest tech trends", "AI and ML trends", [self.topic1])
        
        self.cuoora.add_question(self.question1)
        self.cuoora.add_question(self.question2)
        self.cuoora.add_question(self.question3)
        
        self.user1.follow(self.user2)
        self.user2.follow(self.user3)

    def test_social_retrieval(self):

        retrieved_questions = self.cuoora.get_questions_for_user(self.user1, SocialRetrieverFactory(), 100)
        self.assertIn(self.question1, retrieved_questions)
        self.assertNotIn(self.question3, retrieved_questions)

        self.user1.stop_follow(self.user2)
        retrieved_questions = self.cuoora.get_questions_for_user(self.user1, SocialRetrieverFactory(), 100)
        self.assertNotIn(self.question1, retrieved_questions)

    def test_topics_retrieval(self):
        retrieved_questions = self.cuoora.get_questions_for_user(self.user2, TopicsRetrieverFactory(), 100)
        self.assertNotIn(self.question1, retrieved_questions)
        self.assertIn(self.question2, retrieved_questions)
        self.assertNotIn(self.question3, retrieved_questions)

        self.question3.add_topic(self.topic2)
        retrieved_questions = self.cuoora.get_questions_for_user(self.user2, TopicsRetrieverFactory(), 100)
        self.assertNotIn(self.question1, retrieved_questions)
        self.assertIn(self.question2, retrieved_questions)
        self.assertIn(self.question3, retrieved_questions)

        self.question1.add_topic(self.topic2)
        retrieved_questions = self.cuoora.get_questions_for_user(self.user2, TopicsRetrieverFactory(), 100)
        self.assertIn(self.question2, retrieved_questions)
        self.assertIn(self.question3, retrieved_questions)
        self.assertNotIn(self.question1, retrieved_questions)

    def test_news_retrieval(self):
        retrieved_questions = self.cuoora.get_questions_for_user(self.user3, NewsRetrieverFactory(), 100)
        self.assertIn(self.question1, retrieved_questions)
        self.assertIn(self.question2, retrieved_questions)
        self.assertNotIn(self.question3, retrieved_questions)

    def test_popular_today_retrieval(self):
        retrieved_questions = self.cuoora.get_questions_for_user(self.user3, PopularTodayRetrieverFactory(), 100)
        self.assertEqual(len(retrieved_questions), 0)

        vote = Vote(self.user2)
        self.user2.add_vote(vote)
        self.question1.add_vote(vote)
        retrieved_questions = self.cuoora.get_questions_for_user(self.user3, PopularTodayRetrieverFactory(), 100)
        self.assertIn(self.question1, retrieved_questions)

class TestUserScore(unittest.TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User("test_user", "password")
        other_user = User("other_user", "password")

        # Crear preguntas y respuestas
        self.question1 = Question(self.user, "¿Qué es Python?", "Explicación sobre Python")
        self.question2 = Question(self.user, "¿Cómo funciona la memoria en C?", "Detalles sobre memoria en C")
        
        self.answer1 = Answer(self.question1, self.user, "Python es un lenguaje interpretado.")
        self.answer2 = Answer(self.question2, self.user, "En C, la memoria se maneja con malloc y free.")

        # Crear votos
        vote1 = Vote(other_user, is_like=True)  # Voto positivo
        vote2 = Vote(other_user, is_like=False)  # Voto negativo

        # Agregar votos a preguntas
        self.question1.add_vote(vote1)  # +1 positivo → cuenta
        self.question2.add_vote(vote2)  # +1 negativo → no cuenta

        vote1 = Vote(other_user, is_like=True)  # Voto positivo
        vote2 = Vote(other_user, is_like=False)  # Voto negativo
        # Agregar votos a respuestas
        self.answer1.add_vote(vote1)  # +1 positivo → cuenta
        self.answer2.add_vote(vote2)  # +1 negativo → no cuenta

        # Asociar preguntas y respuestas al usuario
        self.user.questions = [self.question1, self.question2]
        self.user.answers = [self.answer1, self.answer2]

    def test_calculate_score(self):
        expected_score = 10 + 20  # Pregunta 1 (10) + Respuesta 1 (20)
        self.assertEqual(self.user.calculate_score(), expected_score)

    def test_calculate_score_after_new_votes(self):

        initial_expected_score = 10 + 20
        self.assertEqual(self.user.calculate_score(), initial_expected_score)

        another_user = User("new_user", "password")
        new_vote = Vote(another_user, is_like=True)  
        self.question2.add_vote(new_vote)

        another_user = User("new_user", "password")
        new_vote = Vote(another_user, is_like=True)
        self.question2.add_vote(new_vote)

        expected_new_score = initial_expected_score + 10
        self.assertEqual(self.user.calculate_score(), expected_new_score)

if __name__ == '__main__':
    unittest.main()
