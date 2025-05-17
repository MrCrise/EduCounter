import json
import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sessions import create_session, get_video_url
from framegen import frame_generator
from predict import model_predict


router = APIRouter()


class StartRequest(BaseModel):
    '''
    Validate counting session request data.
    '''

    auditorium_id: str
    video_url: str


class StartResponse(BaseModel):
    '''
    Validate successful session creation response.
    '''

    session_id: str


@router.post('/start', response_model=StartResponse)
async def start_counting_session(request: StartRequest):
    '''
    Create session from request and send session id as a response.
    '''
    try:
        session_id = create_session(request.auditorium_id, request.video_url)
        return {'session_id': session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def event_generator(session_id: str) -> AsyncGenerator:
    '''
    Generate people count in session's auditorium
    and return it in Server-sent events format.
    '''
    try:
        video_url = get_video_url(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail='Session not found')

    async for frame in frame_generator(video_url):
        people_count: int = await asyncio.get_running_loop().run_in_executor(
            None, model_predict, frame
        )
        count_dict = {'count': people_count}
        yield f'data: {json.dumps(count_dict)}\n\n'


@router.get('/sse/counter/{session_id}')
async def sse_count(session_id: str):
    '''
    Server-sent events realisation.
    Return streaming response to client.
    '''
    return StreamingResponse(
        event_generator(session_id),
        media_type='text/event-stream',
    )
