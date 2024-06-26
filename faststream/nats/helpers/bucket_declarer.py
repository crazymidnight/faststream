from typing import TYPE_CHECKING, Dict, Optional

from nats.js.api import KeyValueConfig

if TYPE_CHECKING:
    from nats.js import JetStreamContext
    from nats.js.api import Placement, RePublish, StorageType
    from nats.js.kv import KeyValue


class KVBucketDeclarer:
    buckets: Dict[str, "KeyValue"]

    def __init__(self, connection: "JetStreamContext") -> None:
        self._connection = connection
        self.buckets = {}

    async def create_key_value(
        self,
        bucket: str,
        *,
        description: Optional[str] = None,
        max_value_size: Optional[int] = None,
        history: int = 1,
        ttl: Optional[float] = None,  # in seconds
        max_bytes: Optional[int] = None,
        storage: Optional["StorageType"] = None,
        replicas: int = 1,
        placement: Optional["Placement"] = None,
        republish: Optional["RePublish"] = None,
        direct: Optional[bool] = None,
        # custom
        declare: bool = True,
    ) -> "KeyValue":
        if (key_value := self.buckets.get(bucket)) is None:
            if declare:
                key_value = await self._connection.create_key_value(
                    config=KeyValueConfig(
                        bucket=bucket,
                        description=description,
                        max_value_size=max_value_size,
                        history=history,
                        ttl=ttl,
                        max_bytes=max_bytes,
                        storage=storage,
                        replicas=replicas,
                        placement=placement,
                        republish=republish,
                        direct=direct,
                    )
                )
            else:
                key_value = await self._connection.key_value(bucket)

            self.buckets[bucket] = key_value

        return key_value
