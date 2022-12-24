from pyfcm import FCMNotification


def send_notify(reg_id, message_title, message_body):

    api_key = "AAAA_IMvqgI:APA91bEuATTnof0pEAKV5Il1UbrR5BKRph-O1gVChEXeA0Sa_rvkPZMStFpXqj6UBHXkHBpEfhAyHtErWOp67PPgFbaVxhMB7wKRUzaAiyiFDdLb5zv2hY1DtJA8Ykmu1nagyqfITbZy"

    push_service = FCMNotification(
        api_key=api_key)

    push_service.notify_single_device(
        registration_id=reg_id, message_title=message_title, message_body=message_body,  time_to_live=3600, sound=True)


# def send_topic(topic_condition, message):

#     api_key = "AAAAkHp6ON8:APA91bHBAv-LJ-Kyvio8lqdKhVJ9vkKlijFjRIaXvtuaYWkOaji1U1ihrCY4davotBp7GBidyRVza1idWLZs4TW6m5sc5wm-nVGFwCiAJIMnceMNa8ADuSdut3CDosdW30hI8-3FZ9oK"

#     push_service = FCMNotification(
#         api_key=api_key)

#     res = push_service.notify_topic_subscribers(
#         message_body=message, topic_name=topic_condition, sound=True)


send_notify('dEXfqlfQTtGtxD86ZFGdi5:APA91bE0eaXQ4ylsv63HlVBZZYKebL29WwQD83deh1qJKo2PbyBcgNdjzlhaIJneZnreOlPpbtmtw6BgFSnYu8fMsTch5Ccsb2uG7t2r-nYH-tpXvbN9Bog_EgOuLpG9ZoBD3KOBI7dB', 'test', 'test')
