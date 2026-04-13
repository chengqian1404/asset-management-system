# Excel导入导出工具模块
from typing import List, Dict, Any, Optional
from io import BytesIO

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False


def parse_excel_assets(file_content: bytes) -> List[Dict[str, Any]]:
    """
    解析Excel文件中的资产数据
    
    期望的Excel列顺序:
    资产编号, 资产名称, 分类, 位置, 购买日期, 购买价格, 供应商, 备注
    """
    if not EXCEL_AVAILABLE:
        raise RuntimeError("openpyxl未安装，无法处理Excel文件")

    wb = openpyxl.load_workbook(BytesIO(file_content))
    ws = wb.active

    # 读取表头（第一行）
    headers = []
    for cell in ws[1]:
        headers.append(str(cell.value).strip() if cell.value else "")

    # 列名映射（支持中英文列名）
    col_map = {
        "资产编号": "asset_number", "asset_number": "asset_number",
        "资产名称": "name", "name": "name",
        "分类": "category_name", "category": "category_name",
        "位置": "location", "location": "location",
        "购买日期": "purchase_date", "purchase_date": "purchase_date",
        "购买价格": "purchase_price", "purchase_price": "purchase_price",
        "供应商": "supplier", "supplier": "supplier",
        "备注": "description", "description": "description",
    }

    # 解析每一行数据（从第二行开始）
    assets = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):  # 跳过空行
            continue

        asset_data = {}
        for i, value in enumerate(row):
            if i < len(headers) and headers[i] in col_map:
                field = col_map[headers[i]]
                asset_data[field] = str(value).strip() if value is not None else None

        if asset_data.get("asset_number") and asset_data.get("name"):
            assets.append(asset_data)

    return assets


def generate_assets_excel(assets: List[Dict[str, Any]]) -> bytes:
    """生成资产列表Excel文件"""
    if not EXCEL_AVAILABLE:
        raise RuntimeError("openpyxl未安装，无法生成Excel文件")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "资产列表"

    # 设置表头样式
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")

    # 写入表头
    headers = ["资产编号", "资产名称", "分类", "状态", "位置", "负责人", "购买日期", "购买价格", "供应商", "备注"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    # 写入数据
    for row_idx, asset in enumerate(assets, 2):
        ws.cell(row=row_idx, column=1, value=asset.get("asset_number", ""))
        ws.cell(row=row_idx, column=2, value=asset.get("name", ""))
        ws.cell(row=row_idx, column=3, value=asset.get("category", ""))
        ws.cell(row=row_idx, column=4, value=asset.get("status", ""))
        ws.cell(row=row_idx, column=5, value=asset.get("location", ""))
        ws.cell(row=row_idx, column=6, value=asset.get("owner", ""))
        ws.cell(row=row_idx, column=7, value=str(asset.get("purchase_date", "") or ""))
        ws.cell(row=row_idx, column=8, value=float(asset.get("purchase_price", 0) or 0))
        ws.cell(row=row_idx, column=9, value=asset.get("supplier", ""))
        ws.cell(row=row_idx, column=10, value=asset.get("description", ""))

    # 自动调整列宽
    for col in ws.columns:
        max_length = 0
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col[0].column_letter].width = min(max_length + 2, 30)

    # 保存到字节流
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
