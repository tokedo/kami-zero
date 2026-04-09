"""
Kamigotchi MCP Executor — the agent's muscle.

Reads private keys from ~/.blocklife-keys/.env (outside the repo).
Exposes game actions as MCP tools. The LLM (brain) calls tools through
Claude Code; this server (muscle) handles secrets, API auth, and
transaction signing. The LLM never sees private keys.

Multi-account: keys file holds {LABEL}_OPERATOR_KEY / {LABEL}_OWNER_KEY
pairs. accounts/roster.yaml (in-repo) maps labels to public addresses.
All per-account tools accept an `account` label parameter (default "main").

Architecture:
  Claude Code (brain) --MCP--> executor (muscle) ---> Kamibots API / Yominet RPC
"""

import json
import os
import time
from pathlib import Path

import httpx
import yaml
from dotenv import load_dotenv, set_key
from eth_account.messages import encode_defunct
from mcp.server.fastmcp import FastMCP
from web3 import Web3

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parent.parent
_KEYS_PATH = Path.home() / ".blocklife-keys" / ".env"
_ROSTER_PATH = _REPO / "accounts" / "roster.yaml"

load_dotenv(_KEYS_PATH)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KAMIBOTS_BASE = "https://api.kamibots.xyz"
WORLD_ADDRESS = Web3.to_checksum_address(
    "0x2729174c265dbBd8416C6449E0E813E88f43D0E7"
)
CHAIN_ID = 428962654539583
RPC_URL = os.environ.get(
    "RPC_URL", "https://jsonrpc-yominet-1.anvil.asia-southeast.initia.xyz"
)

# ---------------------------------------------------------------------------
# Web3
# ---------------------------------------------------------------------------

w3 = Web3(Web3.HTTPProvider(RPC_URL))
_GAS_PRICE = {"maxFeePerGas": 2_500_000, "maxPriorityFeePerGas": 0}

_WORLD_ABI = json.loads(
    '[{"type":"function","name":"systems","inputs":[],'
    '"outputs":[{"type":"address"}],"stateMutability":"view"}]'
)
_SYSTEMS_COMPONENT_ABI = json.loads(
    '[{"type":"function","name":"getEntitiesWithValue",'
    '"inputs":[{"name":"v","type":"uint256"}],'
    '"outputs":[{"type":"uint256[]"}],"stateMutability":"view"}]'
)
_WORLD_FULL_ABI = json.loads(
    '[{"type":"function","name":"systems","inputs":[],'
    '"outputs":[{"type":"address"}],"stateMutability":"view"},'
    '{"type":"function","name":"components","inputs":[],'
    '"outputs":[{"type":"address"}],"stateMutability":"view"}]'
)
_world = w3.eth.contract(address=WORLD_ADDRESS, abi=_WORLD_FULL_ABI)
_system_cache: dict[str, str] = {}
_component_cache: dict[str, str] = {}


def _resolve_system(system_id: str) -> str:
    """Resolve system ID string to on-chain contract address (cached)."""
    if system_id not in _system_cache:
        h = int.from_bytes(Web3.keccak(text=system_id), "big")
        sc_addr = _world.functions.systems().call()
        sc = w3.eth.contract(address=sc_addr, abi=_SYSTEMS_COMPONENT_ABI)
        entities = sc.functions.getEntitiesWithValue(h).call()
        if not entities:
            raise ValueError(f"System not found on-chain: {system_id}")
        addr = Web3.to_checksum_address(
            "0x" + hex(entities[0])[2:].zfill(40)[-40:]
        )
        _system_cache[system_id] = addr
    return _system_cache[system_id]


def _resolve_component(component_id: str) -> str:
    """Resolve component ID string to on-chain contract address (cached)."""
    if component_id not in _component_cache:
        h = int.from_bytes(Web3.keccak(text=component_id), "big")
        cc_addr = _world.functions.components().call()
        cc = w3.eth.contract(address=cc_addr, abi=_SYSTEMS_COMPONENT_ABI)
        entities = cc.functions.getEntitiesWithValue(h).call()
        if not entities:
            raise ValueError(f"Component not found on-chain: {component_id}")
        addr = Web3.to_checksum_address(
            "0x" + hex(entities[0])[2:].zfill(40)[-40:]
        )
        _component_cache[component_id] = addr
    return _component_cache[component_id]


def _kami_entity_id(kami_index: int) -> int:
    """Derive kami entity ID from token index: keccak256("kami.id", index)."""
    return int.from_bytes(
        Web3.solidity_keccak(["string", "uint32"], ["kami.id", kami_index]), "big"
    )


