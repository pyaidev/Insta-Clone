from apps.common.models import Tag
from apps.posts.models import PostTag


def extract_tags(post_id, text):
    words = text.split()
    modified_text = ""

    for word in words:
        if word.startswith("#"):
            # find tags from text, create tags in database, and connect them with post
            tag_name = word.strip("#")
            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                PostTag.objects.get_or_create(
                    tag=tag, post_id=post_id
                )
                continue
        modified_text += word + ' '

    return modified_text
