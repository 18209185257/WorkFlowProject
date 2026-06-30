from .leader_dashboard_service import (
    build_project_trend_chart,
    build_project_status_chart,
    build_daily_report_chart,
    build_risk_rank_html
)

from .project_heatmap_service import (
    build_project_heatmap_html
)

from .project_warning_service import (
    build_project_warning_html
)

from .auto_ai_insight_service import (
    build_auto_ai_insight
)

from .customer_profile_service import (
    build_customer_amount_chart,
    build_customer_project_chart,
    build_customer_industry_chart,
    build_customer_active_chart
)

def refresh_dashboard():
    return (
        build_project_trend_chart(),
        build_project_status_chart(),
        build_project_heatmap_html(),
        build_daily_report_chart(),
        build_risk_rank_html(),
        build_project_warning_html(),
        build_auto_ai_insight(),
        build_customer_amount_chart(),
        build_customer_project_chart(),
        build_customer_industry_chart(),
        build_customer_active_chart()
    )