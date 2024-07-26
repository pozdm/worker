import asyncio
from datetime import datetime, timedelta
import os
from pprint import pprint

from aiogram import Bot
import aioschedule
import jinja2
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from templates.form_template import stats_day_form


bot = Bot(token=os.getenv('BOT_TOKEN'))

url = os.getenv("URL") + "statistics/"

uris = [
    "users_stats",
    "utm_stats",
    "views_stats",
    "subscribers_stats",
    "chats_stats"
]


async def pars_stats():
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    day_before_yesterday = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")

    params = {
        "start_date": day_before_yesterday,
        "end_date": yesterday,
    }

    stats = dict()

    for uri in uris:
        response = requests.get(url + uri, params=params)
        if response.status_code != 200:
            continue

        stats[uri] = response.json()

    template = jinja2.Template(stats_day_form)
    result = template.render(
        date=yesterday,
        total_users=stats.get("users_stats", {}).get("result_for_end_day", {}).get("total_users"),
        total_users_delta=stats.get("users_stats", {}).get("delta", {}).get("total_users"),
        unique_users=stats.get("users_stats", {}).get("result_for_end_day", {}).get("users_for_day"),
        unique_users_delta=stats.get("users_stats", {}).get("delta", {}).get("users_for_day"),
        views=stats.get("users_stats", {}).get("result_for_end_day", {}).get("views_for_day"),
        views_delta=stats.get("users_stats", {}).get("delta", {}).get("views_for_day"),
        utm_stats=stats.get("utm_stats"),
        views_stats=stats.get("views_stats"),
        subscribers_tg=stats.get("subscribers_stats", {}).get("result_for_end_day", {}).get("tg"),
        subscribers_tg_delta=stats.get("subscribers_stats", {}).get("delta", {}).get("tg"),
        subscribers_vk=stats.get("subscribers_stats", {}).get("result_for_end_day", {}).get("vk"),
        subscribers_vk_delta=stats.get("subscribers_stats", {}).get("delta", {}).get("vk"),
        subscribers_total=stats.get("subscribers_stats", {}).get("result_for_end_day", {}).get("total"),
        subscribers_total_delta=stats.get("subscribers_stats", {}).get("delta", {}).get("total"),
        chats=stats.get("chats_stats", {}).get("result_for_end_day", {}).get("chats"),
        chats_delta=stats.get("chats_stats", {}).get("delta", {}).get("chats"),
        chats_users=stats.get("chats_stats", {}).get("result_for_end_day", {}).get("users"),
        chats_users_delta=stats.get("chats_stats", {}).get("delta", {}).get("users"),
        chats_messages=stats.get("chats_stats", {}).get("result_for_end_day", {}).get("messages"),
        chats_messages_delta=stats.get("chats_stats", {}).get("delta", {}).get("messages")
    )

    chat_id = -000000000
    await bot.send_message(
        chat_id=chat_id,
        text=result,
        parse_mode='HTML',
        disable_web_page_preview=True
    )


async def main():
    aioschedule.every().days.at("10:00").do(pars_stats)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
