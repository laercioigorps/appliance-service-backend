from service.models import Status


class SampleDataCreation:
    def __init__(self):
        self.customers = []
        self.statuses = []
        self.organization = None
        self.models = []

    def updateStatuses(self):
        self.statuses = Status.objects.all()
