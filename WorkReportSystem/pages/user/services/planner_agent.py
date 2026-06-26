def plan_task(question):

    if not question:
        return ["chat"]

    q = question.lower()

    plans = []

    # 日报
    if "日报" in q:
        plans.append("daily")

    # 会议
    if "会议" in q:
        plans.append("meeting")

    # 项目
    if "项目" in q:
        plans.append("project")

    # 风险
    if "风险" in q:
        plans.append("risk")

    # 工作总结
    summary_words = [
        "总结",
        "工作总结",
        "最近工作",
        "近期工作",
        "工作情况",
        "工作概览",
        "工作汇报",
        "本周工作",
        "本月工作"
    ]

    if any(
        word in q
        for word in summary_words
    ):
        # plans.extend(
        #     [
        #         "daily",
        #         "meeting",
        #         "project",
        #         "risk"
        #     ]
        # )
        plans.append(
            "employee_summary"
        )

    plans = list(
        dict.fromkeys(plans)
    )

    if not plans:
        plans.append("chat")

    return plans