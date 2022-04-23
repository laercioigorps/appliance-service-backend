from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"

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
    solutions = models.ManyToManyField(Solution, blank=True)

    def __str__(self) -> str:
        return self.name


class Symptom(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=150)
    categories = models.ManyToManyField(Category, blank=True)
    causes = models.ManyToManyField(Problem, blank=True)

    def __str__(self) -> str:
        return self.name


class Historic(models.Model):
    completed = models.BooleanField(default=False)
    symptoms = models.ManyToManyField(Symptom, blank=True)
    problems = models.ManyToManyField(Problem, blank=True)
    solutions = models.ManyToManyField(Solution, blank=True)
    appliance = models.ForeignKey(
        Appliance, on_delete=models.CASCADE, blank=True, null=True
    )