def _account_entity_id(account: str) -> int:
    """Derive account entity ID from owner wallet address: uint256(address)."""
    acct = _get_account(account)
    if not acct.owner_addr:
        raise ValueError(f"Account '{account}' has no owner address")
    return int(acct.owner_addr, 16)


def _harvest_entity_id(kami_index: int) -> int:
    """Derive harvest entity ID: keccak256("harvest", kamiEntityId)."""
    kami_eid = _kami_entity_id(kami_index)
    return int.from_bytes(
        Web3.solidity_keccak(["string", "uint256"], ["harvest", kami_eid]), "big"
    )


def _quest_entity_id(quest_index: int, account_entity_id: int) -> int:
    """Derive quest instance entity ID: keccak256("quest.instance", index, accountId)."""
    return int.from_bytes(
        Web3.solidity_keccak(
            ["string", "uint32", "uint256"],
            ["quest.instance", quest_index, account_entity_id],
        ),
        "big",
    )


# Component read ABIs
_STRING_VALUE_ABI = json.loads(
    '[{"type":"function","name":"getValue",'
    '"inputs":[{"name":"entity","type":"uint256"}],'
    '"outputs":[{"type":"string"}],"stateMutability":"view"}]'
)
_UINT_VALUE_ABI = json.loads(
    '[{"type":"function","name":"getValue",'
    '"inputs":[{"name":"entity","type":"uint256"}],'
    '"outputs":[{"type":"uint256"}],"stateMutability":"view"}]'
)
_UINT32_VALUE_ABI = json.loads(
    '[{"type":"function","name":"getValue",'
    '"inputs":[{"name":"entity","type":"uint256"}],'
    '"outputs":[{"type":"uint32"}],"stateMutability":"view"}]'
)


# ---------------------------------------------------------------------------
# Account registry — loaded from .env + roster.yaml
# ---------------------------------------------------------------------------


class _Account:
    __slots__ = ("label", "operator_key", "owner_key", "operator_addr", "owner_addr")

    def __init__(self, label: str, operator_key: str, owner_key: str | None):
        self.label = label
        self.operator_key = operator_key
        self.owner_key = owner_key
        self.operator_addr = w3.eth.account.from_key(operator_key).address
        self.owner_addr = (
            w3.eth.account.from_key(owner_key).address if owner_key else None
        )


_accounts: dict[str, _Account] = {}

# Kamibots credentials — shared across accounts (per-user, not per-account).
# Auto-populated by register_kamibots tool.
_kamibots_api_key: str | None = os.environ.get("KAMIBOTS_API_KEY") or None
_privy_id: str | None = os.environ.get("PRIVY_ID") or None


def _load_accounts() -> None:
    """Scan .env for *_OPERATOR_KEY pairs, build account registry."""
    labels: set[str] = set()
    for key in os.environ:
        if key.endswith("_OPERATOR_KEY"):
            labels.add(key.removesuffix("_OPERATOR_KEY").lower())
        elif key.endswith("_OWNER_KEY"):
            labels.add(key.removesuffix("_OWNER_KEY").lower())

    for label in sorted(labels):
        op_key = os.environ.get(f"{label.upper()}_OPERATOR_KEY")
        own_key = os.environ.get(f"{label.upper()}_OWNER_KEY")
        if not op_key:
            print(
                f"WARNING: {label.upper()}_OPERATOR_KEY missing, "
                f"skipping account '{label}'"
            )
            continue
        _accounts[label] = _Account(label, op_key, own_key)

    # Cross-reference with roster.yaml
    if _ROSTER_PATH.exists():
        with open(_ROSTER_PATH) as f:
            roster = yaml.safe_load(f) or {}
        roster_labels = set((roster.get("accounts") or {}).keys())
        env_labels = set(_accounts.keys())
        for lbl in roster_labels - env_labels:
            print(f"WARNING: '{lbl}' in roster.yaml but no keys in .env")
        for lbl in env_labels - roster_labels:
            print(f"WARNING: '{lbl}' has keys in .env but not in roster.yaml")

    if _accounts:
        print(f"Loaded {len(_accounts)} account(s): {', '.join(_accounts.keys())}")
    else:
        print("WARNING: No accounts loaded. Fill .env with *_OPERATOR_KEY entries.")


_load_accounts()


def _get_account(label: str) -> _Account:
    """Look up account by label. Raises ValueError if not found."""
    if label not in _accounts:
        available = ", ".join(_accounts.keys()) or "(none)"
        raise ValueError(f"Account '{label}' not found. Available: {available}")
    return _accounts[label]


# ---------------------------------------------------------------------------
# Transaction helper
# ---------------------------------------------------------------------------


