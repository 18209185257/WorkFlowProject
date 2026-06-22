import gradio as gr

from pages.customer.services.customer_service import (
    build_customer_html,
    build_customer_kpi_html
)


def create_customer_page():

    with gr.Column(
        visible=False,
        elem_classes=["customer-page"]
    ) as page:

        gr.HTML("""
        <div class="section-title">
            👥 客户管理
        </div>
        """)

        # KPI
        customer_kpi = gr.HTML(
            value=build_customer_kpi_html()
        )

        customer_html = gr.HTML(
            value=build_customer_html()
        )

        modal_html = gr.HTML("""

        <div id="customerModal"
             class="custom-modal"
             style="display:none">

            <div class="custom-modal-content">

                <h3 id="customer_modal_title">
                    新增客户
                </h3>

                <input id="c_id" type="hidden"/>

                <label>客户名称</label>
                <input id="c_name"/>

                <label>联系人</label>
                <input id="c_contact"/>

                <label>联系电话</label>
                <input id="c_phone"/>

                <label>邮箱</label>
                <input id="c_email"/>

                <label>地址</label>
                <input id="c_address"/>

                <div style="margin-top:20px">

                    <button
                        class="blue-btn"
                        onclick="saveCustomer()">
                        保存
                    </button>

                    <button
                        onclick="closeCustomerModal()">
                        取消
                    </button>

                </div>

            </div>

        </div>

        """)

        with gr.Row(elem_classes=["customer-row"]):
            add_btn = gr.Button(
                "➕ 新增客户",
                variant="primary",
                elem_id="customer_add_btn",
                elem_classes=["btn-new-project"]
            )
            refresh_btn = gr.Button(
                "🔄 刷新",
                elem_classes=["btn-refresh"]
            )
            back_btn = gr.Button(
                "返回管理后台",
                elem_classes=["btn-back"]
            )

        refresh_btn.click(
            fn=lambda: (
                build_customer_kpi_html(),
                build_customer_html()
            ),
            outputs=[
                customer_kpi,
                customer_html
            ]
        )

        save_customer_event = gr.Textbox(
            value="",
            elem_id="save_customer_event",
            container=False
        )

        delete_customer_event = gr.Textbox(
            value="",
            elem_id="delete_customer_event",
            container=False
        )

    return (
        page,
        customer_kpi,
        customer_html,
        modal_html,
        add_btn,
        refresh_btn,
        back_btn,
        save_customer_event,
        delete_customer_event
    )