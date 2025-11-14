thonpython
import logging
from .utils_time import convert_timestamp

def parse_reddit_post(json_data, original_url: str):
    """
    Parses Reddit post JSON (two-list structure).
    """
    results = []

    try:
        post_info = json_data[0]["data"]["children"][0]["data"]

        post_entry = {
            "contentType": "post",
            "createdAt": convert_timestamp(post_info.get("created_utc")),
            "id": post_info.get("name"),
            "parseId": post_info.get("id"),
            "subreddit": post_info.get("subreddit"),
            "communityName": f"r/{post_info.get('subreddit')}",
            "authorId": post_info.get("author_fullname"),
            "author": post_info.get("author"),
            "title": post_info.get("title"),
            "body": post_info.get("selftext"),
            "upvotes": post_info.get("ups"),
            "noOfcomments": post_info.get("num_comments"),
            "communityMembers": post_info.get("subreddit_subscribers"),
            "url": original_url,
            "thumbnailUrl": post_info.get("thumbnail"),
            "videoUrl": post_info.get("media", {}).get("reddit_video", {}).get("fallback_url")
            if post_info.get("media")
            else None,
            "isVideo": post_info.get("is_video"),
            "isAd": post_info.get("is_created_from_ads_ui"),
            "isPinned": post_info.get("pinned"),
            "isOver18": post_info.get("over_18"),
        }

        results.append(post_entry)

        # Comments section
        comments_raw = json_data[1]["data"]["children"]
        for item in comments_raw:
            if item["kind"] != "t1":
                continue
            c = item["data"]
            comment_entry = {
                "contentType": "comment",
                "createdAt": convert_timestamp(c.get("created_utc")),
                "id": c.get("name"),
                "parseId": c.get("id"),
                "parentId": c.get("parent_id"),
                "postId": c.get("link_id"),
                "subreddit": c.get("subreddit"),
                "communityName": f"r/{c.get('subreddit')}",
                "authorId": c.get("author_fullname"),
                "author": c.get("author"),
                "body": c.get("body"),
                "upvotes": c.get("ups"),
                "noOfreplies": c.get("replies", {}).get("data", {}).get("children", []).__len__()
                if isinstance(c.get("replies"), dict)
                else 0,
                "url": f"{original_url}/{c.get('id')}/",
            }
            results.append(comment_entry)

    except Exception as e:
        logging.error(f"Error while parsing Reddit JSON: {e}")

    return results