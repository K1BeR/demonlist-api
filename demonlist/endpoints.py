from enums import *
"""
List of API Endpoints
"""

LISTS = {
    DemonListType.main: "",
    DemonListType.beyond: "beyondlist",
    DemonListType.future: "futurelist",
}

API_ENDPOINTS = {
    "sign_in": {
        "path": "api/signin/",
        "method": "post",
        "action": "signin",
    },
    "get_player_stats": {
        "path": "api/top_players/?action=get_stat&id=",
        "method": "get",
    },
    "get_country_stats": {
        "path": "api/top_countries/?action=get_stat&",
        "method": "get",
    },
    "get_level_info": {
        "path": "mainlist/",
        "method": "get",
    },
    "get_top": {
        "path": "",
        "method": "get",
    },
    "get_whitelist": {
        "path": "whitelist/",
        "method": "get",
    },
    "get_contacts": {
        "path": "contacts/",
        "method": "get",
    },
    "submit_record": {
        "path": "api/record_submit/",
        "method": "post",
    },
    "add_level_main": {
        "path": "api/level_main/",
        "method": "post",
        "action": "add",
    },
    "add_level_future": {
        "path": "api/level_future/",
        "method": "post",
        "action": "add",
    },
    "add_record": {
        "path": "api/add_record/",
        "method": "post",
        "action": "add",
    },
    "change_nick": {
        "path": "api/change_nick/",
        "method": "post",
        "action": "add",
    },
    "change_country": {
        "path": "api/users/",
        "method": "post",
        "action": "edit-country",
    },
    "change_badge": {
        "path": "api/users/",
        "method": "post",
        "action": "edit-badge",
    },
    "ban_user": {
        "path": "api/users/",
        "method": "post",
        "action": "ban",
    },
    "unban_user": {
        "path": "api/users/",
        "method": "post",
        "action": "unban",
    },
    "whitelist_user": {
        "path": "api/whitelist/",
        "method": "post",
        "action": "add",
    },
    "unwhitelist_user": {
        "path": "api/whitelist/",
        "method": "post",
        "action": "delete",
    },
    "requests": {
        "path": "api/requests/",
        "method": "post",
    },
}
