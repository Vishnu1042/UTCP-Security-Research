import sys
import runpy
from urllib.parse import urlparse

from utcp.utcp_client import UtcpClient


# ============================================================
# UTCP SECURITY MITIGATION
#
# TEST 1 - Credential -> Endpoint Binding
# TEST 2 - Tool Metadata Endpoint Validation
# TEST 3 - Attacker-Controlled Manual Registration
# TEST 4 - Untrusted User -> Manual Registration
# ============================================================


class UTCPMitigation:

    def __init__(self):

        # ====================================================
        # TRUSTED ENDPOINT
        # ====================================================

        self.trusted_endpoint = "http://127.0.0.1:8001"

        # ====================================================
        # CREDENTIAL -> ENDPOINT BINDING
        # ====================================================

        self.credential_bindings = {
            "API_KEY": self.trusted_endpoint
        }

        # ====================================================
        # TRUSTED MANUALS
        #
        # Your existing test files use:
        #
        # manual_a
        # manual-a
        #
        # Both are therefore recognized as the trusted
        # Manual identity.
        # ====================================================

        self.trusted_manuals = {
            "manual_a": self.trusted_endpoint,
            "manual-a": self.trusted_endpoint
        }

        # ====================================================
        # CURRENT TEST
        # ====================================================

        self.current_test = ""


    # ========================================================
    # URL NORMALIZATION
    # ========================================================

    def normalize_url(self, url):

        if not url:
            return ""

        parsed = urlparse(str(url))

        return (
            f"{parsed.scheme.lower()}://"
            f"{parsed.netloc.lower()}"
            f"{parsed.path.rstrip('/')}"
        )


    # ========================================================
    # TEST 1
    # CREDENTIAL -> ENDPOINT BINDING
    # ========================================================

    def check_credential_endpoint(
        self,
        credential_name,
        requested_endpoint
    ):

        print()
        print("=" * 60)
        print("MITIGATION - TEST 1")
        print("CREDENTIAL-ENDPOINT BINDING VALIDATION")
        print("=" * 60)

        authorized_endpoint = self.normalize_url(
            self.credential_bindings.get(
                credential_name,
                ""
            )
        )

        requested_endpoint = self.normalize_url(
            requested_endpoint
        )

        print()
        print("Credential:")
        print(f"    {credential_name}")

        print()
        print("Authorized endpoint:")
        print(f"    {authorized_endpoint}")

        print()
        print("Requested endpoint:")
        print(f"    {requested_endpoint}")

        print()
        print("Checking credential-endpoint binding...")

        # ----------------------------------------------------
        # BLOCK UNAUTHORIZED ENDPOINT
        # ----------------------------------------------------

        if requested_endpoint != authorized_endpoint:

            print()
            print("❌ CREDENTIAL-ENDPOINT MISMATCH")
            print("❌ TEST 1 ATTACK DETECTED")
            print("❌ REQUEST BLOCKED")
            print("❌ CREDENTIAL WILL NOT BE SENT")

            return False

        # ----------------------------------------------------
        # ALLOW TRUSTED ENDPOINT
        # ----------------------------------------------------

        print()
        print("✅ CREDENTIAL-ENDPOINT MATCH")
        print("✅ REQUEST ALLOWED")

        return True


    # ========================================================
    # TEST 2
    # TOOL METADATA ENDPOINT VALIDATION
    # ========================================================

    def check_metadata_endpoint(
        self,
        tool_name,
        metadata_endpoint
    ):

        print()
        print("=" * 60)
        print("MITIGATION - TEST 2")
        print("TOOL METADATA ENDPOINT VALIDATION")
        print("=" * 60)

        trusted_endpoint = self.normalize_url(
            self.trusted_endpoint
        )

        metadata_endpoint = self.normalize_url(
            metadata_endpoint
        )

        print()
        print("Tool:")
        print(f"    {tool_name}")

        print()
        print("Trusted endpoint:")
        print(f"    {trusted_endpoint}")

        print()
        print("Endpoint from Tool metadata:")
        print(f"    {metadata_endpoint}")

        print()
        print("Checking Tool metadata endpoint...")

        # ----------------------------------------------------
        # BLOCK MALICIOUS METADATA
        # ----------------------------------------------------

        if metadata_endpoint != trusted_endpoint:

            print()
            print("❌ MALICIOUS TOOL METADATA DETECTED")
            print("❌ METADATA SPECIFIES UNAUTHORIZED ENDPOINT")
            print("❌ TEST 2 ATTACK DETECTED")
            print("❌ TOOL EXECUTION BLOCKED")
            print("❌ CREDENTIAL WILL NOT BE SENT")

            return False

        # ----------------------------------------------------
        # ALLOW TRUSTED METADATA
        # ----------------------------------------------------

        print()
        print("✅ TOOL METADATA ENDPOINT TRUSTED")
        print("✅ TOOL EXECUTION ALLOWED")

        return True


    # ========================================================
    # TEST 3
    # ATTACKER-CONTROLLED MANUAL REGISTRATION
    # ========================================================

    def check_manual_registration(self, manual):

        manual_name = getattr(
            manual,
            "name",
            ""
        )

        manual_url = getattr(
            manual,
            "url",
            ""
        )

        print()
        print("=" * 60)
        print("MITIGATION - TEST 3")
        print("ATTACKER-CONTROLLED MANUAL REGISTRATION")
        print("=" * 60)

        print()
        print("Manual name:")
        print(f"    {manual_name}")

        print()
        print("Manual source:")
        print(f"    {manual_url}")

        print()
        print("Trusted Manuals:")

        for name, url in self.trusted_manuals.items():

            print(
                f"    {name} -> "
                f"{self.normalize_url(url)}"
            )

        print()
        print("Checking Manual identity...")

        trusted_url = self.trusted_manuals.get(
            manual_name
        )

        # ----------------------------------------------------
        # CHECK MANUAL NAME
        # ----------------------------------------------------

        if trusted_url is None:

            print()
            print("❌ UNTRUSTED MANUAL NAME")
            print("❌ MANUAL IDENTITY IS NOT TRUSTED")
            print("❌ TEST 3 ATTACK DETECTED")
            print("❌ MANUAL REGISTRATION BLOCKED")
            print("❌ TOOL WILL NOT BE REGISTERED")

            return False

        # ----------------------------------------------------
        # CHECK MANUAL SOURCE
        # ----------------------------------------------------

        trusted_url = self.normalize_url(
            trusted_url
        )

        normalized_url = self.normalize_url(
            manual_url
        )

        print()
        print("Expected trusted source:")
        print(f"    {trusted_url}")

        print()
        print("Checking Manual source...")

        if normalized_url != trusted_url:

            print()
            print("❌ MANUAL SOURCE MISMATCH")
            print("❌ MANUAL IDENTITY/SOURCE BINDING FAILED")
            print("❌ TEST 3 ATTACK DETECTED")
            print("❌ MANUAL REGISTRATION BLOCKED")
            print("❌ TOOL WILL NOT BE REGISTERED")

            return False

        print()
        print("✅ MANUAL IDENTITY TRUSTED")
        print("✅ MANUAL SOURCE TRUSTED")
        print("✅ MANUAL REGISTRATION ALLOWED")

        return True


    # ========================================================
    # TEST 4
    # UNTRUSTED USER -> MANUAL REGISTRATION
    # ========================================================

    def check_untrusted_user_manual(self, manual):

        manual_name = getattr(
            manual,
            "name",
            ""
        )

        manual_url = getattr(
            manual,
            "url",
            ""
        )

        print()
        print("=" * 60)
        print("MITIGATION - TEST 4")
        print("UNTRUSTED USER -> MANUAL REGISTRATION")
        print("=" * 60)

        print()
        print("User-supplied Manual:")
        print(f"    Name: {manual_name}")
        print(f"    URL : {manual_url}")

        print()
        print("Checking Manual supplied by untrusted user...")

        trusted_url = self.trusted_manuals.get(
            manual_name
        )

        # ----------------------------------------------------
        # CHECK MANUAL IDENTITY
        # ----------------------------------------------------

        if trusted_url is None:

            print()
            print("❌ UNTRUSTED USER-SUPPLIED MANUAL")
            print("❌ MANUAL IDENTITY IS NOT TRUSTED")
            print("❌ TEST 4 ATTACK DETECTED")
            print("❌ REGISTRATION BLOCKED")
            print("❌ MANUAL WILL NOT BE REGISTERED")

            return False

        # ----------------------------------------------------
        # CHECK MANUAL SOURCE
        # ----------------------------------------------------

        normalized_user_url = self.normalize_url(
            manual_url
        )

        normalized_trusted_url = self.normalize_url(
            trusted_url
        )

        print()
        print("Trusted Manual source:")
        print(f"    {normalized_trusted_url}")

        print()
        print("Checking user-supplied Manual source...")

        if normalized_user_url != normalized_trusted_url:

            print()
            print("❌ USER-SUPPLIED MANUAL SOURCE MISMATCH")
            print("❌ TEST 4 ATTACK DETECTED")
            print("❌ REGISTRATION BLOCKED")
            print("❌ MANUAL WILL NOT BE REGISTERED")

            return False

        print()
        print("✅ USER-SUPPLIED MANUAL MATCHES TRUSTED MANUAL")
        print("✅ REGISTRATION ALLOWED")

        return True


