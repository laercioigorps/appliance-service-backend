from service.models import Status


class SampleDataCreation:
    def __init__(self):
        self.customers = []
        self.statuses = []
        self.organization = None
        self.appliances = []

    def updateStatuses(self):
        self.statuses = Status.objects.all()


class InitialSampleDataCreation:
    def __init__(self):
        self.brands = []
        self.categories = []
        self.appliances = []
