#Import things that are needed generically
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent, tool
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool

from typing import Type
from youtube_search import YoutubeSearch
import json
from yt_utils import yt_get, yt_transcribe



'''
CustomYTSearchTool searches YouTube videos related to a person and returns a specified number of video URLs.
Input to this tool should be a comma separated list,
 - the first part contains a person name
 - and the second(optional) a number that is the maximum number of video results to return
'''
class CustomYTSearchTool(BaseTool):
    name = "CustomYTSearch"
    description = "search for youtube videos associated with a person. the input to this tool should be a comma separated list, the first part contains a person name and the second a number that is the maximum number of video results to return aka num_results. the second part is optional"

    def _search(self, person:str, num_results) -> str:
        results = YoutubeSearch(person,num_results).to_json()
        data = json.loads(results)
        url_suffix_list = [video['url_suffix'] for video in data['videos']]
        return url_suffix_list
    
    def _run(self, query: str) -> str:
        """Use the tool."""
        values = query.split(",")
        person = values[0]
        if len(values)>1:
            num_results = int(values[1])
        else:
            num_results=2
        return self._search(person,num_results)
    
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("YTSS  does not yet support async")

'''
CustomYTTranscribeTool transcribes YouTube videos associated with someone and
saves the transcriptions in transcriptions.json in your current directory
'''

class CustomYTTranscribeTool(BaseTool):
    name = "CustomeYTTranscribe"
    description = "transcribe youtube videos associated with someone"

    def _summarize(self, url_csv:str) -> str:
        values_list = url_csv.split(",")
        url_set = set(values_list)
        datatype = type(url_set)
        print(f"[YTTRANSCIBE***], received type {datatype} = {url_set}")

        transcriptions = {}

        for vurl in url_set:
            vpath = yt_get(vurl)

            transcription = yt_transcribe(vpath)
            transcriptions[vurl]=transcription

            print(f"transcribed {vpath} into :\n {transcription}")

        with open("transcriptions.json", "w") as json_file:
            json.dump(transcriptions, json_file)
            
        return
    
    def _run(self, query: str) -> str:
        """Use the tool."""
        return self._summarize(query)
    
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("YTSS  does not yet support async")



if __name__ == "__main__":
    llm = OpenAI(temperature=0)
    tools = []

    tools.append(CustomYTSearchTool())
    tools.append(CustomYTTranscribeTool())
    
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent.run("search youtube for Laszlo Bock's youtube videos, and return upto 3 results. list out the results for  video URLs. for each url_suffix in the search JSON output transcribe the youtube videos")
