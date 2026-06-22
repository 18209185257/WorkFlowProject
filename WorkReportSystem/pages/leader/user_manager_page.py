import gradio as gr

def create_user_manager_page():


  with gr.Column(
      visible=False,
      elem_classes=["user-page"],

  ) as page:

      gr.HTML("""
      <div class="breadcrumb">
          管理后台 > 用户管理
      </div>
      """)

      user_html = gr.HTML()

      modal_html = gr.HTML("""

  <div id="editModal" class="custom-modal" style="display:none">


  <div class="custom-modal-content">

      <h3>编辑用户</h3>

      <input id="m_username" readonly placeholder="用户名">

      <input id="m_name" placeholder="姓名">

      <input id="m_phone" placeholder="手机号">

      <select id="m_role">
          <option value="user">user</option>
          <option value="leader">leader</option>
      </select>

      <div
          style="
              margin-top:20px;
              display:flex;
              gap:16px;
          "
      >

          <button
              onclick="window.saveUser()"
              style="
                  background:#1677ff;
                  color:white;
                  border:none;
                  padding:10px 20px;
                  border-radius:6px;
                  cursor:pointer;
              "
          >
              保存
          </button>

          <button
              onclick="window.closeEditModal()"
              style="
                  background:#d9d9d9;
                  border:none;
                  padding:10px 20px;
                  border-radius:6px;
                  cursor:pointer;
              "
          >
              取消
          </button>

      </div>

  </div>

  </div>

<div
    id="deleteModal"
    class="custom-modal"
    style="display:none"
>

    <div class="custom-modal-content">

        <h3>删除用户</h3>

        <p id="delete_username"></p>

        <div
            style="
                display:flex;
                gap:16px;
                margin-top:20px;
            "
        >

            <button
                onclick="confirmDeleteUser()"
                style="
                    background:#ff4d4f;
                    color:white;
                    border:none;
                    padding:10px 20px;
                    border-radius:6px;
                    cursor:pointer;
                "
            >
                确认删除
            </button>

            <button
                onclick="closeDeleteModal()"
                style="
                    background:#d9d9d9;
                    border:none;
                    padding:10px 20px;
                    border-radius:6px;
                    cursor:pointer;
                "
            >
                取消
            </button>

        </div>

    </div>

</div>
      """)

      back_btn = gr.Button(
          "返回管理后台"
      )

  return (
      page,
      user_html,
      modal_html,
      back_btn
  )

