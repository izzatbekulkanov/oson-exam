from django.db import models
from django.utils.translation import gettext_lazy as _
from university.models import Subject

# Create your models here.

class ExamType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Exam Type"))

    def __str__(self):
        return self.name


# Exam model
class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


# Question model
class Question(models.Model):
    text = models.TextField(verbose_name=_("Question Text"))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Subject"))
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, verbose_name=_("Exam Type"))

    def __str__(self):
        return self.text[:50]  # Show first 50 characters of the question text


# Answer model
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name=_("Question"))
    text = models.CharField(max_length=255, verbose_name=_("Answer Text"))
    is_correct = models.BooleanField(default=False, verbose_name=_("Is Correct"))

    def __str__(self):
        return self.text


# ExamQuestion model to link exams and questions (Many-to-many relationship)
class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exam.title} - {self.question.text[:50]}"  # Display exam title and first 50 characters of the question text
