import schedule
import jinja2
import requests
from datetime import datetime, timedelta

from templates.form_template import stats_day_form


url = "http://127.0.0.1:8000/statistics/"

uris = [
    "users_stats",
    "utm_stats",
    "views_stats",
    "subscribers_stats",
    "chats_stats"
]


def pars_stats():
    today = datetime.now()
    last_day = today - timedelta(days=1)
    before_yesterday = last_day - timedelta(days=1)

    params = {
        # "start_date": last_day.strftime("%Y-%m-%d"),
        # "end_date": before_yesterday.strftime("%Y-%m-%d"),
        "start_date": "2024-07-20",
        "end_date": "2024-07-21",
    }

    stats = dict()

    for uri in uris:
        response = requests.get(url + uri, params=params)
        if response.status_code != 200:
            continue

        stats[uri] = response.json()

    template = jinja2.Template(stats_day_form)
    result = template.render(
        date=last_day.strftime("%Y-%m-%d"),
        total_users=stats["users_stats"]["result_for_end_day"]["total_users"],
        total_users_delta=stats["users_stats"]["delta"]["total_users"],
        unique_users=stats["users_stats"]["result_for_end_day"]["users_for_day"],
        unique_users_delta=stats["users_stats"]["delta"]["users_for_day"],
        views=stats["users_stats"]["result_for_end_day"]["views_for_day"],
        views_delta=stats["users_stats"]["delta"]["views_for_day"],
        utm_stats=stats["utm_stats"],
        views_stats=stats["views_stats"],
        subscribers_tg=stats["subscribers_stats"]["result_for_end_day"]["tg"],
        subscribers_tg_delta=stats["subscribers_stats"]["delta"]["tg"],
        subscribers_vk=stats["subscribers_stats"]["result_for_end_day"]["vk"],
        subscribers_vk_delta=stats["subscribers_stats"]["delta"]["vk"],
        subscribers_total=stats["subscribers_stats"]["result_for_end_day"]["total"],
        subscribers_total_delta=stats["subscribers_stats"]["delta"]["total"],
        chats=stats["chats_stats"]["result_for_end_day"]["chats"],
        chats_delta=stats["chats_stats"]["delta"]["chats"],
        chats_users=stats["chats_stats"]["result_for_end_day"]["users"],
        chats_users_delta=stats["chats_stats"]["delta"]["users"],
        chats_messages=stats["chats_stats"]["result_for_end_day"]["messages"],
        chats_messages_delta=stats["chats_stats"]["delta"]["messages"]
    )

    with open("stats.md", "w", encoding="UTF-8") as f:
        f.write(result)

    print("Success")


def main():
    schedule.every().days.at("10:00").do(pars_stats)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    pars_stats()
