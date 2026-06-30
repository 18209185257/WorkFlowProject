from pages.leader.services.ai_weekly_report_service import (
    build_ai_weekly_report
)

from pages.leader.services.knowledge.knowledge_service import (
    search_knowledge
)


def run_weekly_report_agent(question):

    return build_ai_weekly_report()