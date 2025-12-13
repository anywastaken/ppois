
from datetime import datetime
from social_network.content.ContentItem import ContentItem
from social_network.content.Comment import Comment
from social_network.content.Like import Like
from social_network.media.MediaFile import MediaFile
from social_network.content.Hashtag import Hashtag


class Post(ContentItem):
    def __init__(self, post_id: int, author_id: int, content: str):
        super().__init__(post_id, author_id)
        if not content or not content.strip():
            raise ValueError("Post content cannot be empty")

        self.content: str = content.strip()
        self.updated_at: datetime | None = None
        self.is_public: bool = True
        self.likes_count: int = 0

        self.comments: list[Comment] = []
        self.likes: list[Like] = []
        self.media_files: list[MediaFile] = []
        self.hashtags: list[Hashtag] = []

    def add_comment(self, author_id: int, text: str) -> Comment:
        comment = Comment(comment_id=len(self.comments) + 1, post_id=self.id, author_id=author_id, text=text)
        self.comments.append(comment)
        return comment

    def add_like(self, user_id: int) -> Like:
        for like in self.likes:
            if like.user_id == user_id:
                raise ValueError("User already liked this post")
        like = Like(like_id=len(self.likes) + 1, user_id=user_id, post_id=self.id)
        self.likes.append(like)
        self.likes_count = len(self.likes)
        return like

    def edit_content(self, new_content: str) -> None:
        if not new_content or not new_content.strip():
            raise ValueError("New content cannot be empty")
        self.content = new_content.strip()
        self.updated_at = datetime.now()
        self.extract_and_store_hashtags()

    def extract_and_store_hashtags(self) -> None:
        import re
        hashtags = re.findall(r"#(\w+)", self.content)
        self.hashtags = [Hashtag(tag) for tag in set(hashtags)]

    def delete(self) -> None:
        self.content = "[DELETED]"
        self.media_files.clear()
        self.comments.clear()
        self.likes.clear()
        self.likes_count = 0
        self.hashtags.clear()

    def is_liked_by(self, user_id: int) -> bool:
        return any(like.user_id == user_id for like in self.likes)

    def get_comment_count(self) -> int:
        return len(self.comments)