def _send_tx(
    account: str,
    system_id: str,
    abi: list,
    args: list,
    gas_limit: int | None = None,
) -> dict:
    """Build, sign, send a transaction with the account's operator key."""
    acct = _get_account(account)
    addr = _resolve_system(system_id)
    contract = w3.eth.contract(address=addr, abi=abi)
    fn = contract.functions.executeTyped(*args)

    tx_params = {
        "from": acct.operator_addr,
        "chainId": CHAIN_ID,
        "nonce": w3.eth.get_transaction_count(acct.operator_addr),
        **_GAS_PRICE,
    }
    if gas_limit:
        tx_params["gas"] = gas_limit

    built = fn.build_transaction(tx_params)
    signed = w3.eth.account.sign_transaction(built, private_key=acct.operator_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    return {
        "tx_hash": "0x" + receipt.transactionHash.hex(),
        "status": "success" if receipt.status == 1 else "reverted",
        "block": receipt.blockNumber,
        "gas_used": receipt.gasUsed,
        "account": account,
    }


# ---------------------------------------------------------------------------
# Kamibots API helpers
# ---------------------------------------------------------------------------


def _require_api_key() -> None:
    if not _kamibots_api_key:
        raise ValueError(
            "Kamibots API key not set. Call register_kamibots(account) first."
        )


def _headers() -> dict:
    _require_api_key()
    return {"X-Agent-Key": _kamibots_api_key}


async def _api_get(path: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(f"{KAMIBOTS_BASE}{path}", headers=_headers())
        r.raise_for_status()
        return r.json()


async def _api_post(path: str, body: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            f"{KAMIBOTS_BASE}{path}", headers=_headers(), json=body or {}
        )
        if r.status_code >= 400:
            try:
                detail = r.json()
            except Exception:
                detail = r.text
            raise RuntimeError(
                f"API {r.status_code} on POST {path}: {detail}"
            )
        return r.json()


async def _api_delete(path: str, body: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.request(
            "DELETE",
            f"{KAMIBOTS_BASE}{path}",
            headers={**_headers(), "Content-Type": "application/json"},
            content=json.dumps(body) if body else None,
        )
        r.raise_for_status()
        return r.json()


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP("kamigotchi-executor")

# ---- Setup & account management ----


@mcp.tool()
def list_accounts() -> dict:
    """List all configured accounts with labels and public addresses.

    No private data is exposed. Shows whether Kamibots API is registered.
    """
    accts = {}
    for label, acct in _accounts.items():
        accts[label] = {
            "operator_address": acct.operator_addr,
            "owner_address": acct.owner_addr,
        }
    return {"accounts": accts, "kamibots_registered": _kamibots_api_key is not None}


@mcp.tool()
async def register_kamibots(account: str = "main") -> dict:
    """Register with Kamibots API using the account's owner wallet.

    Signs a registration message, obtains API key and privy_id, and saves
    them to .env automatically. Only needs to be called once — credentials
    are shared across all accounts.

    Args:
        account: Account label (must have an owner key in .env).
    """
    global _kamibots_api_key, _privy_id

    acct = _get_account(account)
    if not acct.owner_key:
        raise ValueError(
            f"Account '{account}' has no owner key. "
            f"Set {account.upper()}_OWNER_KEY in .env."
        )

    timestamp = int(time.time())
    message = f"Register for Kamibots: {timestamp}"
    signable = encode_defunct(text=message)
    signed = w3.eth.account.sign_message(signable, private_key=acct.owner_key)

    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            f"{KAMIBOTS_BASE}/api/agent/register",
            json={
                "walletAddress": acct.owner_addr,
                "signature": "0x" + signed.signature.hex(),
                "message": message,
                "label": f"Agent ({account})",
            },
        )
        r.raise_for_status()
        data = r.json()

    api_key = data.get("apiKey")
    privy_id = data.get("privyId")

    if api_key:
        _kamibots_api_key = api_key
        set_key(str(_KEYS_PATH), "KAMIBOTS_API_KEY", api_key)
    if privy_id:
        _privy_id = privy_id
        set_key(str(_KEYS_PATH), "PRIVY_ID", privy_id)

    return {
        "registered": True,
        "is_new_user": data.get("isNewUser"),
        "has_operator_key": data.get("hasOperatorKey"),
        "api_key_saved": bool(api_key),
        "privy_id_saved": bool(privy_id),
        "message": "API key and privy_id saved to .env. "
        "Next: call store_operator_key() for each account.",
    }


@mcp.tool()
async def store_operator_key(account: str = "main") -> dict:
    """Send the account's operator key to Kamibots for strategy execution.

    The key is encrypted at rest (AES-256-GCM) on Kamibots servers.
    Must be called after register_kamibots() and before starting strategies.

    Args:
        account: Account label.
    """
    acct = _get_account(account)
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            f"{KAMIBOTS_BASE}/api/agent/operator-key",
            headers=_headers(),
            json={"operatorKey": acct.operator_key},
        )
        r.raise_for_status()

    return {
        "account": account,
        "operator_address": acct.operator_addr,
        "stored": True,
        "message": "Operator key stored securely",
    }


# ---- Kamibots API: state reads ----


@mcp.tool()
async def get_tier(account: str = "main") -> dict:
    """Account tier info: tier name, tax rate, total/used/remaining strategy slots.

    Args:
        account: Account label (for context; API key is shared).
    """
    return await _api_get("/api/agent/tier")


@mcp.tool()
async def get_inventory(account: str = "main") -> dict:
    """All items and balances in the account inventory.

    Args:
        account: Account label (for context; API key is shared).
    """
    return await _api_get("/api/agent/inventory")


@mcp.tool()
async def get_kami_state(kami_id: int, account: str = "main") -> dict:
    """Full kami data via playwright endpoint: stats, harvest, skills, traits, bonuses.

    Args:
        kami_id: Kami token index (e.g. 45).
        account: Account label (for context).
    """
    return await _api_get(f"/api/playwright/kami/{kami_id}/")


@mcp.tool()
async def get_kami_state_slim(kami_id: int, account: str = "main") -> dict:
    """Slim kami data: stats, harvest, skills, bonuses. Lighter than full state.

    Args:
        kami_id: Kami token index (e.g. 45).
        account: Account label (for context).
    """
    return await _api_get(f"/api/playwright/kami/{kami_id}/slim")


@mcp.tool()
async def get_all_strategies(account: str = "main") -> dict:
    """List all active strategies for this account.

    Args:
        account: Account label (for context; API key is shared).
    """
    return await _api_get("/api/agent/strategies")


@mcp.tool()
async def get_strategy_status(kami_id: int, account: str = "main") -> dict:
    """Strategy status for a specific kami. Cached 15s server-side.

    Args:
        kami_id: Kami token index.
        account: Account label (for context).
    """
    return await _api_get(f"/api/strategies/status/{kami_id}")


@mcp.tool()
async def get_strategy_logs(
    container_id: str, tail: int = 30, account: str = "main"
) -> dict:
    """Recent log lines from a running strategy container.

    Args:
        container_id: Strategy container ID (from start response or strategy list).
        tail: Number of log lines to return (default 30).
        account: Account label (for context).
    """
    return await _api_get(f"/api/strategies/{container_id}/logs?tail={tail}")


@mcp.tool()
async def get_prices() -> dict:
    """Latest marketplace prices for all items. Cached ~3 minutes."""
    return await _api_get("/api/prices/latest")


@mcp.tool()
async def get_npc_prices() -> dict:
    """Live NPC shop prices for all items."""
    return await _api_get("/api/npc-prices/live")


@mcp.tool()
async def get_nodes() -> dict:
    """All harvest nodes: affinity, room, drops, level requirements. Cached 24h."""
    return await _api_get("/api/playwright/nodes")


@mcp.tool()
async def get_account_kamis(
    account: str = "main", address: str = ""
) -> dict:
    """List all kamis for an address. Defaults to the account's operator address.

    Args:
        account: Account label.
        address: Override address (default: account's operator address).
    """
    if not address:
        address = _get_account(account).operator_addr
    return await _api_get(f"/api/accounts/{address}/kamis")


# ---- Kamibots API: strategy management ----


@mcp.tool()
async def start_strategy(
    strategy_type: str,
    config: dict,
    kami_id: int = 0,
    node_id: int = 0,
    account: str = "main",
) -> dict:
    """Start a Kamibots strategy.

    Args:
        strategy_type: One of harvestAndRest, harvestAndFeed, rest_v3,
            auto_v2, bodyguard, craft.
        config: Strategy-specific config dict.
            See integration/kamibots/README.md for schemas.
        kami_id: Kami token index. Required for all strategies. For
            multi-kami strategies (auto_v2, rest_v3), pass any kami
            from the group.
        node_id: Harvest node index. Must match kami's current room.
        account: Account label.
    """
    if not _privy_id:
        raise ValueError("privy_id not set. Call register_kamibots() first.")
    return await _api_post(
        "/api/strategies/start",
        {
            "strategyType": strategy_type,
            "kamiId": kami_id,
            "nodeId": node_id,
            "config": config,
            "keyData": {"privy_id": _privy_id},
        },
    )


@mcp.tool()
async def stop_strategy(kami_id: int, account: str = "main") -> dict:
    """Stop the running strategy for a kami.

    Args:
        kami_id: Kami token index.
        account: Account label.
    """
    if not _privy_id:
        raise ValueError("privy_id not set. Call register_kamibots() first.")
    return await _api_delete(
        f"/api/strategies/kami/{kami_id}",
        {"keyData": {"privy_id": _privy_id}},
    )


# ---- On-chain: direct game actions ----

_ABI_MOVE = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"roomIndex","type":"uint32"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)
_ABI_FEED = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"kamiID","type":"uint256"},{"name":"itemIndex","type":"uint32"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)
_ABI_REVIVE = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"id","type":"uint256"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)
_ABI_LEVEL = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"kamiID","type":"uint256"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)
_ABI_EQUIP = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"kamiID","type":"uint256"},{"name":"itemIndex","type":"uint32"}],'
    '"outputs":[{"type":"uint256"}],"stateMutability":"nonpayable"}]'
)
_ABI_UNEQUIP = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"kamiID","type":"uint256"},{"name":"slotType","type":"string"}],'
    '"outputs":[{"type":"uint32"}],"stateMutability":"nonpayable"}]'
)
_ABI_HARVEST_START = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"kamiID","type":"uint256"},{"name":"nodeIndex","type":"uint32"},'
    '{"name":"taxerID","type":"uint256"},{"name":"taxAmt","type":"uint256"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"},'
    '{"type":"function","name":"executeBatched",'
    '"inputs":[{"name":"kamiIDs","type":"uint256[]"},{"name":"nodeIndex","type":"uint32"},'
    '{"name":"taxerID","type":"uint256"},{"name":"taxAmt","type":"uint256"}],'
    '"outputs":[{"type":"bytes[]"}],"stateMutability":"nonpayable"}]'
)
_ABI_HARVEST_STOP = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"id","type":"uint256"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"},'
    '{"type":"function","name":"executeBatched",'
    '"inputs":[{"name":"ids","type":"uint256[]"}],'
    '"outputs":[{"type":"bytes[]"}],"stateMutability":"nonpayable"}]'
)
_ABI_HARVEST_COLLECT = _ABI_HARVEST_STOP  # same signature
_ABI_LISTING_BUY = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"merchantIndex","type":"uint32"},'
    '{"name":"itemIndices","type":"uint32[]"},'
    '{"name":"amts","type":"uint32[]"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)


