from datetime import datetime


class PatientRegistry:
    def __init__(
        self,
        patient_id: int,
        action_id: int,
        comment: str,
        timestamp: datetime | None = None,
        user_id: int | None = None,
        id: int | None = None,
    ):
        self.id = id
        self.patient_id = patient_id
        self.action_id = action_id
        self.comment = comment
        self.timestamp = timestamp
        self.user_id = user_id
