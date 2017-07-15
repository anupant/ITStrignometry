from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.urlresolvers import reverse


class Course(models.Model):
    #user = models.ForeignKey(User, default=1)
    course_name = models.CharField(max_length=250)
    course_logo = models.FileField()
    course_description = models.CharField(max_length=250)

    def get_absolute_url(self):
        return reverse('learning:detail',kwargs = {'pk': self.pk})

    def __str__(self):
        return self.course_name


class Course_Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_content_description = models.CharField(max_length=250)
    course_content1 = models.FileField()

    def __str__(self):
        return self.course_content_description



class Quiz(models.Model):
    course_content = models.ForeignKey(Course_Content, on_delete=models.CASCADE)
    quiz_description = models.CharField(max_length=250)
    numOfQuestions = models.CharField(max_length=250)
    noOfQuestionsCorrect = models.CharField(max_length=250)
    noOfQuestionsAttempted = models.CharField(max_length=250)
    question_wrong1 = models.CharField(max_length=250)
    #This will keep the number of alternate quiz size if present
    questions_alternate_size = models.IntegerField()
    #no of questions for which alternate string are taken
    questions_alternate_string = models.CharField(max_length=250)

    def __str__(self):
        return self.quiz_description

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=250)
    question_description = models.FileField()
    question_option1 = models.CharField(max_length=250)
    question_option2 = models.CharField(max_length=250)
    question_option3 = models.CharField(max_length=250)
    question_option4 = models.CharField(max_length=250)
    question_hint1 = models.CharField(max_length=250)
    #question_no = models.IntegerField()
    #question_right_answer = models.CharField(max_length=250)
    question_explanation = models.CharField(max_length=250)
    question_difficulty = models.CharField(max_length=250)
    hint_taken = models.BooleanField(default = False)

    def __str__(self):
        return self.question_title


class Quiz_Performance(models.Model):
    #quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1)
    quiz_no = models.CharField(max_length=250,primary_key=True)
    noOfQuestionsCorrect = models.CharField(max_length=250)
    noOfQuestionsAttempted = models.CharField(max_length=250)
    numOfQuestions = models.CharField(max_length=250)
    def __str__(self):
        return self.quiz_no

#Alternate Question List
class Question1(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=250)
    question_description = models.FileField()
    question_option1 = models.CharField(max_length=250)
    question_option2 = models.CharField(max_length=250)
    question_option3 = models.CharField(max_length=250)
    question_option4 = models.CharField(max_length=250)
    question_hint1 = models.CharField(max_length=250)
    question_no = models.IntegerField()
    question_right_answer = models.CharField(max_length=250)
    #question_right_answer_actual = models.CharField(max_length=250)
    question_explanation = models.CharField(max_length=250)
    question_difficulty = models.CharField(max_length=250)
    hint_taken = models.BooleanField(default = False)
    alternate_question_title = models.CharField(max_length=250)
    alternate_question_description = models.FileField()
    alternate_question_option1 = models.CharField(max_length=250)
    alternate_question_option2 = models.CharField(max_length=250)
    alternate_question_option3 = models.CharField(max_length=250)
    alternate_question_option4 = models.CharField(max_length=250)
    alternate_question_hint1 = models.CharField(max_length=250)
    alternate_question_right_answer = models.CharField(max_length=250)



    def __str__(self):
        return self.question_title



class CoursePerformance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz_attempted = models.CharField(max_length=250,primary_key=True)
    #1_1_1_2_3 means course 1 , quiz 1 and question 1,2,3
    quiz_question_wrong = models.CharField(max_length=250)
    quiz_question_hintTaken = models.CharField(max_length=250)
    def __str__(self):
        return self.quiz_attempted



class CoursePerformanceHistory(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1)
    quiz_attempted = models.CharField(max_length=250,primary_key=True)
    #1_1_1_2_3 means course 1 , quiz 1 and question 1,2,3
    quiz_question_wrong = models.CharField(max_length=250)
    quiz_question_hintTaken = models.CharField(max_length=250)
    quiz_question_wrongNo = models.CharField(max_length=250)
    quiz_hintNo = models.CharField(max_length=250)
    def __str__(self):
        return self.quiz_attempted


class QuizPerformanceHistory(models.Model):
    user = models.ForeignKey(User, default=1)
    quiz_no = models.CharField(max_length=250,primary_key=True)

    numOfQuestions = models.CharField(max_length=250)
    noOfQuestionsCorrect = models.CharField(max_length=250)
    noOfQuestionsAttempted = models.CharField(max_length=250)
    numOfQuestionsWrong = models.CharField(max_length=250)

    quiz_question_hintTaken = models.CharField(max_length=250)
    quiz_question_wrongNo = models.CharField(max_length=250)


    def __str__(self):
        return self.quiz_no


