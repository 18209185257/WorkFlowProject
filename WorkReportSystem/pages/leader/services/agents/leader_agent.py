from .intent_router import detect_intent

from .project_agent import run_project_agent

from .risk_agent import run_risk_agent

from .employee_agent import run_employee_agent

from .customer_agent import run_customer_agent

from .business_agent import run_business_agent

from .weekly_report_agent import (
    run_weekly_report_agent
)

from .ollama_client import call_ollama

from pages.leader.services.knowledge.knowledge_service import (
    search_knowledge
)


def leader_agent(
        username,
        question
):

    intent = detect_intent(question)

    if intent == "project":

        return run_project_agent(question)

    elif intent == "risk":

        return run_risk_agent(question)

    elif intent == "employee":

        return run_employee_agent(question)

    elif intent == "customer":

        return run_customer_agent(question)

    elif intent == "business":

        return run_business_agent(question)

    elif intent == "weekly_report":

        return run_weekly_report_agent(question)

    knowledge = search_knowledge(
        question
    )

    prompt = f"""
    企业知识：

    {knowledge}

    问题：

    {question}
    """

    return call_ollama(
        prompt
    )