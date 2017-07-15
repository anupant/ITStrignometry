from django.contrib import admin
from .models import Course,Course_Content,Quiz,Question,Quiz_Performance,Question1,CoursePerformance,\
    CoursePerformanceHistory,QuizPerformanceHistory

admin.site.register(Course)
#admin.site.register(QuestionList)
admin.site.register(Course_Content)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Question1)
admin.site.register(Quiz_Performance)
admin.site.register(CoursePerformance)
admin.site.register(CoursePerformanceHistory)
admin.site.register(QuizPerformanceHistory)


# Register your models here.
