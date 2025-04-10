
from ast import Num
from datetime import datetime
from abc import ABC, abstractmethod

#---------------------------------------------------------------------------------------#

class Votable:
    def __init__(self):
        self.votes = []

    def get_votes(self):
        return self.votes

    def positive_votes(self):
        return [vote for vote in self.votes if vote.is_like()]
	
    def negative_votes(self):
        return [vote for vote in self.votes if not vote.is_like()]

    def add_vote(self, a_vote):
        if any(vote.user == a_vote.user for vote in self.votes):
            raise ValueError("Este usuario ya ha votado")
        self.votes.append(a_vote)

#---------------------------------------------------------------------------------------#

class Answer(Votable):
    def __init__(self, question, user, description):
        super().__init__()
        self.timestamp = datetime.now()
        self.question = question
        self.user = user
        self.description = description
        self.question.add_answer(self)
	
    def get_timestamp(self):
        return self.timestamp
	
    def get_question(self):
        return self.question
		
    def get_user(self):
        return self.user

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

#---------------------------------------------------------------------------------------#

class Question(Votable):
    def __init__(self, user, title, description, topics = []):
        super().__init__()
        self.timestamp = datetime.now()
        self.title = title
        self.description = description
        self.answers = []
        self.user = user
        self.topics = []
        self._initialize_topics(topics)
        user.add_question(self)

    def get_timestamp(self):
        return self.timestamp

    def get_title(self):
        return self.title
    
    def set_title(self, title):
        self.title = title

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_best_answer(self):
        if not self.answers:
            return None    
        return sorted(self.answers, key=lambda a: len(a.positive_votes()) - len(a.negative_votes()), reverse=True)[0]

    def add_answer(self, answer):
        self.answers.append(answer)

    def get_user(self):
        return self.user

    def get_topics(self):
        return self.topics

    def add_topic(self, a_topic):
        if a_topic in self.topics: 
            raise ValueError("El tópico ya está agregado.")
        self.topics.append(a_topic)
        a_topic.add_question(self)

    def _initialize_topics(self, topics):
        for topic in topics:
            self.add_topic(topic)

#---------------------------------------------------------------------------------------#

class Topic:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.questions = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_questions(self):
        return self.questions

    def add_question(self, question):
        self.questions.append(question)

#---------------------------------------------------------------------------------------#

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.questions = []
        self.answers = []
        self.topics_of_interest = []
        self.following = []
        self.votes = []

    def get_username(self):
        return self.username

    def set_username(self, an_object):
        self.username = an_object

    def get_password(self):
        return self.password

    def set_password(self, an_object):
        self.password = an_object

    def get_questions(self):
        return self.questions

    def add_question(self, question):
        self.questions.append(question)

    def get_answers(self):
        return self.answers

    def add_answer(self, an_answer):
        self.answers.append(an_answer)

    def get_topics_of_interest(self):
        return self.topics_of_interest

    def add_topic(self, topic):
        self.topics_of_interest.append(topic)

    def get_following(self):
        return self.following

    def follow(self, user):
        self.following.append(user)

    def stop_follow(self, user):
        self.following.remove(user)

    def get_votes(self):
        return self.votess

    def add_vote(self, vote):
        self.votes.append(vote)

    def calculate_score(self):
        score = 0;
        score += self._sum_votable_score(self.questions, 10)
        score += self._sum_votable_score(self.answers, 20)
        return score

    def _sum_votable_score(self, votable, points):
        score = 0
        for item in votable:
            if len(item.positive_votes()) > len(item.negative_votes()):
                score += points
        return score

    def get_questions_from_topics_of_interest(self):
        questions = []
        for topic in self.topics_of_interest:
            questions.extend(question for question in topic.questions if question.user != self)
        return questions

    def get_questions_from_following(self):
        questions = []
        for follow in self.following:
            questions.extend(follow.questions)
        return questions

#---------------------------------------------------------------------------------------#

class Vote:
    
    def __init__(self, user, is_like=True):
        self.is_positive_vote = is_like
        self.timestamp = datetime.now()
        self.user = user

    def is_like(self):
        return self.is_positive_vote

    def get_user(self):
        return self.user

    def like(self):
        self.is_positive_vote = True

    def dislike(self):
        self.is_positive_vote = False

#---------------------------------------------------------------------------------------#

class QuestionRetriever(ABC):

    def __init__(self, max_questions):
        self.max_questions = max_questions

    def retrieve_sorted_questions(self, questions, user):
        questions = self.retrieve_questions(questions, user)
        questions.sort(key = lambda q: len(q.positive_votes()))
        return questions[:self.max_questions]

    @abstractmethod
    def retrieve_questions(self, questions, user):
        pass

#---------------------------------------------------------------------------------------#

class SocialQuestionRetriever(QuestionRetriever):

    def retrieve_questions(self, questions, user):
        return user.get_questions_from_following()

#---------------------------------------------------------------------------------------#

class TopicsQuestionRetriever(QuestionRetriever):

    def retrieve_questions(self, questions, user):
        return user.get_questions_from_topics_of_interest()

#---------------------------------------------------------------------------------------#

class NewsQuestionRetriever(QuestionRetriever):

    def retrieve_questions(self, questions, user):
        news_col = []
        for question in questions:
            if question.timestamp.date() == datetime.today().date():
                news_col.append(question)
        return news_col

#---------------------------------------------------------------------------------------#

class PopularTodayQuestionRetriever(QuestionRetriever):

    def retrieve_questions(self, questions, user):
        today_questions = [q for q in questions if q.timestamp.date() == datetime.today().date()]
        if today_questions:
            average_votes = sum(len(q.positive_votes()) for q in today_questions) / len(today_questions) #FEATURE ENVY: CAMBIAR
            popular_questions = [q for q in today_questions if len(q.positive_votes()) > average_votes]
            return popular_questions
        return []

#---------------------------------------------------------------------------------------#

class QuestionRetrieverFactory(ABC):

    @abstractmethod
    def create(self):
        pass

class SocialRetrieverFactory(QuestionRetrieverFactory):

    def create(self, max_questions):
        return SocialQuestionRetriever(max_questions)

class TopicsRetrieverFactory(QuestionRetrieverFactory):

    def create(self, max_questions):
        return TopicsQuestionRetriever(max_questions)

class NewsRetrieverFactory(QuestionRetrieverFactory):

    def create(self, max_questions):
        return NewsQuestionRetriever(max_questions)

class PopularTodayRetrieverFactory(QuestionRetrieverFactory):

    def create(self, max_questions):
        return PopularTodayQuestionRetriever(max_questions)

#---------------------------------------------------------------------------------------#

class CuOOra:
    def __init__(self):
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def get_questions_for_user(self, user, retriever_factory: QuestionRetrieverFactory, max_questions):
        return retriever_factory.create(max_questions).retrieve_sorted_questions(self.questions, user)
