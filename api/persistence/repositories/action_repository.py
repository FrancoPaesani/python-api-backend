from sqlalchemy.orm import Session

from domain.action import Action
from persistence.models.patients_models import ActionsDB


class ActionRepository:
    def __init__(self, db: Session):
        self.db = db

    @classmethod
    def from_domain(cls, action: Action) -> ActionsDB:
        return ActionsDB(id=action.id, description=action.description)

    @classmethod
    def to_domain(cls, action: ActionsDB) -> Action:
        return Action(id=action.id, description=action.description)

    def create_action(self, action: Action) -> Action:
        action_db = ActionRepository.from_domain(action)

        self.db.add(action_db)
        self.db.commit()
        self.db.refresh(action_db)

        return ActionRepository.to_domain(action_db)

    def get_actions(self) -> list[Action]:
        actions_db = self.db.query(ActionsDB).all()
        actions = list(map(lambda x: ActionRepository.to_domain(x), actions_db))

        return actions
