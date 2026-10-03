from deepagents import DeepAgentState


class PosterAgentState(DeepAgentState):
    """Extiende el state del agent con el ID del adjunto guardado en Redis."""

    attachment_id: str = None
