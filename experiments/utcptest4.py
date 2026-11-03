import asyncio

from utcp.utcp_client import UtcpClient
from utcp.data.utcp_client_config import UtcpClientConfig
from utcp_http import HttpCallTemplate


async def main():

    print("=" * 60)
    print("TEST 4 - UNTRUSTED USER -> MANUAL REGISTRATION")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Create UTCP client
    # ---------------------------------------------------------

    client = await UtcpClient.create(
        config=UtcpClientConfig()
    )

    print("\n[1] UTCP client created")

    # ---------------------------------------------------------
    # 2. Simulate untrusted user input
    # ---------------------------------------------------------

    untrusted_manual_url = "http://127.0.0.1:8001"

    print("\n[2] UNTRUSTED USER SUPPLIES:")
    print("    Manual URL:", untrusted_manual_url)

    # ---------------------------------------------------------
    # 3. Convert user input directly into Manual
    # ---------------------------------------------------------

    manual = HttpCallTemplate(
        name="untrusted_manual",
        url=untrusted_manual_url,
        http_method="GET"
    )

    print("\n[3] Passing user-supplied Manual to UTCP")
    print("    Calling register_manual()")

    # ---------------------------------------------------------
    # 4. Register Manual
    # ---------------------------------------------------------

    registration = await client.register_manual(
        manual
    )

    print("\n[4] UTCP registration result")
    print("    Success:", registration.success)

    if not registration.success:

        print("\nMANUAL REGISTRATION REJECTED")
        return

    # ---------------------------------------------------------
    # 5. Check registered Tools
    # ---------------------------------------------------------

    print("\n[5] Registered Tools")

    tools = await client.search_tools(
        "",
        100,
        []
    )

    for tool in tools:

        print("    Tool:", tool.name)
        print(
            "    Endpoint:",
            tool.tool_call_template.url
        )

    print("\n" + "=" * 60)
    print("TEST 4 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())