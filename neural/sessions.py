import uuid


sessions: dict = {}


def create_session(auditorium_id: str, video_url: str) -> str:
    '''
    Create a new session for counting in specific auditorium.
    '''

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        'auditorium_id': auditorium_id,
        'video_url': video_url
        }

    return session_id


def get_video_url(session_id: str) -> str:
    '''
    Get video URL from session by unique session id.
    '''

    data = sessions.get(session_id)

    if not data:
        raise KeyError(f'Session {session_id} not found')

    return data['video_url']
