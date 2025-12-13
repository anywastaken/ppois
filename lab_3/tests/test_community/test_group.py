import pytest
from social_network.community.Group import Group
from social_network.exceptions.InsufficientPermissionsException import InsufficientPermissionsException
from social_network.exceptions.UserNotFoundException import UserNotFoundException


@pytest.fixture
def group():
    return Group(group_id=10, name="Dev Team", description="Developers only", owner_id=50)


def test_group_initialization(group):
    assert group.id == 10
    assert group.owner_id == 50
    assert group.name == "Dev Team"
    assert 50 in group._members
    assert 50 in group._admins


def test_group_invalid_name():
    with pytest.raises(ValueError, match="Group name cannot be empty"):
        Group(group_id=1, name="   ", description="x", owner_id=1)


def test_join_success(group):
    group.join(user_id=60)
    assert 60 in group._members


def test_join_duplicate_fails(group):
    group.join(60)
    with pytest.raises(ValueError, match="User is already a member"):
        group.join(60)


def test_join_invalid_id(group):
    with pytest.raises(ValueError, match="User ID must be positive"):
        group.join(-1)


def test_create_post_by_member_success(group):
    group.join(60)
    post = group.create_post(author_id=60, content="Hello group!")
    assert post.content == "Hello group!"


def test_create_post_by_non_member_fails(group):
    with pytest.raises(InsufficientPermissionsException, match="User is not a member"):
        group.create_post(author_id=999, content="Spam")


def test_add_admin_success(group):
    group.join(60)
    group.add_admin(issuer_id=50, new_admin_id=60)
    assert 60 in group._admins


def test_add_admin_non_member_fails(group):
    with pytest.raises(UserNotFoundException, match="User is not a member"):
        group.add_admin(50, 999)


def test_remove_member_by_admin_success(group):
    group.join(60)
    group.remove_member(moderator_id=50, user_id=60)
    assert 60 not in group._members


def test_owner_cannot_leave(group):
    with pytest.raises(ValueError, match="Owner cannot leave the group"):
        group.leave(50)


def test_leave_non_member_fails(group):
    with pytest.raises(UserNotFoundException, match="User is not a member"):
        group.leave(999)


def test_delete_post_success(group):
    group.join(60)
    post = group.create_post(60, "To delete")
    deleted = group.delete_post(moderator_id=50, post_id=post.id)
    assert deleted is True


def test_get_feed_private_denied(group):
    group.is_private = True
    with pytest.raises(InsufficientPermissionsException, match="This group is private"):
        group.get_feed(viewer_id=999)