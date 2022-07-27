from service.models import Status


class SampleDataCreation:
    def __init__(self):
        self.customers = []
        self.statuses = []

    def updateStatuses(self):
        self.statuses = Status.objects.all()
