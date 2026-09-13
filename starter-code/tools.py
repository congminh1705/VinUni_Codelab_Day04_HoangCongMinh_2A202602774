"""Tools backed by the lab's local Vingroup data files."""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "raw-data")


def search_product_catalog(category: str, max_price: int = 999_999_999_999) -> List[Dict[str, Any]]:
    """Return catalog entries matching a category and maximum price."""
    catalog_file = os.path.join(RAW_DATA_DIR, "product_catalog.json")
    if not os.path.exists(catalog_file):
        return [{"error": "Product catalog file not found."}]
    with open(catalog_file, "r", encoding="utf-8") as file:
        products = json.load(file)
    category = category.strip().lower()
    return [product for product in products if product.get("category", "").lower() == category and product.get("price_vnd", float("inf")) <= max_price]


def submit_support_ticket(customer_name: str, issue_description: str, priority: str = "medium") -> Dict[str, Any]:
    """Persist a new support ticket and return its public confirmation."""
    tickets_file = os.path.join(RAW_DATA_DIR, "support_tickets.json")
    existing_tickets: List[Dict[str, Any]] = []
    if os.path.exists(tickets_file):
        with open(tickets_file, "r", encoding="utf-8") as file:
            existing_tickets = json.load(file)
    priority = priority.strip().lower()
    if priority not in {"low", "medium", "high"}:
        priority = "medium"
    now = datetime.now()
    ticket_id = f"TK-{now.strftime('%Y%m%d')}-{len(existing_tickets) + 1:03d}"
    existing_tickets.append({"ticket_id": ticket_id, "customer_name": customer_name,
        "issue_description": issue_description, "priority": priority, "status": "open",
        "created_at": now.isoformat() + "+07:00", "category": "general"})
    with open(tickets_file, "w", encoding="utf-8") as file:
        json.dump(existing_tickets, file, indent=2, ensure_ascii=False)
    return {"ticket_id": ticket_id, "customer_name": customer_name, "priority": priority,
            "status": "open", "message": f"Ticket {ticket_id} đã được tạo thành công."}


TOOL_DEFINITIONS = [
    {"name": "search_product_catalog", "description": "Tra cứu sản phẩm/dịch vụ Vingroup theo danh mục và giá tối đa.", "parameters": {"type": "object", "properties": {"category": {"type": "string", "enum": ["xe_dien", "du_lich"]}, "max_price": {"type": "integer", "description": "Giá tối đa tính bằng VNĐ."}}, "required": ["category"]}},
    {"name": "submit_support_ticket", "description": "Tạo phiếu yêu cầu hỗ trợ cho khách hàng Vingroup.", "parameters": {"type": "object", "properties": {"customer_name": {"type": "string"}, "issue_description": {"type": "string"}, "priority": {"type": "string", "enum": ["low", "medium", "high"]}}, "required": ["customer_name", "issue_description"]}},
]

TOOL_MAP = {"search_product_catalog": search_product_catalog, "submit_support_ticket": submit_support_ticket}
