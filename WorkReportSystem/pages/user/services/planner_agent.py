def plan_task(question):
    if not question:
        return ["chat"]

    plans = []

    question = question.lower()

    if "项目" in question:
        plans.append(
            "project"
        )
    if "风险" in question:
        plans.append(
            "risk"
        )
    if "会议" in question:
        plans.append(
            "meeting"
        )

    if "日报" in question:
        plans.append(
            "daily"
        )
    if (
            "周报" in question
            or
            "总结" in question
    ):
        plans.extend(
            [
                "daily",
                "meeting",
                "project",
                "risk"
            ]
        )
    plans = list(
        dict.fromkeys(plans)
    )
    if not plans:
        plans.append(
            "chat"
        )