@mcp.tool()
def harvest_start(kami_ids: list[int], node_index: int, account: str = "bpeon") -> dict:
    """Start harvesting for one or more kamis at a node. Costs gas.

    Kamis must be in the same room as the node and not already harvesting.
    Uses batch variant for multiple kamis (1 tx).

    Args:
        kami_ids: List of kami token indices.
        node_index: Harvest node index (same as room index).
        account: Account label.
    """
    entity_ids = [_kami_entity_id(k) for k in kami_ids]
    if len(entity_ids) == 1:
        return _send_tx(
            account, "system.harvest.start", _ABI_HARVEST_START,
            [entity_ids[0], node_index, 0, 0], gas_limit=1_500_000,
        )
    # Batch
    acct = _get_account(account)
    addr = _resolve_system("system.harvest.start")
    contract = w3.eth.contract(address=addr, abi=_ABI_HARVEST_START)
    fn = contract.functions.executeBatched(entity_ids, node_index, 0, 0)
    tx_params = {
        "from": acct.operator_addr,
        "chainId": CHAIN_ID,
        "nonce": w3.eth.get_transaction_count(acct.operator_addr),
        "gas": 1_500_000 * len(entity_ids),
        **_GAS_PRICE,
    }
    built = fn.build_transaction(tx_params)
    signed = w3.eth.account.sign_transaction(built, private_key=acct.operator_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    return {
        "tx_hash": "0x" + receipt.transactionHash.hex(),
        "status": "success" if receipt.status == 1 else "reverted",
        "block": receipt.blockNumber,
        "gas_used": receipt.gasUsed,
        "kamis": kami_ids,
        "node": node_index,
    }


def _send_batch_tx(
    account: str,
    system_id: str,
    abi: list,
    fn_name: str,
    args: list,
    gas_per_item: int,
) -> dict:
    """Build, sign, send a batch transaction."""
    acct = _get_account(account)
    addr = _resolve_system(system_id)
    contract = w3.eth.contract(address=addr, abi=abi)
    fn = getattr(contract.functions, fn_name)(*args)
    tx_params = {
        "from": acct.operator_addr,
        "chainId": CHAIN_ID,
        "nonce": w3.eth.get_transaction_count(acct.operator_addr),
        "gas": gas_per_item * max(len(args[0]) if isinstance(args[0], list) else 1, 1),
        **_GAS_PRICE,
    }
    built = fn.build_transaction(tx_params)
    signed = w3.eth.account.sign_transaction(built, private_key=acct.operator_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    return {
        "tx_hash": "0x" + receipt.transactionHash.hex(),
        "status": "success" if receipt.status == 1 else "reverted",
        "block": receipt.blockNumber,
        "gas_used": receipt.gasUsed,
    }


@mcp.tool()
def harvest_stop(kami_ids: list[int], account: str = "bpeon") -> dict:
    """Stop active harvests and auto-collect rewards. Costs gas.

    Uses batch variant for multiple kamis (1 tx). Rewards + scavenge
    points are distributed on stop.

    Args:
        kami_ids: List of kami token indices whose harvests to stop.
        account: Account label.
    """
    h_ids = [_harvest_entity_id(k) for k in kami_ids]
    if len(h_ids) == 1:
        return _send_tx(
            account, "system.harvest.stop", _ABI_HARVEST_STOP,
            [h_ids[0]], gas_limit=2_000_000,
        )
    result = _send_batch_tx(
        account, "system.harvest.stop", _ABI_HARVEST_STOP,
        "executeBatched", [h_ids], 2_000_000,
    )
    result["kamis"] = kami_ids
    return result


@mcp.tool()
def harvest_collect(kami_ids: list[int], account: str = "bpeon") -> dict:
    """Collect rewards from active harvests WITHOUT stopping them. Costs gas.

    Partial collection — kamis keep harvesting. Rewards + scavenge points
    are distributed.

    Args:
        kami_ids: List of kami token indices whose harvests to collect.
        account: Account label.
    """
    h_ids = [_harvest_entity_id(k) for k in kami_ids]
    if len(h_ids) == 1:
        return _send_tx(
            account, "system.harvest.collect", _ABI_HARVEST_COLLECT,
            [h_ids[0]], gas_limit=2_000_000,
        )
    result = _send_batch_tx(
        account, "system.harvest.collect", _ABI_HARVEST_COLLECT,
        "executeBatched", [h_ids], 2_000_000,
    )
    result["kamis"] = kami_ids
    return result


@mcp.tool()
def move_to_room(room_index: int, account: str = "main") -> dict:
    """Move the account to a different room. Costs stamina.

    Args:
        room_index: Target room number (1-70). See catalogs/rooms.csv.
        account: Account label.
    """
    return _send_tx(
        account, "system.account.move", _ABI_MOVE, [room_index], gas_limit=1_200_000
    )


@mcp.tool()
def listing_buy(
    merchant_index: int,
    item_indices: list[int],
    amounts: list[int],
    account: str = "bpeon",
) -> dict:
    """Buy items from an NPC merchant. Must be in the merchant's room.

    Args:
        merchant_index: NPC merchant index (1=Mina, 2=Vending Machine).
        item_indices: List of item indices to buy (global item index, e.g. 11301).
        amounts: List of amounts for each item (parallel to item_indices).
        account: Account label.
    """
    if len(item_indices) != len(amounts):
        raise ValueError("item_indices and amounts must have the same length")
    return _send_tx(
        account,
        "system.listing.buy",
        _ABI_LISTING_BUY,
        [merchant_index, item_indices, amounts],
        gas_limit=1_500_000,
    )


@mcp.tool()
def feed_kami(kami_id: int, food_item_id: int, account: str = "main") -> dict:
    """Use a food item on a kami to restore HP. Works while harvesting.

    Args:
        kami_id: Kami token index (e.g. 45).
        food_item_id: Item ID for the food. Common foods:
            11301=gum(25hp), 11302=burger(50hp), 11303=candy(50hp),
            11304=cookies(100hp), 11311=resin(35hp), 11312=honeydew(75hp),
            11313=golden_apple(150hp), 11314=blue_pansy(25hp).
        account: Account label.
    """
    return _send_tx(
        account,
        "system.kami.use.item",
        _ABI_FEED,
        [_kami_entity_id(kami_id), food_item_id],
    )


@mcp.tool()
def revive_kami(kami_id: int, account: str = "main") -> dict:
    """Revive a dead kami. Costs 33 Onyx Shards. Restores 33 HP -> RESTING.

    Args:
        kami_id: Kami token index (e.g. 45).
        account: Account label.
    """
    return _send_tx(account, "system.kami.onyx.revive", _ABI_REVIVE, [kami_id])


@mcp.tool()
def level_up_kami(kami_id: int, account: str = "main") -> dict:
    """Level up a kami if it has enough XP. Grants 1 skill point.

    Args:
        kami_id: Kami token index (e.g. 45).
        account: Account label.
    """
    return _send_tx(
        account, "system.kami.level", _ABI_LEVEL, [_kami_entity_id(kami_id)]
    )


@mcp.tool()
def equip_item(kami_id: int, item_index: int, account: str = "main") -> dict:
    """Equip an inventory item to a kami. Kami must be RESTING.

    Args:
        kami_id: Kami token index (e.g. 45).
        item_index: Item index from inventory (e.g. 1001 for Wooden Stick).
        account: Account label.
    """
    return _send_tx(
        account,
        "system.kami.equip",
        _ABI_EQUIP,
        [_kami_entity_id(kami_id), item_index],
    )


@mcp.tool()
def unequip_item(kami_id: int, slot_type: str, account: str = "main") -> dict:
    """Unequip an item from a kami slot. Kami must be RESTING.

    Args:
        kami_id: Kami token index (e.g. 45).
        slot_type: Equipment slot name (e.g. "Kami_Pet_Slot").
        account: Account label.
    """
    return _send_tx(
        account,
        "system.kami.unequip",
        _ABI_UNEQUIP,
        [_kami_entity_id(kami_id), slot_type],
    )


# ---- On-chain: quest management ----

_ABI_QUEST_ACCEPT = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"index","type":"uint32"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)
_ABI_QUEST_COMPLETE = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"id","type":"uint256"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)
_ABI_QUEST_DROP = _ABI_QUEST_COMPLETE  # same signature


