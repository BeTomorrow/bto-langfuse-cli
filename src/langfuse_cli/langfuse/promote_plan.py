from dataclasses import dataclass


@dataclass
class PlanItem:
    name: str
    src_version: int | None
    tgt_version: int | None


class Plan:
    items: list[PlanItem]

    def __init__(self):
        self.items = []

    def append(self, name: str, src_version: int | None, tgt_version: int | None):
        self.items.append(PlanItem(name=name, src_version=src_version, tgt_version=tgt_version))

    def has_changes(self) -> bool:
        return len(self.updated_prompts()) > 0 or len(self.removed_prompts()) > 0 or len(self.added_prompts()) > 0

    def added_prompts(self) -> list[PlanItem]:
        return [item for item in self.items if item.src_version is None]

    def removed_prompts(self) -> list[PlanItem]:
        return [item for item in self.items if item.tgt_version is None]

    def updated_prompts(self) -> list[PlanItem]:
        return [item for item in self.items if item.src_version is not None and item.tgt_version is not None and item.src_version != item.tgt_version]

    def unchanged_prompts(self) -> list[PlanItem]:
        return [item for item in self.items if item.src_version is not None and item.tgt_version is not None and item.src_version == item.tgt_version]
