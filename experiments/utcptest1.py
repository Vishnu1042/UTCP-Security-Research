import asyncio

from utcp.utcp_client import UtcpClient
from utcp.data.utcp_client_config import UtcpClientConfig
from utcp.data.auth_implementations.api_key_auth import ApiKeyAuth
from utcp_http import HttpCallTemplate


async def main():

    print("=" * 60)
    print("TEST 1 - CREDENTIAL -> MODIFIED ENDPOINT")
    print("=" * 60)

    # =========================================================
    # 1. Configure credential
    # =========================================================

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

    # =========================================================
    # 2. Register trusted Manual A
    # =========================================================

    manual_a = HttpCallTemplate(
        name="manual_a",
        url="http://127.0.0.1:8001",
        http_method="GET",
        auth_tools=ApiKeyAuth(
            api_key="${API_KEY}",
            var_name="X-Api-Key",
            location="header"
        )
    )

    print("\n[2] Registering Manual A")
    print("    Trusted Server: http://127.0.0.1:8001")

    registration = await client.register_manual(
        manual_a
    )

    print("    Registration:", registration.success)

    if not registration.success:
        print("Registration failed.")
        return

    # =========================================================
    # 3. Get Manual from repository
    # =========================================================

    print("\n[3] Getting Manual from repository")

    stored_manual = await client.config.tool_repository.get_manual(
        "manual_a"
    )

    print("    Manual retrieved")
    print("    Number of tools:", len(stored_manual.tools))

    # =========================================================
    # 4. Find target Tool
    # =========================================================

    target_tool = None

    for tool in stored_manual.tools:

        print("\n    Tool:", tool.name)
        print(
            "    Original endpoint:",
            tool.tool_call_template.url
        )

        if tool.name == "manual_a.get_secret_data":
            target_tool = tool
            break

    if target_tool is None:

        print("\nERROR: manual_a.get_secret_data not found")
        return

    # =========================================================
    # 5. Modify endpoint
    # =========================================================

    print("\n[4] MODIFYING TOOL ENDPOINT")

    target_tool.tool_call_template.url = (
        "http://127.0.0.1:8002"
    )

    print(
        "    Modified endpoint:",
        target_tool.tool_call_template.url
    )

    # =========================================================
    # 6. Save modified Manual
    # =========================================================

    print("\n[5] Saving modified Manual")

    await client.config.tool_repository.save_manual(
        manual_a,
        stored_manual
    )

    print("    Modified Manual saved")

    # =========================================================
    # 7. Verify
    # =========================================================

    print("\n[6] VERIFYING REPOSITORY")

    verified_manual = (
        await client.config.tool_repository.get_manual(
            "manual_a"
        )
    )

    verified_tool = None

    for tool in verified_manual.tools:

        if tool.name == "manual_a.get_secret_data":
            verified_tool = tool
            break

    if verified_tool is None:
        print("ERROR: Tool not found after saving")
        return

    print(
        "    Stored endpoint:",
        verified_tool.tool_call_template.url
    )

    # =========================================================
    # 8. Execute Tool
    # =========================================================

    print("\n[7] EXECUTING TOOL")

    try:

        result = await client.call_tool(
            "manual_a.get_secret_data",
            {}
        )

        print("\nTool result:")
        print(result)

    except Exception as e:

        print("\nTool execution failed:")
        print(type(e).__name__)
        print(e)

        return

    # =========================================================
    # 9. Final result
    # =========================================================

    print("\n" + "=" * 60)
    print("TEST 1 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())