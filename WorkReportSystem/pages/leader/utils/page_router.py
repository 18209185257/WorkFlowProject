import gradio as gr

def switch_page(target):

    pages = [
        "home",
        "ai",
        "project",
        "risk",
        "employee_profile",
        "customer_profile",
        "analytics",
        "report",
        "weekly_report",
        "diagnosis",
        "decision",
        "project_manager"
    ]

    result = []

    for p in pages:

        result.append(
            gr.update(
                visible=(p == target)
            )
        )

    return result