import requests
from typing import TypedDict, List, Optional
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import AzureChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langchain.schema import SystemMessage
import os
import json

# === CONFIG ===
settings_path = os.path.join(os.path.dirname(__file__), '../LangGraph/settings.json')
with open(settings_path, 'r') as f:
    settings = json.load(f)

AZURE_OPENAI_API_KEY = settings["AZURE_OPENAI_KEY"]
AZURE_OPENAI_ENDPOINT = settings["AZURE_OPENAI_ENDPOINT"]
AZURE_DEPLOYMENT_NAME = "gpt-4.1"
BASE_API_URL = "http://localhost:5000/orders"

# === LANGCHAIN LLM ===the execution seem to struck
llm = AzureChatOpenAI(
    openai_api_key=AZURE_OPENAI_API_KEY,
    openai_api_base=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT_NAME,
    openai_api_version="2023-05-15",
    temperature=0
)

# === MEMORY STATE ===
class OrderState(TypedDict):
    last_order_id: Optional[int]
    last_order_data: Optional[dict]

initial_state: OrderState = {"last_order_id": None, "last_order_data": None}

# === FUNCTION TOOLS ===

@tool("create_order")
def create_order_tool(
    organization: str,
    transaction_type: str,
    parties: List[dict] = None,
    services: List[dict] = None,
    charges: List[dict] = None,
    deposits: List[dict] = None,
    loans: List[dict] = None,
    fees: List[dict] = None
) -> dict:
    """Create a new order. Organization and transaction_type are required. Others are optional lists."""
    payload = {
        "organization": organization,
        "transactionType": transaction_type,
    }
    if parties is not None:
        payload["parties"] = parties
    if services is not None:
        payload["services"] = services
    if charges is not None:
        payload["charges"] = charges
    if deposits is not None:
        payload["deposits"] = deposits
    if loans is not None:
        payload["loans"] = loans
    if fees is not None:
        payload["fees"] = fees
    res = requests.post(BASE_API_URL, json=payload)
    return res.json()

@tool("get_order")
def get_order_tool(id: int) -> dict:
    """Get an order by ID."""
    res = requests.get(f"{BASE_API_URL}/{id}")
    return res.json()

@tool("get_all_orders")
def get_all_orders_tool() -> list:
    """Retrieve all orders."""
    res = requests.get(BASE_API_URL)
    return res.json()

@tool("add_or_update_service")
def add_or_update_service_tool(id: int, type: str) -> dict:
    """Add or update a service for an order. Type is required (e.g., Escrow/Title/Both)."""
    payload = {"type": type}
    res = requests.put(f"{BASE_API_URL}/{id}/services", json=payload)
    return res.json()

@tool("add_or_update_party")
def add_or_update_party_tool(id: int, party_type: str, name: str) -> dict:
    """Add or update a party for an order. party_type (buyer/seller/lender/attorney) and name required."""
    payload = {"type": party_type, "name": name}
    res = requests.put(f"{BASE_API_URL}/{id}/parties/{party_type}", json=payload)
    return res.json()

@tool("add_or_update_charge")
def add_or_update_charge_tool(id: int, description: str, amount: float) -> dict:
    """Add or update a charge for an order. Description and amount required."""
    payload = {"description": description, "amount": amount}
    res = requests.put(f"{BASE_API_URL}/{id}/charges", json=payload)
    return res.json()

@tool("add_or_update_deposit")
def add_or_update_deposit_tool(id: int, description: str, amount: float) -> dict:
    """Add or update a deposit for an order. Description and amount required."""
    payload = {"description": description, "amount": amount}
    res = requests.put(f"{BASE_API_URL}/{id}/deposits", json=payload)
    return res.json()

@tool("add_or_update_loan")
def add_or_update_loan_tool(id: int, lender: str, amount: float) -> dict:
    """Add or update a loan for an order. Lender and amount required."""
    payload = {"lender": lender, "amount": amount}
    res = requests.put(f"{BASE_API_URL}/{id}/loans", json=payload)
    return res.json()

@tool("add_or_update_fee")
def add_or_update_fee_tool(id: int, description: str, amount: float) -> dict:
    """Add or update a fee for an order. Description and amount required."""
    payload = {"description": description, "amount": amount}
    res = requests.put(f"{BASE_API_URL}/{id}/fees", json=payload)
    return res.json()

@tool("delete_order")
def delete_order_tool(id: int) -> dict:
    """Delete an order by ID."""
    res = requests.delete(f"{BASE_API_URL}/{id}")
    if res.status_code == 204:
        return {"success": True}
    return {"success": False, "error": res.text}

# === AGENT ===
system_prompt = (
    "You are Order Copilot, an AI assistant for order management. "
    "You help users create, update, read, and delete orders using natural language. "
    "If the user request is missing required information, ask for it and persist until all required details are provided. "
    "Once all required information is collected, call the appropriate tool to perform the action. "
    "List your capabilities if the user asks for help or says 'hi'."
)

# === FUNCTION TOOLS ===

