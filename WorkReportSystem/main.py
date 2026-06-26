import gradio as gr
from fastapi import FastAPI
from auth.auth_service import login_check,change_password

from pages.login.login_page import create_login_page
from pages.user.dashboard_page import create_dashboard_page
from pages.user.project_page import create_project_page
from pages.user.meeting_page import create_meeting_page
from pages.user.daily_page import create_daily_page
from pages.user.password_page import create_password_page

from pages.leader.leader_page import (
    create_leader_page,
    build_overview_html
)

from pages.leader.workflow_ai_page import create_workflow_ai_page

from pages.leader.user_manager_page import create_user_manager_page

from auth.auth_service import register_user,init_db

from pages.leader.services.user_service import (
    build_user_html,
    update_user,
    delete_user_by_name
)

from pages.leader.business_dashboard_page import (
    create_business_dashboard_page
)

from pages.customer.customer_page import (
    create_customer_page
)

from pages.customer.services.customer_service import (
    build_customer_html,
    build_customer_kpi_html,
    add_customer,
    update_customer,
    delete_customer
)

from pages.leader.services.cockpit_service import (
    build_cockpit_html
)

from pages.leader.services.ai_business_service import (
    build_business_analysis_html,
    wrap_analysis
)

from pages.leader.services.risk_service import (
    build_warning_html
)

from pages.leader.cockpit_page import create_cockpit_page

from pages.project_center.project_center_page import (
    create_project_center_page
)

from pages.project_center.services.project_center_service import (
    build_project_html,
    update_project_api,
    delete_project_api,
    add_project_api,
    build_project_kpi_html,
    build_project_rank_html

)

from pages.leader.project_detail_page import (
    create_project_detail_page
)

from pages.leader.services.project_detail_service import (
    build_project_detail_html,
    add_member_and_refresh,
    delete_project_member,
    add_risk_and_refresh,
    delete_risk_and_refresh,
    build_project_ai_analysis
)

from pages.leader.services.project_progress_service import (
    add_project_progress,
    delete_project_progress,
    get_progress_by_id
)

from pages.project_center.project_manager_page import create_project_manager_page
from pages.user.project_progress_page import (
    create_project_progress_page
)

from pages.user.my_project_page import create_my_project_page
from pages.user.services.my_project_service import (
    add_my_project_progress,
    build_my_project_progress_html,
    delete_progress_and_refresh,
    load_my_progress,
    update_progress_and_refresh,
    build_my_project_kpi_html,
    build_my_project_ai_analysis,
    build_my_project_summary_html,
    build_my_project_html,
    query_my_project
)

from pages.leader.services.project_ai_service import (
    generate_project_ai_report
)

from pages.leader.services.workflow_ai_service import (
    build_kpi_html,
    build_ai_side_panel
)

from pages.leader.ai.chat_service import (
    user_send_msg,
    ai_reply
)

from pages.user.my_submit_page import (
    create_my_submit_page
)

from pages.user.services.my_submit_service import (
    build_my_submit_html
)

from pages.user.my_profile_page import (
    create_my_profile_page
)

from pages.user.services.my_profile_service import (
    build_my_profile_html
)

from pages.user.services.dashboard_service import (
    build_dashboard_v14,
    update_user_password,
    get_project_health_rank,
    get_risk_projects,
    generate_dashboard_ai,
    generate_weekly_report,
    generate_daily_report,
    generate_meeting_summary,
    get_project_detail,
    get_submit_detail
)

from pages.user.services.ai_service import *

import json
import os
from common.static_loader import load_js_files
from pages.user.services.rag_service import (
    rebuild_vector_db
)

from pages.user.services.agent_service import ai_agent

from pages.user.services.password_service import (
    change_password
)

# 初始化数据库
init_db()

app = FastAPI()
#项目排行
@app.get("/api/dashboard/rank")
def api_rank():

    return get_project_health_rank()

#风险
@app.get("/api/dashboard/risk")
def api_risk(user:str):

    rows = get_risk_projects(user)

    return [

        {
            "project":r[0],
            "progress":r[1],
            "risk":r[2]
        }

        for r in rows
    ]

#AI分析
@app.get("/api/dashboard/ai")
def api_ai(user:str):

    return {

        "content":
        generate_dashboard_ai(user)

    }

#自动周报
@app.get("/api/dashboard/weekly")
def api_weekly(user:str):

    return {

        "content":
        generate_weekly_report(user)

    }

@app.get("/api/ai/daily")
def ai_daily(task:str):

    return {

        "content":
        generate_daily_report(task)

    }

@app.get("/api/ai/meeting")
def ai_meeting(content:str):

    return {

        "content":
        generate_meeting_summary(content)

    }

@app.get("/api/project/detail")
def api_project_detail(id: int):

    return get_project_detail(id)


@app.get("/api/submit/detail")
def api_submit_detail(id: int):

    return get_submit_detail(id)

user_table_state = gr.State([])
current_project_id = gr.State()
editing_progress_id = gr.State()

js_code = load_js_files()

css_files = [
    "style.css",
    "leader.css",
    "workflow_ai.css",
    "dashboard.css",
    "dashboard-v14.css",
    "ai.css"
]

custom_css = ""