@mcp.tool()
def get_active_quests(account: str = "bpeon") -> dict:
    """Enumerate all active quests for the account by reading on-chain state.

    Returns quest entity IDs and, where possible, matched quest indices.

    Args:
        account: Account label.
    """
    acc_id = _account_entity_id(account)

    owns_addr = _resolve_component("component.id.quest.owns")
    owns_comp = w3.eth.contract(
        address=owns_addr, abi=_SYSTEMS_COMPONENT_ABI
    )
    quest_eids = owns_comp.functions.getEntitiesWithValue(acc_id).call()

    # Pre-compute entity IDs for known quest indices to reverse-map
    known_indices = list(range(1, 109)) + list(range(2001, 2017)) + list(range(3001, 3025))
    eid_to_index = {}
    for idx in known_indices:
        eid_to_index[_quest_entity_id(idx, acc_id)] = idx

    quests = []
    for eid in quest_eids:
        q: dict = {"entity_id": hex(eid)}
        if eid in eid_to_index:
            q["quest_index"] = eid_to_index[eid]
        quests.append(q)

    return {
        "account": account,
        "active_quest_count": len(quests),
        "quests": quests,
    }


@mcp.tool()
def get_quest_status(quest_index: int, account: str = "bpeon") -> dict:
    """Check the on-chain state of a specific quest for the account.

    Returns the quest state string if active, or indicates not accepted.

    Args:
        quest_index: Quest index (1-108 main, 2001-2016 Mina, 3001+ side).
        account: Account label.
    """
    acc_id = _account_entity_id(account)
    q_id = _quest_entity_id(quest_index, acc_id)

    state_addr = _resolve_component("component.state")
    state_comp = w3.eth.contract(address=state_addr, abi=_STRING_VALUE_ABI)

    try:
        state = state_comp.functions.getValue(q_id).call()
        return {
            "quest_index": quest_index,
            "entity_id": hex(q_id),
            "state": state,
            "active": bool(state),
        }
    except Exception as e:
        return {
            "quest_index": quest_index,
            "entity_id": hex(q_id),
            "state": None,
            "active": False,
            "note": f"Not accepted or already completed ({e})",
        }