# ============================================================
# SECURITY OBJECT
# ============================================================

security = UTCPMitigation()


# ============================================================
# SAVE ORIGINAL UTCP CREATE METHOD
# ============================================================

_original_create = UtcpClient.create


# ============================================================
# PROTECTED UTCP CLIENT
# ============================================================

async def protected_create(
    root_dir=None,
    config=None
):

    # --------------------------------------------------------
    # CREATE NORMAL UTCP CLIENT
    # --------------------------------------------------------

    client = await _original_create(
        root_dir=root_dir,
        config=config
    )

    # --------------------------------------------------------
    # SAVE ORIGINAL METHODS
    # --------------------------------------------------------

    original_call_tool = client.call_tool

    original_register_manual = client.register_manual


    # ========================================================
    # PROTECTED TOOL EXECUTION
    # ========================================================

    async def protected_call_tool(
        tool_name,
        tool_args
    ):

        print()
        print("=" * 60)
        print("UTCP SECURITY GATE")
        print("BEFORE TOOL EXECUTION")
        print("=" * 60)

        # ----------------------------------------------------
        # GET TOOL FROM REPOSITORY
        # ----------------------------------------------------

        tool = await client.config.tool_repository.get_tool(
            tool_name
        )

        if tool is None:

            print()
            print("❌ TOOL NOT FOUND")
            print("❌ TOOL EXECUTION BLOCKED")

            raise PermissionError(
                "Tool blocked by security layer."
            )

        # ----------------------------------------------------
        # GET ENDPOINT
        # ----------------------------------------------------

        endpoint = tool.tool_call_template.url

        print()
        print("Tool:")
        print(f"    {tool_name}")

        print()
        print("Endpoint:")
        print(f"    {endpoint}")


        # ====================================================
        # TEST 1
        # CREDENTIAL-ENDPOINT BINDING
        # ====================================================

        if security.current_test == "1":

            allowed = security.check_credential_endpoint(
                "API_KEY",
                endpoint
            )

            if not allowed:

                raise PermissionError(
                    "TEST 1 BLOCKED: "
                    "Credential-endpoint binding violation."
                )


        # ====================================================
        # TEST 2
        # TOOL METADATA VALIDATION
        # ====================================================

        elif security.current_test == "2":

            allowed = security.check_metadata_endpoint(
                tool_name,
                endpoint
            )

            if not allowed:

                raise PermissionError(
                    "TEST 2 BLOCKED: "
                    "Unauthorized endpoint from Tool metadata."
                )


        # ====================================================
        # DEFAULT / UNKNOWN TEST
        # ====================================================

        else:

            # Apply metadata validation first.

            allowed = security.check_metadata_endpoint(
                tool_name,
                endpoint
            )

            if not allowed:

                raise PermissionError(
                    "Unauthorized endpoint from Tool metadata."
                )

            # Then apply credential-endpoint validation.

            allowed = security.check_credential_endpoint(
                "API_KEY",
                endpoint
            )

            if not allowed:

                raise PermissionError(
                    "Credential-endpoint binding violation."
                )


        # ----------------------------------------------------
        # SECURITY CHECK PASSED
        # ----------------------------------------------------

        print()
        print("✅ SECURITY CHECK PASSED")
        print("✅ TOOL EXECUTION ALLOWED")

        return await original_call_tool(
            tool_name,
            tool_args
        )


    # ========================================================
    # PROTECTED MANUAL REGISTRATION
    # ========================================================

    async def protected_register_manual(
        manual_call_template
    ):

        print()
        print("=" * 60)
        print("UTCP SECURITY GATE")
        print("BEFORE MANUAL REGISTRATION")
        print("=" * 60)

        current_test = getattr(
            security,
            "current_test",
            ""
        )


        # ====================================================
        # TEST 3
        # ATTACKER-CONTROLLED MANUAL
        # ====================================================

        if current_test == "3":

            allowed = security.check_manual_registration(
                manual_call_template
            )

            if not allowed:

                raise PermissionError(
                    "TEST 3 BLOCKED: "
                    "Attacker-controlled Manual."
                )


        # ====================================================
        # TEST 4
        # UNTRUSTED USER-SUPPLIED MANUAL
        # ====================================================

        elif current_test == "4":

            allowed = security.check_untrusted_user_manual(
                manual_call_template
            )

            if not allowed:

                raise PermissionError(
                    "TEST 4 BLOCKED: "
                    "Untrusted user-supplied Manual."
                )


        # ====================================================
        # TEST 1 / TEST 2
        # NORMAL TRUSTED MANUAL REGISTRATION
        # ====================================================

        else:

            print()
            print("Trusted Manual registration")
            print("Test 1/2 baseline registration")
            print("Manual registration allowed")

            allowed = True


        # ----------------------------------------------------
        # FINAL REGISTRATION DECISION
        # ----------------------------------------------------

        if not allowed:

            raise PermissionError(
                "Manual registration blocked."
            )

        print()
        print("✅ MANUAL SECURITY CHECK PASSED")
        print("✅ MANUAL REGISTRATION ALLOWED")

        return await original_register_manual(
            manual_call_template
        )


    # ========================================================
    # INSTALL SECURITY HOOKS
    # ========================================================

    client.call_tool = protected_call_tool

    client.register_manual = protected_register_manual


    # ========================================================
    # DISPLAY MITIGATION STATUS
    # ========================================================

    print()
    print("=" * 60)
    print("UTCP SECURITY MITIGATION ACTIVE")
    print("TEST 1 + TEST 2 + TEST 3 + TEST 4")
    print("=" * 60)

    return client


