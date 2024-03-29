import factory


from core.utils.tests.base import faker

from appliances.models import (
    Appliance,
    Brand,
    Category,
    Historic,
    Problem,
    Solution,
    Symptom,
)

from profiles.tests.factories import OrganizationFactory


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.LazyAttribute(lambda _: faker.company())


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: faker.color_name())


class ApplianceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appliance

    model = factory.LazyAttribute(lambda _: faker.lexify(text="??????????"))
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)


class SolutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solution

    name = factory.LazyAttribute(lambda _: faker.name())
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=100))


class ProblemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Problem

    name = factory.LazyAttribute(lambda _: faker.name())
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=100))

    @factory.post_generation
    def solutions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of solutions were passed in, use them
            for solution in extracted:
                self.solutions.add(solution)


class SymptomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Symptom

    name = factory.LazyAttribute(lambda _: faker.name())
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=100))

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of solutions were passed in, use them
            for category in extracted:
                self.categories.add(category)

    @factory.post_generation
    def causes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of solutions were passed in, use them
            for cause in extracted:
                self.causes.add(cause)


class HistoricFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Historic

    appliance = factory.SubFactory(ApplianceFactory)
    org = factory.SubFactory(OrganizationFactory)

    @factory.post_generation
    def symptoms(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of solutions were passed in, use them
            for symptom in extracted:
                self.symptoms.add(symptom)

    @factory.post_generation
    def problems(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of solutions were passed in, use them
            for problem in extracted:
                self.problems.add(problem)

    @factory.post_generation
    def solutions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of solutions were passed in, use them
            for solution in extracted:
                self.solutions.add(solution)
