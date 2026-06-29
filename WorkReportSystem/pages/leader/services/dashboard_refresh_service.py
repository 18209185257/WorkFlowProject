from pages.leader.services.leader_dashboard_service import (
    build_project_trend_chart,
    build_project_status_chart,
    build_daily_report_chart,
    build_risk_rank_html
)

from pages.leader.services.project_heatmap_service import (
    build_project_heatmap_html
)

def refresh_dashboard():

    return (
        build_project_trend_chart(),

        build_project_status_chart(),

        build_project_heatmap_html(),

        build_daily_report_chart(),

        build_risk_rank_html()

    )