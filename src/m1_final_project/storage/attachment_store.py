import os
import uuid

from redis.asyncio import Redis


# NOTE: We're using redis.asyncio.Redis, so every Redis operation that performs I/O must be awaited.
class AttachmentStore:
    def __init__(self):
        # decode_responses queda en False (default) a propósito: los bytes de la
        # imagen no se pueden decodificar como texto y romperían el get
        self._redis = Redis.from_url(url=os.environ["REDIS_DB_URL"])
        self._ttl_seconds = 3600
        self._key_prefix = "lcada:m1_fp:attachments"

    def _get_key(self, attachment_id: str) -> str:
        return f"{self._key_prefix}:{attachment_id}"

    async def set(self, file_bytes: bytes, filename: str, mimetype: str) -> str:
        """Guarda el archivo y devuelve el attachment_id (la key aleatoria)."""
        attachment_id = f"att_{uuid.uuid4().hex}"

        key = self._get_key(attachment_id)

        # `hset` guarda cada campo por separado: los bytes van tal cual, sin base64 ni JSON
        await self._redis.hset(
            name=key,
            mapping={
                "file_bytes": file_bytes,
                "filename": filename,
                "mimetype": mimetype,
            },
        )

        await self._redis.expire(key, self._ttl_seconds)

        return attachment_id

    async def get(self, attachment_id: str) -> dict[str, str | bytes]:
        """Devuelve {"file_name", "mimetype", "data"}, o None si no existe o expiró."""

        # `hgetall` obtains all fields from the mapping, `hget` gets only ONE.
        data = await self._redis.hgetall(name=self._get_key(attachment_id))

        if not data:
            raise KeyError(f'Attachment "{attachment_id}" not found or expired.')

        # NOTE:
        # - Redis stores both keys and values as raw bytes, not strings. Therefore, lookups like data['filename'] will fail because Redis expects the byte representation (b'filename') rather than the string itself.
        # - If a field is already in bytes format, the Redis client skips encoding and passes the raw binary data directly.
        return {
            "file_bytes": data[
                b"file_bytes"
            ],  # Key is the byte representation of the str "file_bytes"
            "filename": data[
                b"filename"
            ].decode(),  # Manually decoded because `decode_responses` is disabled (which is correct in this case). Enabling it would cause Redis to incorrectly attempt decoding on raw file bytes (`file_bytes` field).
            "mimetype": data[b"mimetype"].decode(),
        }


attachment_store = AttachmentStore()
