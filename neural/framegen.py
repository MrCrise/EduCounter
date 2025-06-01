import cv2
import asyncio
from typing import AsyncGenerator


async def frame_generator(video_url: str, max_queue: int = 2) -> AsyncGenerator:
    '''
    Generate frames asynchronously from a video stream URL using OpenCV.
    '''

    loop = asyncio.get_running_loop()
    capture = await loop.run_in_executor(None, cv2.VideoCapture, video_url)
    queue = asyncio.Queue(maxsize=max_queue)

    async def frame_reader():
        while True:
            retval, frame = await loop.run_in_executor(None, capture.read)
            if not retval:
                break

            if queue.full():
                try:
                    _ = queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass

            await queue.put(frame)

            await asyncio.sleep(0.03)

        await loop.run_in_executor(None, capture.release)

    frame_reader_task = asyncio.create_task(frame_reader())

    try:
        while True:
            if frame_reader_task.done() and queue.empty():
                break

            frame = await queue.get()
            yield frame

            await asyncio.sleep(0)
    finally:
        if not frame_reader_task.done():
            frame_reader_task.cancel()

            try:
                await frame_reader_task
            except asyncio.CancelledError:
                pass
