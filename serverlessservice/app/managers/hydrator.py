from typing import Any
from uuid import UUID
from managers.venue_manager import VenueManager
from models.league_team_model import LeagueTeamModel
from models.venue_model import VenueModel, VenueSearchModel
from util.common import RequestOperators


class Hydrator:
    def __init__(
        self,
        venue_manager: VenueManager = VenueManager(),
    ) -> None:
        self.venue_manager = venue_manager

    def hydrate_venues(
        self,
        result_list: list[VenueModel],
        request_operators: RequestOperators | None = None,
    ):
        self.hydrate_league_teams(result_list, request_operators)
        return

    def hydrate_league_teams(
        self,
        result_list: list[LeagueTeamModel],
        request_operators: RequestOperators | None = None,
    ):
        # Hydrate retailer
        self.hydrate_target(
            "home_venue",
            result_list,
            VenueSearchModel(),
            self.venue_manager.search_venues,
            request_operators.hydration if request_operators is not None else None,
        )

    def hydrate_target(
        self,
        target_name: str,
        parent_models: list[Any],
        search_model: Any,
        search_function: callable,
        hydration: list[str],
    ) -> None:
        if hydration is None:
            return

        sub_hydration_list = self.seek_hydration_and_reduce(target_name, hydration)

        if len(sub_hydration_list) > 0:
            sub_hydration_list_with_root_removed = [
                x for x in sub_hydration_list if x != target_name
            ]

            sub_operators: RequestOperators = RequestOperators(skip_paging=True)

            if len(sub_hydration_list_with_root_removed) > 0:
                sub_operators.hydration = [
                    x for x in sub_hydration_list_with_root_removed
                ]

            target_ids = [
                parent_model.__dict__[f"{target_name}_id"]
                for parent_model in parent_models
                if parent_model.__dict__[f"{target_name}_id"] is not None
            ]

            search_model.ids = target_ids

            existing_children = search_function(search_model, None, sub_operators)

            existing_children_dict: dict[UUID, Any] = {
                child.id: child for child in existing_children.items
            }

            for parent_model in parent_models:
                existing_child = (
                    existing_children_dict[parent_model.__dict__[f"{target_name}_id"]]
                    if parent_model.__dict__[f"{target_name}_id"] is not None
                    else None
                )
                parent_model.__dict__[target_name] = existing_child