@tool("create_order")
def create_order_tool(
    organization: str,
    transaction_type: str,
    parties: List[dict] = None,
    services: List[dict] = None,
    charges: List[dict] = None,
    deposits: List[dict] = None,
    loans: List[dict] = None,
    fees: List[dict] = None
) -> dict:
    """Create a new order. Organization and transaction_type are required. Others are optional lists."""
    payload = {
        "organization": organization,
        "transactionType": transaction_type,
    }
    if parties is not None:
        payload["parties"] = parties
    if services is not None:
        payload["services"] = services
    if charges is not None:
        payload["charges"] = charges
    if deposits is not None:
        payload["deposits"] = deposits
    if loans is not None:
        payload["loans"] = loans
    if fees is not None:
        payload["fees"] = fees
    res = requests.post(BASE_API_URL, json=payload)
    return res.json()

@tool("get_order")
def get_order_tool(id: int) -> dict:
    """Get an order by ID."""
    res = requests.get(f"{BASE_API_URL}/{id}")
    return res.json()

@tool("get_all_orders")
def get_all_orders_tool() -> list:
    """Retrieve all orders."""
    res = requests.get(BASE_API_URL)
    return res.json()

@tool("add_or_update_service")
def add_or_update_service_tool(id: int, type: str) -> dict:
    """Add or update a service for an order. Type is required (e.g., Escrow/Title/Both)."""
    payload = {"type": type}
    res = requests.put(f"{BASE_API_URL}/{id}/services", json=payload)
    return res.json()

@tool("add_or_update_party")
def add_or_update_party_tool(id: int, party_type: str, name: str) -> dict:
    """Add or update a party for an order. party_type (buyer/seller/lender/attorney) and name required."""
    payload = {"type": party_type, "name": name}
    res = requests.put(f"{BASE_API_URL}/{id}/parties/{party_type}", json=payload)
    return res.json()

@tool("add_or_update_charge")
def add_or_update_charge_tool(id: int, description: str, amount: float) -> dict:
    """Add or update a charge for an order. Description and amount required."""
    payload = {"description": description, "amount": amount}
    res = requests.put(f"{BASE_API_URL}/{id}/charges", json=payload)
    return res.json()

@tool("add_or_update_deposit")
def add_or_update_deposit_tool(id: int, description: str, amount: float) -> dict:
    """Add or update a deposit for an order. Description and amount required."""
    payload = {"description": description, "amount": amount}
    res = requests.put(f"{BASE_API_URL}/{id}/deposits", json=payload)
    return res.json()

@tool("add_or_update_loan")
def add_or_update_loan_tool(id: int, lender: str, amount: float) -> dict:
    """Add or update a loan for an order. Lender and amount required."""
    payload = {"lender": lender, "amount": amount}
    res = requests.put(f"{BASE_API_URL}/{id}/loans", json=payload)
    return res.json()

@tool("add_or_update_fee")
def add_or_update_fee_tool(id: int, description: str, amount: float) -> dict:
    """Add or update a fee for an order. Description and amount required."""
    payload = {"description": description, "amount": amount}
    res = requests.put(f"{BASE_API_URL}/{id}/fees", json=payload)
    return res.json()

@tool("delete_order")
def delete_order_tool(id: int) -> dict:
    """Delete an order by ID."""
    res = requests.delete(f"{BASE_API_URL}/{id}")
    if res.status_code == 204:
        return {"success": True}
    return {"success": False, "error": res.text}

# === AGENT ===
llm_with_context = AzureChatOpenAI(
    openai_api_key=AZURE_OPENAI_API_KEY,
    openai_api_base=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT_NAME,
    openai_api_version="2023-05-15",
    temperature=0
)

tools = [
    create_order_tool,
    get_order_tool,
    get_all_orders_tool,
    add_or_update_service_tool,
    add_or_update_party_tool,
    add_or_update_charge_tool,
    add_or_update_deposit_tool,
    add_or_update_loan_tool,
    add_or_update_fee_tool,
    delete_order_tool
]

agent = initialize_agent(
    tools=tools,
    llm=llm_with_context,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# === GRAPH NODES ===
def agent_node(state: OrderState) -> OrderState:
    user_input = state.get("user_input")
    try:
        result = agent.run(user_input)
        print(f"[DEBUG] agent.run result: {result}")
        if isinstance(result, dict) and "id" in result:
            state["last_order_id"] = result["id"]
            state["last_order_data"] = result
        state["output"] = result  # Always set output to the agent result (string or dict)
    except Exception as e:
        print(f"[ERROR] agent.run exception: {e}")
        state["output"] = f"[ERROR] {str(e)}"
    return state

# === BUILD GRAPH ===
graph = StateGraph(OrderState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)
graph_compiled = graph.compile()

# === RUNTIME ===
def ensure_user_input(state_or_str):
    if isinstance(state_or_str, str):
        return {"user_input": state_or_str, **initial_state}
    elif isinstance(state_or_str, dict):
        if "user_input" not in state_or_str and "message" in state_or_str:
            state_or_str["user_input"] = state_or_str["message"]
        return {**initial_state, **state_or_str}
    else:
        raise ValueError("Input must be a string or dict")

if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        final_state = graph_compiled.invoke(ensure_user_input(user_input))
        print("\nAssistant:", final_state["output"])
        initial_state.update(final_state)
