import gradio as gr


def create_project_manager_page():

    with gr.Column(
        visible=False,
        elem_classes=["user-page"]
    ) as page:

        gr.HTML("""
        <div class="breadcrumb">
            管理后台 > 项目管理
        </div>
        """)
        project_html = gr.HTML()

        modal_html = gr.HTML("""

<!-- 编辑项目弹窗 -->
<div id="projectModal"
     class="custom-modal"
     style="display:none">

    <div class="custom-modal-content">

        <h3 id="project_modal_title">
            编辑项目
        </h3>

        <input
            id="p_id"
            type="hidden"
        />

        <label>项目名称</label>
        <input
            id="p_name"
            placeholder="项目名称"
        />
        
        <label>项目负责人</label>
        <input
            id="p_leader"
            placeholder="项目负责人"
        />
        
        <label>开发人员（多个逗号分隔）</label>
        <input
            id="p_developers"
            placeholder="张工"
        />
        
        <label>测试人员（多个逗号分隔）</label>
        <input
            id="p_testers"
            placeholder="王工"
        />
        
        <label>UI设计</label>
        <input
            id="p_designer"
            placeholder="设计师"
        />
        
        <label>结构工程师</label>
        <input
            id="p_structure"
            placeholder="结构工程师"
        />
        
        <label>开始日期</label>
        <input
            id="p_start_date"
            type="date"
        />
        
        <label>结束日期</label>
        <input
            id="p_end_date"
            type="date"
        />

        <textarea
            id="p_progress"
            rows="4"
            placeholder="项目进度">
        </textarea>

        <label>是否延期</label>

        <select id="p_delay">
        
            <option value="否">
                否
            </option>
        
            <option value="是">
                是
            </option>
        
        </select>

        <textarea
            id="p_risk"
            rows="3"
            placeholder="风险说明">
        </textarea>

        <div style="
            display:flex;
            gap:12px;
            margin-top:20px;
        ">

            <button
                class="blue-btn"
                onclick="saveProject()"
            >
                保存
            </button>

            <button
                onclick="closeProjectModal()"
            >
                取消
            </button>

        </div>

    </div>

</div>


<!-- 删除项目弹窗 -->
<div id="projectDeleteModal"
     class="custom-modal"
     style="display:none">

    <div class="custom-modal-content">

        <h3>
            删除项目
        </h3>

        <p id="delete_project_name">
        </p>

        <div style="
            display:flex;
            gap:12px;
            margin-top:20px;
        ">

            <button
                class="delete-btn"
                onclick="confirmDeleteProject()"
            >
                确认删除
            </button>

            <button
                onclick="closeProjectDeleteModal()"
            >
                取消
            </button>

        </div>

    </div>

</div>


<!-- 删除项目进展弹窗 -->
<div id="deleteProgressModal"
     class="custom-modal"
     style="display:none">

    <div class="custom-modal-content">

        <h3>
            删除项目进展
        </h3>

        <p>
            确定删除这条项目进展？
        </p>

        <div style="
            display:flex;
            gap:12px;
            margin-top:20px;
        ">

            <button
                class="delete-btn"
                onclick="confirmDeleteProgress()"
            >
                删除
            </button>

            <button
                onclick="closeDeleteProgressModal()"
            >
                取消
            </button>

        </div>

    </div>

</div>

<!-- 项目详情弹窗 -->

<div id="projectViewModal"
     class="custom-modal"
     style="display:none">

    <div class="custom-modal-content">

        <h3>
            项目详情
        </h3>

        <div id="project_detail_content">

        </div>

        <button
            onclick="closeProjectViewModal()"
        >
            关闭
        </button>

    </div>

</div>

""")
        with gr.Row():
            new_project_btn = gr.Button(
                "➕ 新增项目",
                variant="primary",
                elem_classes=["btn-new-project"]
            )
            refresh_project_btn = gr.Button(
                "🔄 刷新项目",
                elem_classes=["btn-refresh"]
            )
            back_btn = gr.Button(
                "返回管理后台",
                elem_classes=["btn-back"]
            )

        save_project_event = gr.Textbox(
            value="",
            elem_id="save_project_event",
            container=False
        )

        delete_project_event = gr.Textbox(
            value="",
            elem_id="delete_project_event",
            container=False
        )

    return (
        page,
        project_html,
        modal_html,
        new_project_btn,
        refresh_project_btn,
        back_btn,
        save_project_event,
        delete_project_event
    )