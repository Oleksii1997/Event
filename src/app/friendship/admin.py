from sqladmin import ModelView

from src.app.friendship.models import FriendshipRequestModel, FriendshipModel


class FriendshipRequestModelAdmin(ModelView, model=FriendshipRequestModel):
    """Реєстрація моделі заявок на дружбу в адмінпанелі"""

    name = "Friend Request"
    name_plural = "Friend Requests"
    icon = "fas fa-user-plus"
    category = "Friend"
    can_create = True
    can_edit = False
    can_delete = True
    can_view_details = True
    column_list = [
        FriendshipRequestModel.id,
        FriendshipRequestModel.receiver_id,
        FriendshipRequestModel.sender_id,
        FriendshipRequestModel.created_at,
    ]
    column_searchable_list = [
        FriendshipRequestModel.id,
        FriendshipRequestModel.receiver_id,
        FriendshipRequestModel.sender_id,
    ]
    column_sortable_list = [
        FriendshipRequestModel.created_at,
    ]
    column_labels = {
        FriendshipRequestModel.id: "ID",
        FriendshipRequestModel.receiver_id: "Receiver",
        FriendshipRequestModel.sender_id: "Sender",
        FriendshipRequestModel.created_at: "Created time",
    }


class FriendshipModelAdmin(ModelView, model=FriendshipModel):
    """Реєстрація моделі друзів в адмінпанелі"""

    name = "Friend"
    name_plural = "Friends"
    icon = "fas fa-user-friends"
    category = "Friend"
    can_create = True
    can_edit = False
    can_delete = True
    can_view_details = True
    column_list = [
        FriendshipModel.id,
        FriendshipModel.user_id,
        FriendshipModel.friend_id,
        FriendshipModel.created_at,
    ]
    column_searchable_list = [
        FriendshipModel.id,
        FriendshipModel.user_id,
        FriendshipModel.friend_id,
    ]
    column_sortable_list = [
        FriendshipModel.created_at,
    ]
    column_labels = {
        FriendshipModel.id: "ID",
        FriendshipModel.user_id: "User",
        FriendshipModel.friend_id: "Friend",
        FriendshipModel.created_at: "Created time",
    }
