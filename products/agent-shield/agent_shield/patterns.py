"""
Pattern definitions for agent-shield security scanner.

Each pattern is a tuple of:
  (name, regex, risk_level, description)

Risk levels: MEDIUM, HIGH, CRITICAL
"""

from typing import Tuple, List

Pattern = Tuple[str, str, str, str]

# Applied to text fields: skill name, description, instructions, system_prompt.
# Also applied to JSON/YAML/Markdown files.
PROMPT_INJECTION: List[Pattern] = [
    (
        "prompt_override",
        r"ignore (all |your )?(previous|prior) instructions",
        "HIGH",
        "Classic prompt injection: override instructions",
    ),
    (
        "prompt_override_2",
        r"disregard (all |your )?(previous|prior|above)",
        "HIGH",
        "Prompt injection: disregard instructions",
    ),
    (
        "role_hijack",
        r"you are now|your (true |real |actual )?(purpose|instructions|goal) (is|are)",
        "HIGH",
        "Role hijacking attempt",
    ),
    (
        "jailbreak",
        r"(ignore|forget|discard|bypass) (everything|all|any) (above|before|prior)",
        "HIGH",
        "Jailbreak attempt",
    ),
    (
        "hidden_instruction",
        r"<(system|SYSTEM)>|<\|im_start\|>|\[INST\]|\[\/INST\]",
        "MEDIUM",
        "Hidden instruction markup in text",
    ),
    (
        "exfil_instruction",
        r"send (this|the|all|my) (conversation|message|chat|history|data|context) to",
        "CRITICAL",
        "Data exfiltration instruction",
    ),
    (
        "base64_in_text",
        r"base64[_\-]?decode|atob\(|fromBase64",
        "MEDIUM",
        "Base64 encoded content in descriptor",
    ),
]

# Applied to code files: .py, .js, .ts
CODE_EXECUTION: List[Pattern] = [
    (
        "eval_exec",
        r"\beval\s*\(|\bexec\s*\(",
        "HIGH",
        "Dynamic code execution (eval/exec)",
    ),
    (
        "subprocess_shell",
        r"subprocess\.(call|run|Popen).*shell\s*=\s*True|os\.system\(|os\.popen\(",
        "HIGH",
        "Shell command execution",
    ),
    (
        "import_hijack",
        r"__import__\s*\(|importlib\.import_module",
        "MEDIUM",
        "Dynamic import (potential code injection)",
    ),
    (
        "encoded_payload",
        r"base64\.b64decode.*exec|exec.*base64\.b64decode",
        "CRITICAL",
        "Encoded payload execution",
    ),
    (
        "env_exfil",
        r"os\.environ.*requests?\.(post|put|get)|subprocess.*os\.environ",
        "CRITICAL",
        "Environment variable exfiltration",
    ),
]

# Applied to all file types — credential and secret targeting patterns.
CREDENTIAL_THEFT: List[Pattern] = [
    (
        "ssh_key_access",
        r"\.ssh[/\\](id_rsa|id_ed25519|authorized_keys|known_hosts)",
        "HIGH",
        "SSH key file access",
    ),
    (
        "keychain_access",
        r"Library[/\\]Keychains|/Keychain|security find-generic-password",
        "HIGH",
        "macOS keychain access (AMOS pattern)",
    ),
    (
        "wallet_seed",
        r"\b(mnemonic|seed.phrase|private.key|wallet.*seed)\b",
        "HIGH",
        "Crypto wallet credential targeting",
    ),
    (
        "browser_credentials",
        r"Login Data|cookies\.sqlite|logins\.json|chrome.*default.*login",
        "HIGH",
        "Browser credential file targeting",
    ),
    (
        "env_secrets",
        r"(API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE_KEY)\s*=",
        "MEDIUM",
        "Hardcoded credential patterns",
    ),
]

# Applied to code files — suspicious network patterns.
NETWORK_EXFIL: List[Pattern] = [
    (
        "raw_socket",
        r"socket\.socket\(\s*socket\.AF_INET.*socket\.SOCK_STREAM\s*\).*connect",
        "HIGH",
        "Raw socket connection (potential reverse shell)",
    ),
    (
        "external_post_with_data",
        r"requests\.post\(['\"]https?://[^'\"]+['\"].*data=.*os\.environ|urllib.*POST.*os\.environ",
        "CRITICAL",
        "Exfiltrating environment to external URL",
    ),
    (
        "dns_exfil",
        r"socket\.gethostbyname.*os\.environ|nslookup.*\$\(",
        "HIGH",
        "DNS-based data exfiltration",
    ),
]

# File extensions that get code-specific patterns applied.
CODE_EXTENSIONS = {".py", ".js", ".ts"}

# File extensions that get text/descriptor patterns applied.
TEXT_EXTENSIONS = {".json", ".yaml", ".yml", ".md"}

# All scannable extensions.
SCANNABLE_EXTENSIONS = CODE_EXTENSIONS | TEXT_EXTENSIONS

# Applied to MCP server config fields (command, args) — checked structurally.
MCP_COMMAND: List[Pattern] = [
    (
        "mcp_download_exec",
        r"(curl|wget)\s.*(sh|bash|python|node|ruby|perl)\b|\|.*(sh|bash|python3?|node)\b",
        "CRITICAL",
        "Download-and-execute pattern in MCP server command/args",
    ),
    (
        "mcp_base64_exec",
        r"base64\s*(--decode|-d)|echo\s+[A-Za-z0-9+/]{20,}.*\|\s*(sh|bash|python3?|node)",
        "CRITICAL",
        "Base64 payload execution in MCP server command/args",
    ),
    (
        "mcp_shell_chain",
        r"[;&`]|\$\(",
        "HIGH",
        "Shell metacharacters in MCP server command (potential injection)",
    ),
    (
        "mcp_tmp_path",
        r"/tmp/|/var/tmp/|\\Temp\\",
        "HIGH",
        "Temporary directory path in MCP server command",
    ),
]

# Applied to MCP server env var values — checked structurally.
MCP_ENV: List[Pattern] = [
    (
        "mcp_env_exfil_url",
        r"https?://[^\s\"']*\$\{?[A-Z_]{3,}",
        "CRITICAL",
        "Env variable embedded in URL (potential credential exfiltration)",
    ),
    (
        "mcp_env_webhook",
        r"https?://(webhook\.|hooks\.|discord\.com/api/webhooks|slack\.com/services|pipedream\.net)",
        "HIGH",
        "Webhook URL in MCP env var (potential exfiltration endpoint)",
    ),
    (
        "mcp_env_hardcoded_secret",
        r"(?i)(password|secret|private_key|api_key|access_token)\s*=\s*.{16,}",
        "HIGH",
        "Hardcoded credential in MCP env var value",
    ),
]

# Risk level ordering for comparison.
RISK_ORDER = {"CLEAN": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


def patterns_for_extension(extension: str) -> List[Pattern]:
    """Return the applicable pattern list for a given file extension."""
    ext = extension.lower()
    if ext in CODE_EXTENSIONS:
        return PROMPT_INJECTION + CODE_EXECUTION + CREDENTIAL_THEFT + NETWORK_EXFIL
    if ext in TEXT_EXTENSIONS:
        return PROMPT_INJECTION + CREDENTIAL_THEFT
    return []


def higher_risk(a: str, b: str) -> str:
    """Return whichever risk level is higher."""
    if RISK_ORDER.get(a, 0) >= RISK_ORDER.get(b, 0):
        return a
    return b
