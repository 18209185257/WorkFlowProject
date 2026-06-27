from .leader_weekly_report_service import (
    generate_leader_weekly_report
)

from .leader_project_analysis_service import (
    generate_project_analysis
)

TOOLS = {

    "weekly_report":{

        "name":"领导周报",

        "func":generate_leader_weekly_report

    },

    "project_analysis":{

        "name":"项目分析",

        "func":generate_project_analysis

    }

}