import logging

from bto_langfuse_cli.langfuse.promote_plan import Plan
from langfuse import get_client, Langfuse

logger = logging.getLogger(__name__)


class LangfuseService:
    _langfuse: Langfuse

    def __init__(self):
        self._langfuse = get_client()
        if self._langfuse.auth_check():
            logger.debug("Langfuse client is authenticated and ready!")
        else:
            logger.error("Authentication failed. Please check your credentials and host.")
            raise Exception("Authentication failed. Please check your credentials and host.")

    def get_all_prompts_names(self, label: str | None = None, tag: str | None = None) -> set[str]:
        prompt_ids = set()
        current_page = 1
        limit = 50

        first_response = self._langfuse.api.prompts.list(label=label, tag=tag, limit=limit, page=current_page)
        remaining_pages = first_response.meta.total_pages - current_page
        current_page = first_response.meta.page + 1
        prompt_ids.update({p.name for p in first_response.data})

        while remaining_pages > 0:
            next_response = self._langfuse.api.prompts.list(label=label, tag=tag, limit=limit, page=current_page)
            remaining_pages = next_response.meta.total_pages - current_page
            current_page = next_response.meta.page + 1
            prompt_ids.update({p.name for p in next_response.data})

        return prompt_ids

    def _get_prompts(self, label: str) -> dict[str, int]:
        prompts_names = self.get_all_prompts_names(label=label)
        prompt_data = [self._langfuse.get_prompt(p, label=label) for p in prompts_names]
        return {p.name: p.version for p in prompt_data}

    def plan(self, src_label, tgt_label) -> Plan:
        src_prompts = self._get_prompts(src_label)
        tgt_prompts = self._get_prompts(tgt_label)

        plan = Plan()

        added_prompts = src_prompts.keys() - tgt_prompts.keys()
        for name in added_prompts:
            plan.append(name=name, src_version=None, tgt_version=src_prompts[name])

        removed_prompts = tgt_prompts.keys() - src_prompts.keys()
        for name in removed_prompts:
            plan.append(name=name, src_version=tgt_prompts[name], tgt_version=None)

        updated_prompts = src_prompts.keys() - added_prompts - removed_prompts
        for name in updated_prompts:
            plan.append(name=name, src_version=tgt_prompts[name], tgt_version=src_prompts[name])

        return plan

    def apply(self, plan: Plan, tgt_label: str):
        for p in plan.added_prompts() + plan.updated_prompts():
            if p.tgt_version is None:
                continue
            labels = self._langfuse.get_prompt(name=p.name, version=p.tgt_version).labels
            if "latest" in labels:
                labels.remove("latest")
            labels.append(tgt_label)
            logger.info(f"Updating prompt {p.name} version {p.tgt_version} set labels {labels}")
            self._langfuse.update_prompt(name=p.name, version=p.tgt_version, new_labels=labels)

        for p in plan.removed_prompts():
            if p.src_version is None:
                continue
            labels = self._langfuse.get_prompt(name=p.name, version=p.src_version).labels
            if "latest" in labels:
                labels.remove("latest")
            if tgt_label in labels:
                labels.remove(tgt_label)
            logger.info(f"Updating prompt {p.name} version {p.src_version} set labels {labels}")
            self._langfuse.update_prompt(name=p.name, version=p.src_version, new_labels=labels)

        self._langfuse.flush()