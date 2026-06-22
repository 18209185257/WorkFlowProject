import requests
from common.db import get_project_conn

from common.config import (
    API_HOST,
    TOKEN,
    TODAY
)

def get_customer_list():
    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select
            id,
            customer_name,
            contact_name,
            phone,
            email,
            address,
            create_time
        from customer
        order by id desc
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def build_customer_html():

    rows = get_customer_list()

    html = """
        <div class="user-table">

            <div class="user-manage-row header">

            <div>客户名称</div>

            <div>联系人</div>
            
            <div>联系电话</div>
            
            <div>邮箱</div>
            
            <div>地址</div>
            
            <div>创建时间</div>

            <div>操作</div>

        </div>
    """

    for row in rows:
        customer_id = row[0]

        customer_name = row[1]

        contact_name = row[2]

        phone = row[3]

        email = row[4]

        address = row[5]

        create_time = row[6]

        html += f"""
        <div class="user-manage-row">

           <div>{customer_name}</div>

            <div>{contact_name}</div>
            
            <div>{phone}</div>
            
            <div>{email}</div>
            
            <div>{address}</div>
            
            <div>{create_time}</div>

            <div>

                <button
                class="edit-btn"
                onclick="editCustomer(
                '{customer_id}',
                `{customer_name}`,
                `{contact_name}`,
                `{phone}`,
                `{email}`,
                `{address}`
                )">

                编辑

                </button>

                <button
                class="delete-btn"
                onclick="deleteCustomer('{customer_id}')">

                删除

                </button>

            </div>

        </div>
        """

    html += "</div>"

    return html


def build_customer_kpi_html():

    rows = get_customer_list()

    total = len(rows)

    return f"""
    <div class="kpi-row">

        <div class="kpi-card">

            <div class="kpi-value">
                {total}
            </div>

            <div class="kpi-label">
                客户总数
            </div>

        </div>

    </div>
    """

def add_customer(
    customer_name,
    contact_name,
    phone,
    email,
    address
):

    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        insert into customer
        (
            customer_name,
            contact_name,
            phone,
            email,
            address,
            create_time
        )
        values
        (
            ?,?,?,?,?,?
        )
        """,
        (
            customer_name,
            contact_name,
            phone,
            email,
            address,
            TODAY
        )
    )
    conn.commit()
    conn.close()

def update_customer(data):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        update customer
        set

            customer_name=?,
            contact_name=?,
            phone=?,
            email=?,
            address=?

        where id=?
        """,
        (
            data["customer_name"],
            data["contact_name"],
            data["phone"],
            data["email"],
            data["address"],
            data["id"]
        )
    )
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        delete from customer
        where id=?
        """,
        (customer_id,)
    )
    conn.commit()
    conn.close()

