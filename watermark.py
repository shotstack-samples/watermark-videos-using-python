import shotstack_sdk as shotstack
import os
import sys

from shotstack_sdk.api import edit_api
from shotstack_sdk.model.clip import Clip
from shotstack_sdk.model.track import Track
from shotstack_sdk.model.timeline import Timeline
from shotstack_sdk.model.output import Output
from shotstack_sdk.model.edit import Edit
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.image_asset import ImageAsset

if __name__ == "__main__":
    host = "https://api.shotstack.io/stage"

    configuration = shotstack.Configuration(host = host)

    configuration.api_key['DeveloperKey'] = os.getenv("SHOTSTACK_KEY")
    
    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        video_asset = VideoAsset(
        src = "https://d1uej6xx5jo4cd.cloudfront.net/sydney.mp4"
        )
        
        video_clip = Clip(
            asset = video_asset,
            start = 0.0,
            length= 10.0
        )
        
        image_asset = ImageAsset(
        src = "https://shotstack-assets.s3-ap-southeast-2.amazonaws.com/logos/real-estate-black.png"
        )
        
        image_clip = Clip(
            asset = image_asset,
            start = 0.0,
            length= 10.0,
            scale = 0.30,
            fit = 'crop',
            position = 'center',
            opacity = 0.2
        )
        
        track_1 = Track(clips=[image_clip])
        track_2 = Track(clips=[video_clip])

        timeline = Timeline(
            background = "#000000",
            tracks     = [track_1, track_2]
        )

        output = Output(
            format      = "mp4",
            resolution  = "hd"
        )

        edit = Edit(
            timeline = timeline,
            output   = output
        )

        try:
            api_response = api_instance.post_render(edit)

            message = api_response['response']['message']
            id = api_response['response']['id']
        
            print(f"{message}\n")
            print(f">> render id: {id}")
        except Exception as e:
            print(f"Unable to resolve API call: {e}")
