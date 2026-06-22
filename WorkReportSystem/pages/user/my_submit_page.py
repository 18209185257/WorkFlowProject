import gradio as gr


def create_my_submit_page():

    with gr.Column(
        visible=False
    ) as page:

        gr.HTML("""
        <div class="breadcrumb">
            工作台 > 我的提交记录
        </div>
        """)

        with gr.Row():

            start_date = gr.Textbox(
                label="开始时间"
            )

            end_date = gr.Textbox(
                label="结束时间"
            )

            submit_type = gr.Dropdown(
                choices=[
                    "全部",
                    "日报",
                    "会议记录",
                    "项目汇报"
                ],
                value="全部",
                label="类型"
            )

            query_btn = gr.Button(
                "查询"
            )

        submit_html = gr.HTML()

        back_btn = gr.Button(
            "返回工作台"
        )

    return (

        page,

        start_date,

        end_date,

        submit_type,

        query_btn,

        submit_html,

        back_btn

    )