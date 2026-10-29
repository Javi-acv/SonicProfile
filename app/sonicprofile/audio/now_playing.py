"""Windows media-session metadata reader (Spotify, browsers, and compatible players).

This module reads metadata exposed by Windows Global System Media Transport Controls.
It does not access, download, or store the playing audio.
"""
from __future__ import annotations

import asyncio
import io
import sys
from dataclasses import dataclass


@dataclass
class NowPlaying:
    title: str = ""
    artist: str = ""
    album: str = ""
    source: str = ""
    artwork: bytes | None = None
    playback_status: str = "unknown"


async def _read_thumbnail(thumbnail) -> bytes | None:
    if thumbnail is None:
        return None
    try:
        from winrt.windows.storage.streams import DataReader
        stream = await thumbnail.open_read_async()
        reader = DataReader(stream.get_input_stream_at(0))
        size = int(stream.size)
        if size <= 0 or size > 12 * 1024 * 1024:
            return None
        await reader.load_async(size)
        buffer = reader.read_buffer(size)
        try:
            data = buffer.to_bytes()
        except AttributeError:
            data = bytes(buffer)
        reader.close()
        stream.close()
        return data
    except Exception:
        return None


async def read_now_playing() -> NowPlaying | None:
    if sys.platform != "win32":
        return None
    try:
        from winrt.windows.media.control import (
            GlobalSystemMediaTransportControlsSessionManager as SessionManager
        )
        manager = await SessionManager.request_async()
        sessions = list(manager.get_sessions())
        if not sessions:
            return None

        # Prefer a session that is currently playing; otherwise use the current session.
        chosen = None
        for session in sessions:
            try:
                info = session.get_playback_info()
                status = str(info.playback_status).lower()
                if "playing" in status:
                    chosen = session
                    break
            except Exception:
                pass
        if chosen is None:
            chosen = manager.get_current_session()
        if chosen is None:
            return None

        props = await chosen.try_get_media_properties_async()
        if props is None:
            return None

        title = str(getattr(props, "title", "") or "").strip()
        artist = str(getattr(props, "artist", "") or "").strip()
        album = str(getattr(props, "album_title", "") or "").strip()
        app_id = str(getattr(chosen, "source_app_user_model_id", "") or "").strip()
        try:
            playback_status = str(chosen.get_playback_info().playback_status).split(".")[-1].lower()
        except Exception:
            playback_status = "unknown"
        artwork = await _read_thumbnail(getattr(props, "thumbnail", None))
        return NowPlaying(
            title=title,
            artist=artist,
            album=album,
            source=app_id,
            artwork=artwork,
            playback_status=playback_status,
        )
    except Exception:
        return None


async def _poll_loop(callback, stopped, interval: float = 2.0):
    last_signature = None
    while not stopped():
        item = await read_now_playing()
        if item is None:
            signature = None
        else:
            signature = (item.title, item.artist, item.album, item.source, item.playback_status, item.artwork)
        if signature != last_signature:
            callback(item)
            last_signature = signature
        await asyncio.sleep(interval)


def run_polling(callback, stopped, interval: float = 2.0):
    """Run the async Windows media poller inside a worker thread."""
    asyncio.run(_poll_loop(callback, stopped, interval))
