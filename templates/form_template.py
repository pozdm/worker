stats_day_form = """
<strong>Ежедневная статистика по аудитории ЯЗЖ за {{ date }}:</strong>  
<strong>Всего пользователей(с декабря 2022): {{ total_users }} ({{ "{:+}".format(total_users_delta) }})</strong>

<strong>Пользователей: {{ unique_users }} ({{ "{:+}".format(unique_users_delta) }})</strong>  
<strong>Просмотров: {{ views }} ({{ "{:+}".format(views_delta) }})</strong>

<strong>UTM term:</strong>
{% for key, value in utm_stats.result_for_end_day.items() -%}
{{ loop.index0 + 1 }}. {{ key }}: {{ value }} ({{ "{:+}".format(utm_stats.delta[key]) }})
{% endfor %}
<strong>Просмотры по сервисам:</strong>
{% for key, value in views_stats.result_for_end_day.items() -%}
{{ loop.index0 + 1 }}. {{ key }}: {{ value }} ({{ "{:+}".format(views_stats.delta[key]) }})
{% endfor %}
<strong>Подписки на уведомления: </strong>  
Telegram: {{ subscribers_tg }} ({{ "{:+}".format(subscribers_tg_delta) }})  
VK: {{ subscribers_vk }} ({{ "{:+}".format(subscribers_vk_delta) }})  
Всего (уникальных): {{ subscribers_total }} ({{ "{:+}".format(subscribers_total_delta) }})

<strong>Домовые чаты (пилот):</strong>  
Всего чатов: {{ chats }} ({{ "{:+}".format(chats_delta) }})  
Всего участников: {{ chats_users }} ({{ "{:+}".format(chats_users_delta) }})  
Всего сообщений: {{ chats_messages }} ({{ "{:+}".format(chats_messages_delta) }})
"""