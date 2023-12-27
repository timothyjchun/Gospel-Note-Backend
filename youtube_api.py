import googleapiclient.discovery
from googleapiclient.errors import HttpError

api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyCz4BHuuj6UOythnQaQIYzaHV7LMg7TRBU"


# Define a function to fetch the video links from a YouTube channel
def get_video_links(channel_username):
    try:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key
        )

        channel_response = (
            youtube.channels()
            .list(
                part="contentDetails",
                forUsername=channel_username,
            )
            .execute()
        )

        print(channel_response)

    except HttpError as e:
        print(f"An HTTP error occurred: {e}")


# Usage example
channel_username = "user-jg1rl7zp6b"
get_video_links(channel_username)