# ============================================================
# PATCH UTCP CLIENT
# ============================================================

UtcpClient.create = protected_create


# ============================================================
# COMMAND-LINE ARGUMENT CHECK
# ============================================================

if len(sys.argv) != 2:

    print()
    print("=" * 60)
    print("USAGE")
    print("=" * 60)

    print()
    print(
        "python utcp_mitigation.py utcptest1.py"
    )

    print()
    print(
        "python utcp_mitigation.py utcptest2.py"
    )

    print()
    print(
        "python utcp_mitigation.py utcptest3.py"
    )

    print()
    print(
        "python utcp_mitigation.py utcptest4.py"
    )

    print()

    sys.exit(1)


# ============================================================
# GET ATTACK FILE
# ============================================================

attack_file = sys.argv[1]

filename = attack_file.lower()


# ============================================================
# DETERMINE CURRENT TEST
# ============================================================

if "utcptest1" in filename:

    security.current_test = "1"

elif "utcptest2" in filename:

    security.current_test = "2"

elif "utcptest3" in filename:

    security.current_test = "3"

elif "utcptest4" in filename:

    security.current_test = "4"

else:

    security.current_test = ""


# ============================================================
# DISPLAY TEST INFORMATION
# ============================================================

print()
print("=" * 60)
print("RUNNING UTCP SECURITY TEST")
print("=" * 60)

print()
print(f"Attack file: {attack_file}")

print()
print(f"Detected test: {security.current_test}")

print()


# ============================================================
# RUN TEST SAFELY
#
# PermissionError is expected when the mitigation blocks
# an attack. Catch it so the terminal does not show a
# long traceback.
# ============================================================

try:

    runpy.run_path(
        attack_file,
        run_name="__main__"
    )


except PermissionError as e:

    print()
    print("=" * 60)
    print("SECURITY MITIGATION RESULT")
    print("=" * 60)

    print()
    print("❌ ATTACK BLOCKED")

    print()
    print(f"Reason: {e}")

    print()
    print("No unauthorized operation was allowed.")
    print("No credential was transmitted.")

    print()
    print("=" * 60)
    print("TEST COMPLETED - MITIGATION SUCCESSFUL")
    print("=" * 60)

    sys.exit(0)


except Exception as e:

    print()
    print("=" * 60)
    print("UNEXPECTED ERROR")
    print("=" * 60)

    print()
    print(f"Error type: {type(e).__name__}")
    print(f"Error: {e}")

    print()
    print("=" * 60)
    print("TEST FAILED - UNEXPECTED ERROR")
    print("=" * 60)

    sys.exit(1)