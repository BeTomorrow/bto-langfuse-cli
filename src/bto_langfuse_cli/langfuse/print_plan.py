from bto_langfuse_cli.langfuse.promote_plan import Plan


def print_plan(plan: Plan):

    print(f"{'-' * 30}")
    print("Plan :")
    if not plan.has_changes():
        print("No change detected !")
        return

    added_prompts = plan.added_prompts()
    if len(added_prompts) > 0:
        print(f"\033[92m Added :\033[0m")
        for p in added_prompts:
            print(f"\033[92m\t + {p.name} : {p.src_version} -> {p.tgt_version}\033[0m")
        print()

    updated_prompts = plan.updated_prompts()
    if len(updated_prompts) > 0:
        print(f"\033[38;5;208m Updated :\033[0m")
        for p in updated_prompts:
            print(f"\033[38;5;208m\t ~ {p.name} : {p.src_version} -> {p.tgt_version} \033[0m")
        print()

    removed_prompts = plan.removed_prompts()
    if len(removed_prompts) > 0:
        print(f"\033[91m Removed :\033[0m")
        for p in removed_prompts:
            print(f"\033[91m\t - {p.name} : {p.src_version} -> {p.tgt_version}\033[0m")
        print()

    print(f"{'-' * 30}")
    print("Summary :")
    print(f"\033[92m  + Added :     {len(plan.added_prompts())}\033[0m")
    print(f"\033[38;5;208m  ~ Updated :   {len(plan.updated_prompts())}\033[0m")
    print(f"\033[91m  - Removed :   {len(plan.removed_prompts())}\033[0m")
    print(f"\033[90m  ° Unchanged : {len(plan.unchanged_prompts())}\033[0m")
    print(f"{'-' * 30}\n")