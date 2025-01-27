from domain.patient import PatientVitalSigns
from persistence.models.patients_models import PatientVitalSignsDB
from sqlalchemy.orm import Session


class VitalSignsRepository:
    def __init__(self, db: Session):
        self.db = db

    @classmethod
    def from_domain(cls, vital_signs: PatientVitalSigns) -> PatientVitalSignsDB:
        return PatientVitalSignsDB(
            vitalsign_id=vital_signs.vitalsign_id,
            patient_id=vital_signs.patient_id,
            temperature=vital_signs.temperature,
            systolic_pressure=vital_signs.systolic_pressure,
            diastolic_pressure=vital_signs.diastolic_pressure,
            pulse_rate=vital_signs.pulse_rate,
            respiration_rate=vital_signs.respiration_rate,
            weight=vital_signs.weight,
            height=vital_signs.height,
        )

    @classmethod
    def to_domain(cls, vital_signs: PatientVitalSignsDB) -> PatientVitalSigns:
        return PatientVitalSigns(
            vitalsign_id=vital_signs.vitalsign_id,
            patient_id=vital_signs.patient_id,
            temperature=vital_signs.temperature,
            systolic_pressure=vital_signs.systolic_pressure,
            diastolic_pressure=vital_signs.diastolic_pressure,
            pulse_rate=vital_signs.pulse_rate,
            respiration_rate=vital_signs.respiration_rate,
            weight=vital_signs.weight,
            height=vital_signs.height,
        )

    def register_vital_signs(self, vital_signs: PatientVitalSigns) -> PatientVitalSigns:
        vital_signs_db = VitalSignsRepository.from_domain(vital_signs)

        self.db.add(vital_signs_db)
        self.db.commit()
        self.db.refresh(vital_signs_db)

        vital_signs.vitalsign_id = vital_signs_db.vitalsign_id

        return vital_signs

    def get_vital_signs(self, patient_id: int) -> list[PatientVitalSigns]:
        vital_signs_db = (
            self.db.query(PatientVitalSignsDB)
            .filter(PatientVitalSignsDB.patient_id == patient_id)
            .all()
        )

        vital_signs = list(
            map(lambda x: VitalSignsRepository.to_domain(x), vital_signs_db)
        )

        return vital_signs