for file in css_files:
    path = os.path.join(
        "static",
        "css",
        file
    )

    if os.path.exists(path):
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            custom_css += "\n" + f.read()

with gr.Blocks(
    title="华智瑞森特工作汇报系统",
    css=custom_css,
    fill_width=True,
    head=f"""
      <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
      <script>
      {js_code}
      
      window.addEventListener("DOMContentLoaded", function(){{
        console.log("DOM Ready");
      }});
      </script>
    """
) as demo:

    # 当前登录用户
    user_state = gr.State("")
    role_state = gr.State("")
    real_name_state = gr.State("")

    # ==========================
    # 顶部导航栏
    # ==========================
    with gr.Row(elem_classes=["top-header"]):
        gr.HTML(
            "<div class='system-title'>Hazhi Raysent</div>"
        )

        gr.HTML(
            "<div class='header-right'></div>"
        )

        gr.HTML("""
        <script>

        window.addEventListener(

            const box =
            document.querySelector(
            '#edit_event textarea'
            );

            if(box){

                box.value =
                e.detail;

                box.dispatchEvent(
                    new Event(
                    'input',
                    {bubbles:true}
                    )
                );
            }
        }
        );

        window.addEventListener(
        'delete-user',
        function(e){

            const box =
            document.querySelector(
            '#delete_event textarea'
            );

            if(box){

                box.value =
                e.detail;

                box.dispatchEvent(
                    new Event(
                    'input',
                    {bubbles:true}
                    )
                );
            }
        }
        );

        </script>
        """)

        current_user = gr.HTML(
            elem_classes=["user-name"]
        )

        logout_btn = gr.Button(
            "退出",
            visible=False,
            elem_classes=["logout-btn"]
        )

    # ==========================
    # 工作台
    # ==========================
    (
        dashboard_page,
        dashboard_html
    ) = create_dashboard_page()

    # (
    #     profile_page,
    #
    #     profile_username,
    #
    #     profile_real_name,
    #
    #     profile_role,
    #
    #     new_pwd,
    #
    #     save_pwd_btn,
    #
    #     pwd_result,
    #
    #     back_my_profile
    # ) = create_my_profile_page()
    #
    # save_pwd_btn.click(
    #     update_user_password,
    #     inputs=[
    #         user_state,
    #         new_pwd
    #     ],
    #     outputs=pwd_result
    # )

    # ==========================
    # 项目页
    # ==========================
    (
        project_page,
        back_project
    ) = create_project_page()

    # ==========================
    # 会议页
    # ==========================
    (
        meeting_page,
        back_meeting
    ) = create_meeting_page()

    # ==========================
    # 日报页
    # ==========================
    (
        daily_page,
        reporter,
        back_daily
    ) = create_daily_page()

    daily_page_btn = gr.Button(
        value="dashboard_daily_hidden",
        elem_id="daily_page_btn",
        elem_classes=["hidden-trigger"]
    )

    meeting_page_btn = gr.Button(
        value="dashboard_meeting_hidden",
        elem_id="meeting_page_btn",
        elem_classes=["hidden-trigger"]
    )

    project_page_btn = gr.Button(
        value="dashboard_project_hidden",
        elem_id="project_page_btn",
        elem_classes=["hidden-trigger"]
    )

    daily_page_btn.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            dashboard_page,
            daily_page
        ]
    )

    meeting_page_btn.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            dashboard_page,
            meeting_page
        ]
    )

    project_page_btn.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            dashboard_page,
            project_page
        ]
    )

    # ==========================
    # 修改密码页
    # ==========================
    # (
    #     password_page,
    #     back_password,
    #     old_pwd,
    #     new_pwd,
    #     confirm_pwd,
    #     submit_btn,
    #     pwd_result
    # ) = create_password_page()

    (
        leader_page,
        overview_html,
        stat_range,
        btn_ai_query,
        btn_user_manager,
        btn_cockpit,
        btn_customer,
        btn_project_center
    ) = create_leader_page()

    (
        workflow_ai_page,
        kpi_project,
        kpi_daily,
        kpi_risk,
        btn_week,
        btn_risk,
        workflow_ai_btn_daily,
        btn_rank,
        ai_chatbot,
        ai_msg,
        ai_summary,
        ai_risk,
        project_rank,
        back_ai,
    ) = create_workflow_ai_page()

    ai_msg.submit(
        user_send_msg,
        [ai_msg, ai_chatbot],
        [ai_msg, ai_chatbot]
    ).then(
        ai_reply,
        [ai_chatbot],
        ai_chatbot
    )

    btn_week.click(
        lambda: "admin本周工作总结",
        outputs=ai_msg
    ).then(
        user_send_msg,
        [ai_msg, ai_chatbot],
        [ai_msg, ai_chatbot]
    ).then(
        ai_reply,
        [ai_msg, ai_chatbot],
        [ai_chatbot]
    )

    btn_risk.click(
        lambda: "项目风险分析",
        outputs=ai_msg
    ).then(
        user_send_msg,
        [ai_msg, ai_chatbot],
        [ai_msg, ai_chatbot]
    ).then(
        ai_reply,
        [ai_msg, ai_chatbot],
        [ai_chatbot]
    )

    btn_rank.click(
        lambda: "项目进度排行榜",
        outputs=ai_msg
    ).then(
        user_send_msg,
        [ai_msg, ai_chatbot],
        [ai_msg, ai_chatbot]
    ).then(
        ai_reply,
        [ai_msg, ai_chatbot],
        [ai_chatbot]
    )

    (
        user_manager_page,
        user_html,
        modal_html,
        back_user_manager
    ) = create_user_manager_page()

    (
        project_center_page,
        project_kpi,
        project_center_html,
        add_btn,
        refresh_btn,
        project_center_rank_html,
        project_center_modal_html,
        back_project_center,
        project_center_save_project_event,
        project_center_delete_project_event
    ) = create_project_center_page()


    def project_center_save_project(data):
        data = json.loads(data)
        if str(data.get("id", "")).strip():
            update_project_api(data)
        else:
            add_project_api(data)
        return (
            build_project_kpi_html(),
            build_project_html(),
            build_project_rank_html()
        )


    project_center_save_project_event.change(
        fn=project_center_save_project,
        inputs=project_center_save_project_event,
        outputs=[
            project_kpi,
            project_center_html,
            project_center_rank_html
        ]
    )


    def project_center_remove_project(project_id):
        delete_project_api(project_id)
        return (
            build_project_kpi_html(),
            build_project_html(),
            build_project_rank_html()
        )


    project_center_delete_project_event.change(
        fn=project_center_remove_project,
        inputs=project_center_delete_project_event,
        outputs=[
            project_kpi,
            project_center_html,
            project_center_rank_html
        ]
    )

    (
        business_dashboard_page,
        back_business_dashboard
    ) = create_business_dashboard_page()

    (
        customer_page,
        customer_kpi,
        customer_html,
        customer_page_modal_html,
        customer_add_btn,
        customer_refresh_btn,
        back_customer,
        save_customer_event,
        delete_customer_event

    ) = create_customer_page()

    def customer_save(data):
        data = json.loads(data)
        if str(data.get("id", "")).strip():
            update_customer(data)
        else:
            add_customer(
                data["customer_name"],
                data["contact_name"],
                data["phone"],
                data["email"],
                data["address"]
            )
        return (
            build_customer_kpi_html(),

            build_customer_html()

        )


    def customer_remove(customer_id):
        delete_customer(customer_id)
        return (
            build_customer_kpi_html(),
            build_customer_html()
        )


    delete_customer_event.change(
        fn=customer_remove,
        inputs=delete_customer_event,
        outputs=[
            customer_kpi,
            customer_html
        ]
    )


    save_customer_event.change(
        fn=customer_save,
        inputs=save_customer_event,
        outputs=[
            customer_kpi,
            customer_html
        ]
    )

    save_user_event = gr.Textbox(
        elem_id="save_user_event",
        visible=False,
        container=False
    )

    delete_user_event = gr.Textbox(
        elem_id="delete_user_event",
        visible=False,
        container=False
    )

    delete_project_event = gr.Textbox(
        visible=False,
        elem_id="delete_project_event"
    )

    (
        login_page,

        username,
        password,
        login_btn,
        login_msg,

        login_panel,
        register_panel,

        register_btn,

        reg_name,
        reg_phone,
        reg_user,
        reg_pwd,

        back_login_btn,
        reg_submit,
        reg_msg

    ) = create_login_page()

    # 驾驶舱
    (
        cockpit_page,

        cockpit_html,
        rank_html,
        cockpit_ai_analysis_html,
        warning_html,
        generate_ai_btn,
        back_cockpit
    ) = create_cockpit_page()

    (
        project_detail_page,
        project_detail_html,
        project_detail_modal_html,
        progress_content,
        risk_content,
        next_plan,
        add_progress_btn,
        member_name,
        member_role,
        add_member_btn,
        ai_project_btn,
        ai_project_html,
        back_project_detail,
        delete_member_id,
        delete_member_btn,
        risk_level,
        risk_desc,
        risk_solution,
        add_risk_btn,

        delete_risk_id,
        delete_risk_btn,
        edit_risk_id,
        delete_progress_id,
        delete_progress_btn,
        edit_progress_id,
        load_progress_btn,
        edit_progress_content,
        edit_risk_content,
        edit_next_plan,
        project_detail_ai_result

    ) = create_project_detail_page()

    (
        project_manager_page,
        project_manager_html,
        project_modal_html,
        new_project_btn,
        refresh_project_btn,
        back_project_manager,
        save_project_event,
        delete_project_manager_event
    ) = create_project_manager_page()


    def save_project(data):
        data = json.loads(data)
        if str(data.get("id", "")).strip():
            update_project_api(data)
        else:
            add_project_api(data)
        return build_project_html()


    save_project_event.change(
        fn=save_project,
        inputs=save_project_event,
        outputs=project_manager_html
    )

    def remove_project(project_id):
        delete_project_api(project_id)
        return build_project_html()

    delete_project_manager_event.change(
        fn=remove_project,
        inputs=delete_project_manager_event,
        outputs=project_center_html
    )

    (
        project_progress_page,
        progress_history_html,
        user_progress_content,
        user_risk_content,
        user_next_plan,
        save_progress_btn,
        progress_result,
        project_ai_btn,
        ai_result,
        back_project_progress
    ) = create_project_progress_page()

    project_ai_btn.click(
        fn=generate_project_ai_report,
        inputs=current_project_id,
        outputs=ai_result
    )

    (
        my_submit_page,
        submit_start_date,
        submit_end_date,
        submit_type,
        submit_query_btn,
        my_submit_html,
        back_my_submit
    ) = create_my_submit_page()

    #查看我的提交记录
    def open_my_submit(real_name):
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            build_my_submit_html(
                real_name
            )
        )

    submit_query_btn.click(
        fn=build_my_submit_html,
        inputs=[
            real_name_state,
            submit_start_date,
            submit_end_date,
            submit_type
        ],
        outputs=my_submit_html
    )

    back_my_submit.click(
        lambda: (
            gr.update(visible=True),
            gr.update(visible=False)
        ),
        outputs=[
            dashboard_page,
            my_submit_page
        ]
    )

   #个人信息页面
    def open_my_profile(username):
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            build_my_profile_html(
                username
            )
        )

    # back_my_profile.click(
    #     lambda: (
    #         gr.update(visible=True),
    #         gr.update(visible=False)
    #     ),
    #     outputs=[
    #         dashboard_page,
    #         profile_page
    #     ]
    # )

    (
        my_project_page,
        my_project_summary_html,
        my_project_html,
        my_project_modal_html,#model_html
        project_summary_html,
        project_kpi_html,
        refresh_project_kpi_btn,
        my_current_project_id,
        edit_my_project_progress_id,
        load_old_project_progress_btn,
        save_edit_progress_btn,
        edit_my_project_progress_content,
        edit_my_project_risk_content,
        edit_my_project_next_plan,
        load_my_project_progress_btn,#load_project_btn
        my_project_progress_content,# progress_content
        my_project_risk_content,#risk_content
        my_project_next_plan,#next_plan
        submit_progress_btn,
        result_msg,
        my_ai_btn,
        ai_html,
        my_project_progress_history_html,
        refresh_progress_btn,
        delete_my_project_progress_id,
        delete_my_project_progress_btn,
        back_btn
    ) = create_my_project_page()

    back_btn.click(
        fn=lambda: (
            gr.update(visible=True),
            gr.update(visible=False)
        ),

        outputs=[
            dashboard_page,
            my_project_page
        ]
    )

    submit_progress_btn.click(
        fn=add_my_project_progress,
        inputs=[
            my_current_project_id,
            real_name_state,
            my_project_progress_content,
            my_project_risk_content,
            my_project_next_plan
        ],
       outputs=result_msg
    )

    def open_ai_page():
        return (
            gr.update(
                visible=False
            ),
            gr.update(
                visible=True
            )
        )


    my_ai_btn.click(
        fn=build_my_project_ai_analysis,
        inputs=my_current_project_id,
        outputs=ai_html
    )

    refresh_project_kpi_btn.click(
        fn=build_my_project_kpi_html,
        inputs=my_current_project_id,
        outputs=project_kpi_html
    )

    load_old_project_progress_btn.click(
        fn=load_my_progress,
        inputs=edit_my_project_progress_id,
        outputs=[
            my_project_progress_content,
            my_project_risk_content,
            my_project_next_plan
        ]
    )

    save_edit_progress_btn.click(
        fn=update_progress_and_refresh,
        inputs=[
            edit_my_project_progress_id,
            my_current_project_id,
            real_name_state,
            edit_my_project_progress_content,
            edit_my_project_risk_content,
            edit_my_project_next_plan
        ],
        outputs=my_project_progress_history_html
    )

    delete_my_project_progress_btn.click(

        fn=delete_progress_and_refresh,

        inputs=[
            delete_my_project_progress_id,
            my_current_project_id,
            real_name_state
        ],

        outputs=my_project_progress_history_html
    )

    back_project_manager.click(
        fn=lambda: (
            gr.update(visible=True),
            gr.update(visible=False)
        ),
        outputs=[
            project_center_page,
            project_manager_page
        ]
    )

