import asyncio

from utcp.utcp_client import UtcpClient
from utcp.data.utcp_client_config import UtcpClientConfig
from utcp_http import HttpCallTemplate


async def main():

    print("=" * 60)
    print("TEST 3 - MANUAL REGISTRATION")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Create UTCP client
    # ---------------------------------------------------------

    config = UtcpClientConfig()

    client = await UtcpClient.create(
        config=config
    )

    print("\n[1] UTCP client created")

    # ---------------------------------------------------------
    # 2. Attacker supplies a Manual
    # ---------------------------------------------------------

    attacker_manual = HttpCallTemplate(
        name="attacker_manual",
        url="http://127.0.0.1:8001",
        http_method="GET"
    )

    print("\n[2] Attacker supplies Manual")
    print("    Manual name: attacker_manual")
    print("    Manual URL : http://127.0.0.1:8001")

    # ---------------------------------------------------------
    # 3. Register Manual
    # ---------------------------------------------------------

    print("\n[3] Registering Manual...")

    registration = await client.register_manual(
        attacker_manual
    )

    print("\n[4] Registration result")
    print("    Success:", registration.success)

    # ---------------------------------------------------------
    # 4. Check registered Tools
    # ---------------------------------------------------------

    if registration.success:

        print("\n*** ATTACKER-CONTROLLED MANUAL ACCEPTED ***")

        tools = await client.search_tools(
            "",
            100,
            []
        )

        print("\nRegistered Tools:")

        for tool in tools:
            print(
                "    Tool:",
                tool.name
            )

            print(
                "    Endpoint:",
                tool.tool_call_template.url
            )

    else:

        print("\nMANUAL REGISTRATION REJECTED")

    print("\n" + "=" * 60)
    print("TEST 3 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())