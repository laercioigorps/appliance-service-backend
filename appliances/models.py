from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Appliance(models.Model):
    model = models.CharField(max_length=20)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.model


class Solution(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.name


class Problem(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=150)
    solutions = models.ManyToManyField(Solution)

    def __str__(self) -> str:
        return self.name

class Symptom(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=150)
    categories = models.ManyToManyField(Category)
    causes = models.ManyToManyField(Problem)

    def __str__(self) -> str:
        return self.name
