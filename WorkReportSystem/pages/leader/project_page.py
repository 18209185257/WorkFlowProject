import gradio as gr

from common.project_db import (
    get_all_project
)


def build_project_table():

    rows = []

    for p in get_all_project():

        rows.append([

            p["project_name"],

            p["main_leader"],

            p["progress"],

            p["status"]

        ])

    return rows


def create_leader_project_page():

    with gr.Column(
        visible=False,
        elem_id="page-project"
    ) as page:

        gr.HTML(
            "<h2>📁 项目管理中心</h2>"
        )

        project_df = gr.Dataframe(
            value=build_project_table(),
            headers=[
                "项目",
                "负责人",
                "进度",
                "状态"
            ]
        )

    return page