@mcp.tool()
def accept_quest(quest_index: int, account: str = "bpeon") -> dict:
    """Accept a quest by index. Costs gas.

    Requirements are checked on-chain (previous quest completed, location, etc).

    Args:
        quest_index: Quest index to accept.
        account: Account label.
    """
    return _send_tx(
        account,
        "system.quest.accept",
        _ABI_QUEST_ACCEPT,
        [quest_index],
        gas_limit=1_500_000,
    )


@mcp.tool()
def complete_quest(quest_index: int, account: str = "bpeon") -> dict:
    """Complete an active quest. Costs gas. All objectives must be met.

    Computes the quest entity ID from the index and account.

    Args:
        quest_index: Quest index of the active quest to complete.
        account: Account label.
    """
    acc_id = _account_entity_id(account)
    q_id = _quest_entity_id(quest_index, acc_id)
    return _send_tx(
        account,
        "system.quest.complete",
        _ABI_QUEST_COMPLETE,
        [q_id],
        gas_limit=2_000_000,
    )


@mcp.tool()
def check_quest_completable(quest_index: int, account: str = "bpeon") -> dict:
    """Check if a quest can be completed right now (free staticCall, no gas).

    Returns completable=True if all objectives are met.

    Args:
        quest_index: Quest index to check.
        account: Account label.
    """
    acc_id = _account_entity_id(account)
    q_id = _quest_entity_id(quest_index, acc_id)

    addr = _resolve_system("system.quest.complete")
    contract = w3.eth.contract(address=addr, abi=_ABI_QUEST_COMPLETE)

    acct = _get_account(account)
    try:
        contract.functions.executeTyped(q_id).call(
            {"from": acct.operator_addr}
        )
        return {"quest_index": quest_index, "completable": True}
    except Exception as e:
        return {
            "quest_index": quest_index,
            "completable": False,
            "reason": str(e),
        }


