import os

from fastmcp.client.auth.oauth import OAuth
from mcp.shared.auth import OAuthMetadata

from m1_final_project.mcps.token_storage import get_user_token_storage


class XOAuth(OAuth):
    """
    X no publica discovery (ni PRM ni authorization-server-metadata) para
    api.x.com/mcp — confirmado en docs.x.com/tools/mcp. El fallback del SDK
    sin discovery arma endpoints incorrectos (https://api.x.com/authorize),
    así que forzamos los reales antes de autorizar.
    """

    def __init__(self, *args, asked_scope: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._asked_scope = asked_scope

    async def _perform_authorization_code_grant(self):
        self.context.client_metadata.scope = self._asked_scope
        return await super()._perform_authorization_code_grant()

    async def _perform_authorization(self):
        self.context.oauth_metadata = OAuthMetadata(
            issuer="https://x.com",
            authorization_endpoint="https://x.com/i/oauth2/authorize",
            token_endpoint="https://api.x.com/2/oauth2/token",
        )
        return await super()._perform_authorization()


def x_auth(user_id: str):
    return XOAuth(
        client_id=os.environ["X_CLIENT_ID"],
        client_secret=os.environ["X_CLIENT_SECRET"],
        # Agregamos `offline.access` a los scopes — sin eso no hay refresh_token, y tu usuario tendría que re-loguearse cada vez que expire el access token.
        # Scopes obtained from: https://mcpservers.org/servers/DataWhisker/x-mcp-server
        scopes=["tweet.read", "tweet.write", "media.write", "offline.access"],
        asked_scope="tweet.read tweet.write media.write offline.access",
        token_storage=get_user_token_storage(user_id),
        callback_port=8774,
        additional_client_metadata={
            "token_endpoint_auth_method": "client_secret_basic"
        },
        # En el exchange del code por el access_token, el default del SDK es
        # client_secret_post: client_id y client_secret viajan en el body del POST.
        # Con client_secret_basic, viajan en el header Authorization: Basic
        # base64(client_id:client_secret). X exige client_secret_basic para
        # confidential clients — rechaza client_secret_post con 401
        # "Missing valid authorization header".
    )
