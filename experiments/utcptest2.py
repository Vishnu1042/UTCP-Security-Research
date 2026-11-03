import asyncio

from utcp.utcp_client import UtcpClient
from utcp.data.utcp_client_config import UtcpClientConfig
from utcp.data.auth_implementations.api_key_auth import ApiKeyAuth
from utcp_http import HttpCallTemplate


async def main():

    print("=" * 60)
    print("TEST 2 - TOOL METADATA CONTROLS ENDPOINT")
    print("=" * 60)

    # =====================================================
    # 1. Configure credential
    # =====================================================

    config = UtcpClientConfig(
        variables={
            "manual__a_API_KEY": "SECRET_A"
        }
    )

    client = await UtcpClient.create(
        config=config
    )

    print("\n[1] Credential configured")
    print("    SECRET_A")

    # =====================================================
    # 2. Register Manual A
    # =====================================================

    manual_a = HttpCallTemplate(
        name="manual-a",
        url="http://127.0.0.1:8001",
        http_method="GET",
        auth_tools=ApiKeyAuth(
            api_key="${API_KEY}",
            var_name="X-Api-Key",
            location="header"
        )
    )

    print("\n[2] Registering Manual A")
    print("    Discovery server: 127.0.0.1:8001")

    registration = await client.register_manual(
        manual_a
    )

    print("    Registration:", registration.success)

    if not registration.success:
        return

    # =====================================================
    # 3. Read Tool metadata
    # =====================================================

    print("\n[3] Reading discovered Tool")

    manual = await client.config.tool_repository.get_manual(
        "manual_a"
    )

    target_tool = None

    for tool in manual.tools:

        print("\n    Tool:", tool.name)

        print(
            "    Endpoint from metadata:",
            tool.tool_call_template.url
        )

        if tool.name == "manual_a.get_secret_data":
            target_tool = tool

    if target_tool is None:
        print("\nERROR: Tool not found")
        return

    # =====================================================
    # 4. IMPORTANT:
    #    NO endpoint modification here
    # =====================================================

    print("\n[4] Endpoint was NOT modified by the test")

    print(
        "    UTCP will use:",
        target_tool.tool_call_template.url
    )

    # =====================================================
    # 5. Execute Tool
    # =====================================================

    print("\n[5] Executing Tool")

    try:

        result = await client.call_tool(
            "manual_a.get_secret_data",
            {}
        )

        print("\nTool result:")
        print(result)

    except Exception as e:

        print("\nExecution error:")
        print(type(e).__name__)
        print(e)

        return

    print("\n" + "=" * 60)
    print("TEST 2 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())