@mcp.tool()
def drop_quest(quest_index: int, account: str = "bpeon") -> dict:
    """Drop/abandon an active quest. Costs gas.

    Args:
        quest_index: Quest index of the active quest to drop.
        account: Account label.
    """
    acc_id = _account_entity_id(account)
    q_id = _quest_entity_id(quest_index, acc_id)
    return _send_tx(
        account,
        "system.quest.drop",
        _ABI_QUEST_DROP,
        [q_id],
        gas_limit=1_000_000,
    )


# ---------------------------------------------------------------------------
# Scavenge & Droptable
# ---------------------------------------------------------------------------


def _scavenge_registry_id(node_index: int) -> int:
    """Registry scavenge bar ID: keccak256("registry.scavenge", "NODE", nodeIndex)."""
    return int.from_bytes(
        Web3.solidity_keccak(
            ["string", "string", "uint32"],
            ["registry.scavenge", "NODE", node_index],
        ),
        "big",
    )


def _scavenge_instance_id(node_index: int, account: str) -> int:
    """Per-account scavenge instance: keccak256("scavenge.instance", "NODE", nodeIndex, holderID)."""
    acc_id = _account_entity_id(account)
    return int.from_bytes(
        Web3.solidity_keccak(
            ["string", "string", "uint32", "uint256"],
            ["scavenge.instance", "NODE", node_index, acc_id],
        ),
        "big",
    )


