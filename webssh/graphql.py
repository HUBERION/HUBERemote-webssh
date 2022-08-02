import os
from typing import Tuple

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from dotenv import load_dotenv

load_dotenv()

transport = AIOHTTPTransport(
    url=os.getenv("API_ENDPOINT"),
    headers={"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}
)

async def get_host_and_port_from_api(sessionId: str) -> Tuple[str, int]:
    async with Client(
        transport=transport, 
        fetch_schema_from_transport=False
    ) as session:
        query: str = f"""
            query {{
                sessions(
                    filters: {{
                        sessionId: {{ eq: "{sessionId}" }}
                    }}
                ){{
                    data {{
                        attributes {{
                            supporterPort
                            clientHost
                        }}
                    }}
                }}
            }}
        """
        result = await session.execute(gql(query))

        return (
            result["sessions"]["data"][0]["attributes"]["clientHost"],
            result["sessions"]["data"][0]["attributes"]["supporterPort"]
        )