#选择项目自动刷新历史记录
    refresh_progress_btn.click(
        fn=build_my_project_progress_html,
        inputs=[
            my_current_project_id,
            real_name_state
        ],
        outputs=my_project_progress_history_html
    )

    def delete_progress_and_refresh(progress_id, project_id):
        delete_project_progress(progress_id)
        return build_project_detail_html(
            project_id
        )

    delete_progress_btn.click(
        fn=delete_progress_and_refresh,
        inputs=[
            delete_progress_id,
            current_project_id
        ],
        outputs=project_detail_html
    )


    def load_progress(progress_id):
        row = get_progress_by_id(
            progress_id
        )

        if not row:
            return "", "", ""

        return (

            row[1],
            row[2],
            row[3]
        )

    load_progress_btn.click(
        fn=load_progress,
        inputs=edit_progress_id,
        outputs=[
            progress_content,
            risk_content,
            next_plan
        ]
    )

    def refresh_overview(range_type):

        return build_overview_html(range_type)

    def change_pwd_and_logout(
            username,
            old_pwd,
            new_pwd,
            confirm_pwd
    ):

        msg = change_password(
            username,
            old_pwd,
            new_pwd,
            confirm_pwd
        )

        if "成功" in msg:

            return (
                gr.update(visible=True),
                gr.update(visible=False)
            )

        raise gr.Error(msg)


    # submit_btn.click(
    #     change_pwd_and_logout,
    #     inputs=[
    #         user_state,
    #         old_pwd,
    #         new_pwd,
    #         confirm_pwd
    #     ],
    #     outputs=[
    #
    #         user_state,
    #         role_state,
    #
    #         login_page,
    #         dashboard_page,
    #         leader_page,
    #         password_page,
    #
    #         current_user,
    #         logout_btn
    #     ]
    # )


    def save_user(data):

        import json

        obj = json.loads(data)

        update_user(
            obj["username"],
            obj["name"],
            obj["phone"],
            obj["role"]
        )

        gr.Info("用户修改成功")
        return build_user_html()

    save_user_event.change(
        fn=save_user,
        inputs=save_user_event,
        outputs=user_html
    )


    def remove_project(project_id):
        delete_project_api(project_id)
        gr.Warning("项目已删除")
        return build_project_html()


    delete_project_event.change(
        fn=remove_project,
        inputs=delete_project_event,
        outputs=project_center_html
    )


    def do_delete_user(username):
        delete_user_by_name(username)
        gr.Info("用户删除成功")
        return build_user_html()

    delete_user_event.change(
        fn=do_delete_user,
        inputs=delete_user_event,
        outputs=user_html
    )

    # ====================================================
    # 登录
    # ====================================================
    def do_login(user, pwd):

        result = login_check(user, pwd)

        if not result:
            return (

                "",
                "",
                "",

                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),

                gr.update(),
                gr.update(),

                "用户名或密码错误",
                ""
            )

        role = result[0]
        real_name = result[1]

        if not real_name:
            real_name = user
        reporter.value = real_name

        print(
            "登录用户:",
            user,
            role,
            real_name
        )

        if role == "leader":
            return (

                user,
                role,
                real_name,

                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),

                gr.update(
                    value=f"👤 {user}",
                    visible=True
                ),

                gr.update(visible=True),

                "",
                real_name
            )

        return (

            user,
            role,
            real_name,

            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),

            gr.update(
                value=f"👤 {user}",
                visible=True
            ),

            gr.update(visible=True),

            "",
            real_name
        )

    def show_register():
        return (
            gr.update(visible=False),
            gr.update(visible=True)
        )

    def hide_register():
        return gr.update(visible=False)

    def show_login():
        return (
            gr.update(visible=True),
            gr.update(visible=False)
        )


    login_btn.click(
        fn=do_login,
        inputs=[username, password],
        outputs=[
            user_state,
            role_state,
            real_name_state,

            login_page,
            dashboard_page,
            leader_page,

            current_user,
            logout_btn,

            login_msg,
            reporter
        ]
    ).then(
        fn=build_dashboard_v14,
        inputs=[user_state, real_name_state],
        outputs=dashboard_html
    ).then(
    fn=None,
    js="""
    () => {

        console.log("Dashboard Loaded");

        setTimeout(()=>{

            if(window.afterDashboardRender){

                window.afterDashboardRender();

            }

        },500);

    }
    """
)

    register_btn.click(
        show_register,
        outputs=[
            login_panel,
            register_panel
        ]
    )

    back_login_btn.click(
        show_login,
        outputs=[
            login_panel,
            register_panel
        ]
    )

    # btn_change_pwd.click(
    #     lambda: (
    #         gr.update(visible=False),
    #         gr.update(visible=True)
    #     ),
    #     outputs=[
    #         dashboard_page,
    #         password_page
    #     ]
    # )

    def register_and_back(
            username,
            password,
            real_name,
            phone
    ):

        msg = register_user(
            username,
            password,
            real_name,
            phone
        )

        # 注册成功
        if "成功" in msg:
            gr.Info(msg)
            return (
                gr.update(visible=True),  # login_panel
                gr.update(visible=False)  # register_panel
            )

        # 注册失败
        raise gr.Error(msg)

    reg_submit.click(
        register_and_back,
        inputs=[
            reg_user,
            reg_pwd,
            reg_name,
            reg_phone
        ],
        outputs=[
            login_panel,
            register_panel
        ]
    )


    def generate_business_ai():

        result = build_business_analysis_html()

        return wrap_analysis(result)


    generate_ai_btn.click(

        fn=generate_business_ai,

        outputs=cockpit_ai_analysis_html
    )


    # ====================================================
    # 打开管理端 用户管理页
    # ====================================================
    # def open_user_manager():
    #
    #     data = get_user_list()
    #
    #     print(data)
    #
    #     df = pd.DataFrame(
    #         data,
    #         columns=[
    #             "用户名",
    #             "角色",
    #             "姓名",
    #             "手机号",
    #             "创建时间"
    #         ]
    #     )
    #
    #     return (
    #         gr.update(visible=False),
    #         gr.update(visible=True),
    #         df
    #     )

    def open_user_manager():
        data = build_user_html()
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(value=data)
        )


    def open_customer_page():

        html = build_customer_html()

        return (

            gr.update(visible=False),

            gr.update(visible=True),

            html
        )

    # ====================================================
    # 工作台 -> 客户管理
    # ====================================================
    btn_customer.click(
        fn=open_customer_page,
        outputs=[
            leader_page,
            customer_page
        ]
    )

    # ====================================================
    # 退出登录
    # ====================================================
    def logout():

        return (
            "",  # user_state
            "",  # role_state

            gr.update(visible=True),  # login_page

            gr.update(visible=True),  # login_panel
            gr.update(visible=False),  # register_panel

            gr.update(visible=False),  # dashboard_page
            gr.update(visible=False),  # leader_page
            gr.update(visible=False),  # project_page
            gr.update(visible=False),  # meeting_page
            gr.update(visible=False),  # daily_page
            # gr.update(visible=False),  # password_page

            gr.update(
                value="",
                visible=False
            ),

            gr.update(visible=False)
        )

    logout_btn.click(
        logout,
        outputs=[
            user_state,
            role_state,

            login_page,

            login_panel,
            register_panel,

            dashboard_page,
            leader_page,
            project_page,
            meeting_page,
            daily_page,
            # password_page,

            current_user,
            logout_btn
        ],

        js="""
        () => {
            location.reload();
        }
        """
    )

    # ====================================================
    # 工作台 -> 项目汇报
    # ====================================================
    # btn_project_report.click(
    #     lambda: (
    #         gr.update(visible=False),
    #         gr.update(visible=True)
    #     ),
    #     outputs=[
    #         dashboard_page,
    #         project_page
    #     ]
    # )

    # ====================================================
    # 工作台 -> 我的项目
    # ====================================================
    def open_my_project(real_name):
        print("当前用户=", real_name)
        return (

            gr.update(visible=False),

            gr.update(visible=True),

            build_my_project_summary_html(
                real_name
            ),

            build_my_project_html(
                real_name
            )
        )

    # btn_my_project.click(
    #     fn=open_my_project,
    #     inputs=real_name_state,
    #     outputs=[
    #         dashboard_page,
    #         my_project_page,
    #         my_project_summary_html,
    #         my_project_html
    #     ]
    # )

    # ====================================================
    # 工作台 -> 会议记录
    # ====================================================
    # btn_meeting.click(
    #     lambda: (
    #         gr.update(visible=False),
    #         gr.update(visible=True)
    #     ),
    #     outputs=[
    #         dashboard_page,
    #         meeting_page
    #     ]
    # )

    # ====================================================
    # 客户管理 -> 工作台
    # ====================================================
    back_customer.click(
        lambda: (
            gr.update(visible=True),
            gr.update(visible=False)
        ),
        outputs=[
            leader_page,
            customer_page
        ]
    )

    def open_daily_page(real_name):
        print("进入日报页面")
        print("real_name =", real_name)
        return (
            gr.update(visible=False),  # dashboard
            gr.update(visible=True),  # daily
            gr.update(value=real_name)
        )


    def load_user_table():
        return build_user_html()


    def open_delete(username):

        return (
            gr.update(visible=True),
            f"确定删除用户：{username}？"
        )


    daily_entry_btn = gr.Button(
        visible=False,
        elem_id="daily_entry_btn"
    )

    meeting_entry_btn = gr.Button(
        visible=False,
        elem_id="meeting_entry_btn"
    )

    project_entry_btn = gr.Button(
        visible=False,
        elem_id="project_entry_btn"
    )

    daily_entry_btn.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            dashboard_page,
            daily_page
        ]
    )

    meeting_entry_btn.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            dashboard_page,
            meeting_page
        ]
    )

    project_entry_btn.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            dashboard_page,
            project_page
        ]
    )

    ai_daily_btn = gr.Button(
        value="ai_daily",
        elem_id="ai_daily_btn",
        elem_classes=["hidden-trigger"]
    )

    ai_weekly_btn = gr.Button(
        value="ai_weekly",
        elem_id="ai_weekly_btn",
        elem_classes=["hidden-trigger"]
    )

    ai_project_btn1 = gr.Button(
        value="ai_project",
        elem_id="ai_project_btn1",
        elem_classes=["hidden-trigger"]
    )

    ai_risk_btn = gr.Button(
        value="ai_risk",
        elem_id="ai_risk_btn",
        elem_classes=["hidden-trigger"]
    )

    ai_meeting_btn = gr.Button(
        value="ai_meeting",
        elem_id="ai_meeting_btn",
        elem_classes=["hidden-trigger"]
    )

    ai_chat_btn = gr.Button(
        value="ai_chat",
        elem_id="ai_chat_btn",
        elem_classes=["hidden-trigger"]
    )



    ai_result_box = gr.Textbox(
        visible=False,
        elem_id="ai_result_box"
    )

    ai_result_box.change(
        None,
        inputs=ai_result_box,
        outputs=ai_result_box,
        js="""
        (text)=>{
            window.dispatchEvent(
                new CustomEvent(
                    "ai-result-update",
                    {detail:text}
                )
            );
            return [];
        }
        """
    )

    ai_question_event = gr.Textbox(
        value="",
        visible=True,
        elem_id="ai_question_event",
        elem_classes=["hidden-trigger"]
    )

    # ai_chat_btn.click(
    #     ai_agent,
    #     inputs=[
    #         user_state,
    #         ai_question_event
    #     ],
    #     outputs=ai_result_box
    # )

    ai_chat_btn.click(
        lambda u, q: print(
            "触发成功",
            u,
            q
        ),
        inputs=[
            user_state,
            ai_question_event
        ]
    )

    ai_send_btn = gr.Button(
        value="send",
        visible=True,
        elem_id="ai_send_btn",
        elem_classes=["hidden-trigger"]
    )

    ai_send_btn.click(

        ai_agent,

        inputs=[
            user_state,
            ai_question_event
        ],

        outputs=ai_result_box

    )

    print(type(ai_question_event))


    ai_daily_btn.click(
        generate_ai_daily,
        inputs=user_state,
        outputs=ai_result_box
    )

    ai_weekly_btn.click(
        generate_ai_weekly,
        inputs=user_state,
        outputs=ai_result_box
    )

    ai_project_btn1.click(
        generate_project_summary,
        inputs=user_state,
        outputs=ai_result_box
    )

    ai_meeting_btn.click(
        generate_ai_meeting_summary,
        inputs=real_name_state,
        outputs=ai_result_box
    )

    ai_risk_btn.click(
        generate_ai_risk_report,
        inputs=real_name_state,
        outputs=ai_result_box
    )

    # ai_question_event.change(
    #     ai_rag_chat,
    #     inputs=ai_question_event,
    #     outputs=ai_result_box
    # )

    # pwd_result = gr.Textbox(
    #     elem_id="pwd_result"
    # )

    rebuild_vector_btn = gr.Button(
        visible=False
    )

    rebuild_vector_btn.click(
        rebuild_vector_db,
        outputs=ai_result_box
    )

    change_pwd_btn = gr.Button(

        value="change_pwd",

        elem_id="change_pwd_btn",

        elem_classes=["hidden-trigger"]

    )

    old_pwd_event = gr.Textbox(
        value="",
        elem_id="old_pwd_event",
        elem_classes=["hidden-trigger"]
    )

    new_pwd_event = gr.Textbox(
        value="",
        elem_id="new_pwd_event",
        elem_classes=["hidden-trigger"]
    )
    trigger = gr.State()  # 状态变量接收成功标记
    click_event = change_pwd_btn.click(
        change_password,
        inputs=[
            user_state,
            old_pwd_event,
            new_pwd_event
        ],
        outputs=[trigger]
    )

    click_event.then(
        fn=lambda x: None,
        inputs=[trigger],
        outputs=[],
        js="""
            function(success) {
                if (success) {
                    alert("密码修改成功，请重新登录");
                    // 刷新当前页面
                    window.location.reload();
                    // 跳登录页替换上面：window.location.href="/login";
                }
            }
            """
    )



    # ====================================================
    # 项目页 -> 工作台
    # ====================================================
    back_project.click(
        fn=lambda username, real_name: (
            gr.update(visible=False),
            gr.update(visible=True),
            build_dashboard_v14(
                username,
                real_name
            )
        ),

        inputs=[
            user_state,
            real_name_state
        ],

        outputs=[
            project_page,
            dashboard_page,
            dashboard_html
        ]
    ).then(
            fn=None,
            js="""
            () => {
                setTimeout(()=>{
                    if(window.initDashboardCharts){
                        initDashboardCharts();
                    }
                },500);
            }
            """
        )

    # ====================================================
    # 会议页 -> 工作台
    # ====================================================
    back_meeting.click(
        fn=lambda username, real_name: (
            gr.update(visible=False),
            gr.update(visible=True),
            build_dashboard_v14(
                username,
                real_name
            )
        ),

        inputs=[
            user_state,
            real_name_state
        ],

        outputs=[
            meeting_page,
            dashboard_page,
            dashboard_html
        ]
    ).then(
            fn=None,
            js="""
            () => {
                setTimeout(()=>{
                    if(window.initDashboardCharts){
                        initDashboardCharts();
                    }
                },500);
            }
            """
        )

    # ====================================================
    # 日报页 -> 工作台
    # ====================================================
    back_daily.click(
        fn=lambda username, real_name: (
            gr.update(visible=False),
            gr.update(visible=True),
            build_dashboard_v14(
                username,
                real_name
            )
        ),

        inputs=[
            user_state,
            real_name_state
        ],

        outputs=[
            daily_page,
            dashboard_page,
            dashboard_html
        ]
    ).then(
            fn=None,
            js="""
            () => {
        
                setTimeout(()=>{
        
                    if(window.initDashboardCharts){
        
                        initDashboardCharts();
        
                    }
        
                },500);
        
            }
            """
        )

    # ====================================================
    # 修改密码 -> 工作台
    # ====================================================
    # back_password.click(
    #     lambda: (
    #         gr.update(visible=True),
    #         gr.update(visible=False)
    #     ),
    #     outputs=[
    #         dashboard_page,
    #         password_page
    #     ]
    # )

    # ====================================================
    # AI工作流查询
    # ====================================================
    def open_ai_workflow():
        kpi1, kpi2, kpi3 = build_kpi_html()
        summary_html, risk_html, rank_html = (
            build_ai_side_panel()
        )
        return (
            gr.update(visible=False),

            gr.update(visible=True),

            kpi1,
            kpi2,
            kpi3,

            summary_html,
            risk_html,
            rank_html
        )

    btn_ai_query.click(
        fn=open_ai_workflow,
        outputs=[
            leader_page,
            workflow_ai_page,
            kpi_project,
            kpi_daily,
            kpi_risk,
            ai_summary,
            ai_risk,
            project_rank
        ]
    )

    # ====================================================
    # 驾驶舱按钮
    # ====================================================
    def open_cockpit():

        return (

            gr.update(visible=False),

            gr.update(visible=True),

            build_cockpit_html(),

            """
            <div class='ai-analysis-card'>
            点击生成经营分析
            </div>
            """,
            build_warning_html()
        )

    btn_cockpit.click(
        fn=open_cockpit,
        outputs=[
            leader_page,
            cockpit_page,

            cockpit_html,
            cockpit_ai_analysis_html,
            warning_html
        ]
    )

    back_cockpit.click(
        fn=lambda: (
            gr.update(visible=True),
            gr.update(visible=False)
        ),
        outputs=[
            leader_page,
            cockpit_page
        ]
    )

    # ====================================================
    # 用户管理按钮
    # ====================================================
    btn_user_manager.click(
        fn=lambda: (
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            leader_page,
            user_manager_page
        ]
    ).then(
        fn=build_user_html,
        outputs=user_html
    )


    back_ai.click(
        fn=lambda: (
            build_overview_html(),
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            overview_html,
            workflow_ai_page,
            leader_page
        ]
    )

    # ====================================================
    # 用户管理页
    # ====================================================
    back_user_manager.click(
        fn=lambda: (
            build_overview_html(),
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            overview_html,
            user_manager_page,
            leader_page
        ]
    )

    # ====================================================
    # 驾驶舱返回到工作台
    # ====================================================
    back_business_dashboard.click(
        lambda: (
            gr.update(visible=True),
            gr.update(visible=False)
        ),
        outputs=[
            leader_page,
            business_dashboard_page
        ]
    )


    def open_project_center():

        return (

            gr.update(visible=False),

            gr.update(visible=True),

            build_project_html()
        )


    btn_project_center.click(

        open_project_center,

        outputs=[

            leader_page,

            project_center_page,

            project_center_html
        ]
    )

    back_project_center.click(
        lambda: (
            gr.update(visible=True),
            gr.update(visible=False)
        ),
        outputs=[
            leader_page,
            project_center_page
        ]
    )

    project_detail_event = gr.Textbox(
        visible=False,
        container=False
    )


    def open_project_detail(project_id):

        return (

            gr.update(visible=False),

            gr.update(visible=True),

            build_project_detail_html(
                int(project_id)
            )
        )


    project_detail_event.change(
        fn=open_project_detail,
        inputs=project_detail_event,
        outputs=[
            project_center_page,
            project_detail_page,
            project_detail_html
        ]
    )

    add_progress_btn.click(
        fn=lambda pid, content, risk, nextp:
        add_project_progress(
            pid,
            content,
            risk,
            nextp,
            "当前用户"
        ),

        inputs=[
            current_project_id,
            progress_content,
            risk_content,
            next_plan
        ]
    )


    def load_progress(progress_id):
        row = get_progress_by_id(
            progress_id
        )

        if not row:
            return "", "", ""

        return (

            row[1],
            row[2],
            row[3]
        )


    load_progress_btn.click(
        fn=load_progress,

        inputs=edit_progress_id,

        outputs=[

            edit_progress_content,

            edit_risk_content,

            edit_next_plan
        ]
    )

    # add_btn.click(
    #     fn=lambda: """
    #     <script>
    #     document.getElementById('projectModal').style.display='flex'
    #     </script>
    #     """,
    #     outputs=project_modal_html
    # )

    add_btn.click(
        fn=lambda: (
            gr.update(visible=False),
            gr.update(visible=True),
            build_project_html()
        ),
        outputs=[
            project_center_page,
            project_manager_page,
            project_manager_html
        ]
    ).then(
        fn=None,
        js="""
        () => {
            setTimeout(() => {
                addProject();
            }, 300);
        }
        """
    )

    new_project_btn.click(
        fn=None,
        js="() => addProject()"
    )

    refresh_project_btn.click(
        fn=build_project_html,
        outputs=project_manager_html
    )

    add_member_btn.click(
        fn=add_member_and_refresh,

        inputs=[
            current_project_id,
            member_name,
            member_role
        ],

        outputs=project_detail_html
    )

    delete_member_btn.click(
        fn=delete_project_member,

        inputs=delete_member_id
    )

    add_risk_btn.click(

        fn=add_risk_and_refresh,

        inputs=[

            current_project_id,

            risk_level,
            risk_desc,
            risk_solution

        ],

        outputs=project_detail_html
    )

    delete_risk_btn.click(

        fn=delete_risk_and_refresh,

        inputs=[
            delete_risk_id,
            current_project_id
        ],

        outputs=project_detail_html
    )

    ai_project_btn.click(
        fn=build_project_ai_analysis,
        inputs=current_project_id,
        outputs=ai_project_html
    )

    save_progress_btn.click(
        fn=lambda pid,
                  content,
                  risk,
                  nextp,
                  username:
        add_project_progress(
            pid,
            content,
            risk,
            nextp,
            username
        ),

        inputs=[
            current_project_id,
            progress_content,
            risk_content,
            next_plan,
            user_state
        ],
        outputs=progress_result
    )



demo.queue(default_concurrency_limit=1)
demo.launch(
    server_name="0.0.0.0",
    server_port=7864,
    share=False,
    allowed_paths=["static"],
    show_error=False
)