_ABI_SCAV_CLAIM = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"scavBarID","type":"uint256"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)
_ABI_DROPTABLE_REVEAL = json.loads(
    '[{"type":"function","name":"executeTyped",'
    '"inputs":[{"name":"commitIDs","type":"uint256[]"}],'
    '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
)


@mcp.tool()
def get_scavenge_points(node_index: int, account: str = "bpeon") -> dict:
    """Check accumulated scavenge points for a node.

    Reads the Value component on the scavenge instance entity.

    Args:
        node_index: Harvest node index (e.g., 47 for Scrap Paths).
        account: Account label.
    """
    instance_id = _scavenge_instance_id(node_index, account)
    comp_addr = _resolve_component("component.value")
    comp = w3.eth.contract(address=comp_addr, abi=_UINT_VALUE_ABI)
    try:
        points = comp.functions.getValue(instance_id).call()
    except Exception:
        points = 0
    return {
        "node_index": node_index,
        "account": account,
        "points": points,
        "instance_entity": hex(instance_id),
    }


@mcp.tool()
def scavenge_claim(node_index: int, account: str = "bpeon") -> dict:
    """Claim scavenge rewards for a node. Costs gas.

    Triggers droptable commit(s) that must be revealed in a later block.

    Args:
        node_index: Harvest node index.
        account: Account label.
    """
    reg_id = _scavenge_registry_id(node_index)
    return _send_tx(
        account,
        "system.scavenge.claim",
        _ABI_SCAV_CLAIM,
        [reg_id],
        gas_limit=2_000_000,
    )


@mcp.tool()
def droptable_reveal(commit_ids: list[int], account: str = "bpeon") -> dict:
    """Reveal droptable commits to receive items. Costs gas.

    Must be called in a later block than the claim that created the commits.

    Args:
        commit_ids: List of commit entity IDs from scavenge claims.
        account: Account label.
    """
    return _send_tx(
        account,
        "system.droptable.item.reveal",
        _ABI_DROPTABLE_REVEAL,
        [commit_ids],
        gas_limit=2_000_000,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
