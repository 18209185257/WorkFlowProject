import re


def extract_real_name(
        question
):

    names = re.findall(
        r'[\u4e00-\u9fa5]{2,4}',
        question
    )

    for n in names:

        if (
            "工作" not in n
            and
            "最近" not in n
            and
            "总结" not in n
        ):
            return n

    return ""

def build_employee_summary_prompt(
        real_name,
        work
):

    return f"""
你是企业领导助手。

下面是员工最近日报：

员工：

{real_name}

日报：

{work}

请生成：

1、最近工作总结

2、工作亮点

3、风险问题

4、领导建议

不要输出模板。
"""

