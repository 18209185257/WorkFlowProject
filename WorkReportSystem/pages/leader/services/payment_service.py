from common.db import get_project_conn


def get_payment_list():

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        customer_name,
        order_name,
        payment_amount,
        payment_date
    FROM payment_record
    ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def build_payment_html():

    rows = get_payment_list()

    html = """
    <div class='user-table'>

    <div class='user-manage-row header'>
        <div>客户</div>
        <div>订单</div>
        <div>回款金额</div>
        <div>回款日期</div>
    </div>
    """

    for r in rows:

        html += f"""
        <div class='user-manage-row'>
            <div>{r[0]}</div>
            <div>{r[1]}</div>
            <div>¥{r[2]:,.0f}</div>
            <div>{r[3]}</div>
        </div>
        """

    html += "</div>"

    return html