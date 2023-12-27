from aiohttp import ClientSession, TCPConnector
import asyncio
from dataclasses import dataclass
from bs4 import BeautifulSoup
import json
import pprint
from collections import deque
from typing import Union, List


@dataclass
class URL:
    url: str


class Client:
    url: URL = "https://www.youtube.com/@user-jg1rl7zp6b/videos"

    def __init__(self):
        # self.session = ClientSession()
        self.session = ClientSession(connector=TCPConnector(ssl=False))
        self.NewGospelNotes: Union[deque, List[dict]] = deque([])
        self.GospelNotes: list = []

    def process_title_data(self, full_title, v_url):
        if "천세종" not in full_title:
            title_index = full_title.find("일") + 1
        else:
            title_index = full_title.find("복음노트") + 4
        general_title = full_title[:title_index]
        specific_title = full_title[title_index:]
        if len(specific_title) > 2:
            # maybe recursion?
            passage_index = specific_title.find(
                "장", 3
            )  # Cuz '시편'이 있으면 1까지는 걸러야 하고, 공백 생각하면 2까지 걸러야함.
            if specific_title[passage_index - 1].isnumeric():
                # ok
                passage = specific_title[: passage_index + 1]
                specific_title = specific_title[passage_index + 1 :]
            else:
                # ok
                passage_index = specific_title.find("편", 3)
                if specific_title[passage_index - 1].isnumeric():
                    passage = specific_title[: passage_index + 1]
                    specific_title = specific_title[passage_index + 1 :]
                else:
                    # nothing
                    passage = ""
        indi_note = {
            "url": v_url,
            "general_title": general_title,
            "passage": passage if passage else "",
            "specific_title": specific_title,
        }
        self.NewGospelNotes.appendleft(indi_note)
        return

    async def get_recent_video_data(self) -> list:
        async with self.session.get(self.url) as res:
            data: str = await res.text()
            string_data: str = data.split("ytInitialData = ")[1].split(";</script>")[0]
            dict_data: dict = json.loads(string_data)
            video_list: list = dict_data["contents"]["twoColumnBrowseResultsRenderer"][
                "tabs"
            ][1]["tabRenderer"]["content"]["richGridRenderer"]["contents"]
            return video_list

    def add_recent_gospel_notes(self):
        with open("gospel_notes.txt", "r+", encoding="UTF-8") as f:
            self.GospelNotes: list = json.loads(f.read())
            GospelNotesToAdd: list = []
            for i in range(-1, -len(self.NewGospelNotes) - 1, -1):
                if self.NewGospelNotes[i] in self.GospelNotes:  # 이미 있는 영상이 나올때 까지 검색하기
                    GospelNotesToAdd: list = self.NewGospelNotes[
                        i + 1 :
                    ]  # 없는 영상들 원본 데이터에 담기
                    break
                else:
                    continue
            self.GospelNotes += GospelNotesToAdd
            f.seek(0)
            f.write(json.dumps(self.GospelNotes))

    async def create_recent_gospel_notes(self):
        video_list = await self.get_recent_video_data()
        for i in range(len(video_list) - 1):  # last item is not a video item
            video_specific_data = video_list[i]["richItemRenderer"]["content"][
                "videoRenderer"
            ]
            title_data = video_specific_data["title"]
            url_data = video_specific_data["navigationEndpoint"]["commandMetadata"][
                "webCommandMetadata"
            ]["url"]
            video_url: str = url_data.split("/watch?v=")[1]

            full_title = title_data["runs"][0]["text"]
            self.process_title_data(full_title, video_url)
        self.NewGospelNotes = list(self.NewGospelNotes)
        self.add_recent_gospel_notes()
        return "Success"


async def main():
    client = Client()
    res = await client.create_recent_gospel_notes()
    if res == "Success":
        print("Success")
    else:
        print("Failed")
    await client.session.close()


if __name__ == "__main__":
    asyncio.run(main())
