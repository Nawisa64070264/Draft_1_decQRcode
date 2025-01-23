from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
import io
import base64
import json

app = Flask(__name__)

def generate_qrcode_with_style(data):
    background_path = r"C:\Users\Nawisa T\OneDrive\Senior_Project\Try_decorate_barcode(2)\static\images\Background.png"  # แก้ไข path ให้ถูกต้อง
    font_path = r"C:\Users\Nawisa T\OneDrive\Senior_Project\Try_decorate_barcode(2)\static\fonts\ARLRDBD.TTF"  # หรือ path ของ font ที่คุณต้องการ

    try:
        background = Image.open(background_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Background image not found at {background_path}")
        return None

    max_width = 350
    if background.width > max_width:
        new_width = max_width
        new_height = int(background.height * (new_width / background.width))
        background = background.resize((new_width, new_height), Image.Resampling.LANCZOS)
    canvas_width, canvas_height = background.size

    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color=(255, 255, 255, 0)).convert("RGBA")

    frame_width = 350  # ค่าโดยประมาณ โปรดแก้ไขตามขนาดจริงของกรอบสีขาว
    frame_height = 250 # ค่าโดยประมาณ โปรดแก้ไขตามขนาดจริงของกรอบสีขาว

    qr_width = int(min(frame_width, frame_height) * 0.8)
    qr_img = qr_img.resize((qr_width, qr_width), Image.Resampling.LANCZOS)

    frame_x = int((canvas_width - frame_width) // 2)
    frame_y = int((canvas_height - frame_height) // 2)

    # *** ปรับตำแหน่ง QR Code ตรงนี้ ***
    qr_y = int(frame_y + (frame_height - qr_width) // 0.68) # วางตรงกลางแนวตั้งของกรอบ
    qr_x = int(frame_x + (frame_width - qr_width) // 1.63)
    background.paste(qr_img, (qr_x, qr_y), qr_img)

    draw = ImageDraw.Draw(background)
    font_top = ImageFont.truetype(font_path, 24)

    top_text = "Purely Trace\nSt.\n65"
    top_bbox = draw.multiline_textbbox((0, 0), top_text, font=font_top, align="center") # เพิ่ม align="center"
    top_width, top_height = top_bbox[2] - top_bbox[0], top_bbox[3] - top_bbox[1]

    # คำนวณตำแหน่งกึ่งกลางแนวนอน
    center_x = canvas_width // 2
    # คำนวณตำแหน่งกึ่งกลางแนวตั้ง (เหนือกรอบ)
    top_center_y = frame_y - top_height // 2 - 10 # -10 คือระยะห่างจากขอบกรอบ

    # คำนวณตำแหน่งเริ่มต้นของข้อความ
    top_x = center_x - top_width // 2
    top_y = top_center_y - top_height // 0.5

    # วาดข้อความหลายบรรทัด โดยจัดกึ่งกลาง
    draw.multiline_text((top_x, top_y), top_text, fill="black", font=font_top, align="center", spacing=5) # เพิ่ม spacing

  
    bottom_text = "Treat\nme\nwith\ncare"
    bottom_font = ImageFont.truetype(font_path, 18)
    bottom_bbox = draw.multiline_textbbox((0, 0), bottom_text, font=bottom_font, align="center")
    bottom_width, bottom_height = bottom_bbox[2] - bottom_bbox[0], bottom_bbox[3] - bottom_bbox[1]

    # *** ปรับตำแหน่งข้อความ "Treat me with care" ตรงนี้ ***
    bottom_position = (int((canvas_width - bottom_width) // 2), int(frame_y + frame_height + 70)) # เว้นระยะห่าง 30px จากขอบล่างของกรอบ

    draw.multiline_text(bottom_position, bottom_text, fill="black", font=bottom_font, align="center", spacing=10)

    buffer = io.BytesIO()
    background.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def handle_qrcode_generation(form_data, keys):
    data_string = json.dumps(form_data)
    qrcode_image = generate_qrcode_with_style(data_string)
    return qrcode_image

# เส้นทางสำหรับ QR Code ของเกษตรกร
@app.route('/qrcode/farmer', methods=['GET', 'POST'])
def qrcode_farmer():
    if request.method == 'POST':
        try:
            form_data = {
                "tank_id": request.form.get('tank_id'),
                "production_date": request.form.get('production_date'),
                "farmer_id": request.form.get('farmer_id'),
                "destination_factory": request.form.get('destination_factory'),
                "signature": "dummy_signature"
            }
            qrcode_image = handle_qrcode_generation(form_data, form_data.keys())
            return render_template('qrcode_farmer.html', qrcode_image=qrcode_image)
        except Exception as e:
            return render_template('qrcode_farmer.html', error_message=f"เกิดข้อผิดพลาด: {e}")
    return render_template('qrcode_farmer.html')

# เส้นทางสำหรับ QR Code ของโรงงาน
@app.route('/qrcode/factory', methods=['GET', 'POST'])
def qrcode_factory():
    if request.method == 'POST':
        try:
            form_data = {
                "lot_id": request.form.get('lot_id'),
                "production_date": request.form.get('production_date'),
                "expiration_date": request.form.get('expiration_date'),
                "factory_id": request.form.get('factory_id'),
                "signature": "dummy_signature"
            }
            qrcode_image = handle_qrcode_generation(form_data, form_data.keys())
            return render_template('qrcode_factory.html', qrcode_image=qrcode_image)
        except Exception as e:
            return render_template('qrcode_factory.html', error_message=f"เกิดข้อผิดพลาด: {e}")
    return render_template('qrcode_factory.html')

# เส้นทางสำหรับ QR Code ของลูกค้า
@app.route('/qrcode/customer', methods=['GET', 'POST'])
def qrcode_customer():
    if request.method == 'POST':
        try:
            form_data = {
                "lot_id": request.form.get('lot_id'),
                "product_name": request.form.get('product_name'),
                "url": request.form.get('url')
            }
            qrcode_image = handle_qrcode_generation(form_data, form_data.keys())
            return render_template('qrcode_customer.html', qrcode_image=qrcode_image)
        except Exception as e:
            return render_template('qrcode_customer.html', error_message=f"เกิดข้อผิดพลาด: {e}")
    return render_template('qrcode_customer.html')

# เส้นทางหน้าหลัก
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
