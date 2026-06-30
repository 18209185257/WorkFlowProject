import os


KNOWLEDGE_DIR = (
    "knowledge_base"
)


def load_all_knowledge():

    content = []

    if not os.path.exists(
        KNOWLEDGE_DIR
    ):
        return ""

    for filename in os.listdir(
        KNOWLEDGE_DIR
    ):

        if not filename.endswith(
            ".md"
        ):
            continue

        path = os.path.join(
            KNOWLEDGE_DIR,
            filename
        )

        try:

            with open(
                path,
                "r",
                encoding="utf8"
            ) as f:

                content.append(
                    f.read()
                )

        except:

            pass

    return "\n\n".join(content)

def search_knowledge(
        question,
        top_k=3
):

    docs = []

    keywords = [
        x
        for x in question.split()
        if x
    ]

    for file in os.listdir(
        KNOWLEDGE_DIR
    ):

        if not file.endswith(".md"):
            continue

        path = os.path.join(
            KNOWLEDGE_DIR,
            file
        )

        with open(
            path,
            "r",
            encoding="utf8"
        ) as f:

            text = f.read()

        score = 0

        for k in keywords:

            if k in text:

                score += 1

        docs.append(
            (
                score,
                text
            )
        )

    docs.sort(
        key=lambda x:x[0],
        reverse=True
    )

    return "\n\n".join(
        [
            x[1]
            for x in docs[:top_k]
        ]
    )

