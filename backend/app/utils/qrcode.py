# 二维码生成工具模块
import io
import base64
from typing import Optional

try:
    import qrcode
    from qrcode.image.pil import PilImage
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


def generate_qr_code(data: str) -> Optional[str]:
    """
    生成二维码并返回Base64编码的PNG图片字符串
    
    参数:
        data: 二维码内容（通常是资产编号或URL）
    
    返回:
        Base64编码的PNG图片字符串，失败时返回None
    """
    if not QR_AVAILABLE:
        return None

    try:
        # 创建二维码对象
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # 生成图片
        img = qr.make_image(fill_color="black", back_color="white")

        # 转换为Base64字符串
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_base64}"
    except Exception:
        return None
