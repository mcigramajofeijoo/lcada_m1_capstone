import os

from cryptography.fernet import Fernet
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from key_value.aio.wrappers.prefix_collections import PrefixCollectionsWrapper

redis_store = RedisStore()

encrypted_redis_storage = FernetEncryptionWrapper(
    key_value=RedisStore(url=os.environ["REDIS_DB_URL"]),
    fernet=Fernet(os.environ["OAUTH_STORAGE_ENCRYPTION_KEY"]),
)


def get_user_token_storage(user_id: str):
    return PrefixCollectionsWrapper(
        key_value=PrefixCollectionsWrapper(
            key_value=encrypted_redis_storage, prefix=f"lca_m1_fp_mcp_oauth:"
        ),
        prefix=f"user_{user_id}:",
    )
