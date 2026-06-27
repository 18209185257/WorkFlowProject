def plan_leader_task(
        question
):

    q = question.lower()

    plans = []

    if "周报" in q:

        plans.append(
            "weekly_report"
        )

    if (
        "项目分析" in q
        or
        "项目情况" in q
    ):

        plans.append(
            "project_analysis"
        )

    return plans