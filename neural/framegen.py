import cv2
import asyncio
from typing import AsyncGenerator


async def frame_generator(video_url: str) -> AsyncGenerator:
    '''
    Generate frames asynchronously from a video stream URL using OpenCV.

    TODO: Implement queue checking for frame capture.
          (FIFO queue realisation would be good)

          Current realisation have a problem that
          if frames will generate faster than model
          can handle them, they will stack in queue
          and service will start sending outdated info.
    '''

    loop = asyncio.get_running_loop()
    capture = await loop.run_in_executor(None, cv2.VideoCapture, video_url)

    try:
        while True:
            retval, frame = await loop.run_in_executor(None, capture.read)
            if not retval:
                break
            yield frame
            await asyncio.sleep(0.5)  # Avoiding tight loop.
    finally:
        await loop.run_in_executor(None, capture.release)
