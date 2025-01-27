from domain.action import Action
from schemas.action_schema import ActionRequest, ActionResponse
from persistence.repositories.action_repository import ActionRepository


class ActionService:
    def __init__(self, action_repository: ActionRepository):
        self.action_repository = action_repository

    def create_action(self, action: ActionRequest) -> ActionResponse:
        new_action = Action(action.description)

        new_action = self.action_repository.create_action(new_action)

        return new_action

    def get_actions(self) -> list[ActionResponse]:
        return self.action_repository.get_actions()
