from dataclasses import dataclass


@dataclass
class PosterAgentContext:
    linkedin_user_urn: str | None = None
