# Reference: https://www.youtube.com/watch?v=icUOWuDoOoE&list=PL3JVwFmb_BnQLC2agvYrJJ1cvfxED4ta_&index=5

media_item_ids = [.....]

request_body = {
    'mediaItemIds': media_item_ids
}

response = service.albums().batchAddMediaItems(
    albumId=albumId,
    body=request_body
).execute()