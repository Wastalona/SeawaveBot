from aiogram.types import User, Chat


TEST_ADMIN = User(
    id=974268069,
    is_bot=False,
    first_name="ADMIN",
    last_name=None,
    username=None,
    language_code=None,
    is_premium=None,
    added_to_attachment_menu=None,
    can_join_groups=None,
    can_read_all_group_messages=None,
    supports_inline_queries=None,
    can_connect_to_business=None,
    has_main_web_app=None
)

TEST_EMP = User(
    id=7477986473,
    is_bot=False,
    first_name="EMPLOYEE",
    last_name=None,
    username=None,
    language_code=None,
    is_premium=None,
    added_to_attachment_menu=None,
    can_join_groups=None,
    can_read_all_group_messages=None,
    supports_inline_queries=None,
    can_connect_to_business=None,
    has_main_web_app=None
)

TEST_USER = User(
    id=1,
    is_bot=False,
    first_name="USER",
    last_name=None,
    username=None,
    language_code=None,
    is_premium=None,
    added_to_attachment_menu=None,
    can_join_groups=None,
    can_read_all_group_messages=None,
    supports_inline_queries=None,
    can_connect_to_business=None,
    has_main_web_app=None
)


TEST_CHAT = Chat(
    id=2,
    type="private",
    title=None, 
    username=None, 
    first_name=None, 
    last_name=None, 
    is_forum=None, 
    accent_color_id=None, 
    active_usernames=None, 
    available_reactions=None, 
    background_custom_emoji_id=None, 
    bio=None, 
    birthdate=None, 
    business_intro=None, 
    business_location=None, 
    business_opening_hours=None, 
    can_set_sticker_set=None, 
    custom_emoji_sticker_set_name=None, 
    description=None, 
    emoji_status_custom_emoji_id=None, 
    emoji_status_expiration_date=None, 
    has_aggressive_anti_spam_enabled=None, 
    has_hidden_members=None, 
    has_private_forwards=None, 
    has_protected_content=None, 
    has_restricted_voice_and_video_messages=None, 
    has_visible_history=None, 
    invite_link=None, 
    join_by_request=None, 
    join_to_send_messages=None, 
    linked_chat_id=None, 
    location=None, 
    message_auto_delete_time=None, 
    permissions=None, 
    personal_chat=None, 
    photo=None, 
    pinned_message=None, 
    profile_accent_color_id=None,
     profile_background_custom_emoji_id=None, 
     slow_mode_delay=None, 
     sticker_set_name=None, 
     unrestrict_boost_count=None
)