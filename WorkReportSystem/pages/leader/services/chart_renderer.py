import json

def render_chart(
        chart_id,
        option,
        height=350
):

    return f"""
    <div
        class="leader-chart"

        data-chart-id="{chart_id}"

        data-option='{json.dumps(option)}'

        style="
            height:{height}px;
            width:100%;
        "
    >
    </div>
    """