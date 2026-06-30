def detect_intent(question):

    q = question.lower()

    if "周报" in q:
        return "weekly_report"

    if "风险" in q:
        return "risk"

    if "员工" in q:
        return "employee"

    if "客户" in q:
        return "customer"

    if (
        "经营" in q
        or "收入" in q
        or "利润" in q
    ):
        return "business"

    if (
        "项目" in q
        or "进度" in q
    ):
        return "project"

    return "chat"