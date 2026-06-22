import hashlib


def deduplicate_data(data_list):
    """
    日报/会议数据去重
    """

    unique = []
    seen = set()

    if not isinstance(data_list, list):
        return []

    for item in data_list:

        if not isinstance(item, list):
            continue

        if len(item) < 5:
            continue

        content_text = str(item[2]).strip()

        content_hash = hashlib.md5(
            content_text.encode("utf-8")
        ).hexdigest()

        key = f"{item[3]}|{content_hash}"

        if key not in seen:
            seen.add(key)
            unique.append(item)

    unique.sort(
        key=lambda x: x[3]
    )

    return unique
