from common.db import get_project_conn


def get_order_list():

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        id,
        customer_name,
        order_name,
        order_amount,
        order_status,
        sign_date
    FROM sales_order
    ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def build_order_html():

    rows = get_order_list()

    html = """
    <div class='user-table'>

    <div class='user-manage-row header'>
        <div>客户</div>
        <div>订单</div>
        <div>金额</div>
        <div>状态</div>
        <div>签约日期</div>
    </div>
    """

    for r in rows:

        html += f"""
        <div class='user-manage-row'>
            <div>{r[1]}</div>
            <div>{r[2]}</div>
            <div>¥{r[3]:,.0f}</div>
            <div>{r[4]}</div>
            <div>{r[5]}</div>
        </div>
        """

    html += "</div>"

    return html