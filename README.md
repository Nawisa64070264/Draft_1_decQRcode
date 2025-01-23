# QR code decoratde alredy

Generate Barcode & QR code from text feild on UI.

Type of QR code: Dynamic QR 
Languge: Python, HTML

This is a part of my thesis project. First time using flask that is framework of python

### QR Code Design Specification for the Project  

#### **1. Objective**  
- Minimize database storage and retrieval operations.  
- Maximize the utility of QR codes by embedding essential data directly into them, reducing server dependency.  

---

#### **2. Data to Encode in QR Codes**  
##### **Farmer's QR Code (Raw Milk Tank)**  
- **Tank ID**: Unique identifier for the raw milk tank.  
- **Production Date**: Date of milk collection.  
- **Farmer ID**: Identifier for the farmer.  
- **Destination Factory**: Factory ID or location.  
- **Digital Signature**: To verify the integrity of the QR code data.  

##### **Factory's QR Code (Product Lot)**  
- **Product Lot ID**: Unique identifier for the lot.  
- **Production Date**: Date of product creation.  
- **Expiration Date**: Best before date.  
- **Factory ID**: Identifier for the factory.  
- **Ingredients (optional)**: Key ingredient metadata.  
- **Digital Signature**: To ensure authenticity and prevent tampering.  

##### **Customer's QR Code (Product Information)**  
- **Product Lot ID**: Links to the entire product journey.  
- **Embedded History (Optional)**: Basic journey information (e.g., Farmer ID, Factory ID).  
- **Consumer URL**: Link to a web page showing the detailed journey.  

---

#### **3. QR Code Format**  
- **Type**: QR Code (ISO/IEC 18004:2015).  
- **Error Correction Level**: H (High) – Allows embedding a small logo while maintaining data integrity.  
- **Version**:  
  - Farmer QR Code: Version 3-5 (26x26 to 37x37 cells).  
  - Factory QR Code: Version 5-10 (37x37 to 57x57 cells, depending on lot size).  
  - Customer QR Code: Version 4-6 (33x33 to 41x41 cells).  

---

#### **4. Embedded Data Optimization**  
- Use **compressed formats** (e.g., Base64 or hexadecimal) to minimize QR code size.  
- Use **hashing** or **shortened identifiers** for Tank ID, Product Lot ID, and other unique fields.  
- Embed only **static and non-sensitive data**.  

---

#### **5. Additional Design Elements**  
- **Logo Integration**: Place a small company logo in the center of the QR code.  
- **Color Contrast**: Use high-contrast colors (e.g., black on white) for easy scanning.  
- **Quiet Zone**: Maintain a minimum of 4 units of white space around the QR code.  

---

#### **6. Security Features**  
- **Digital Signatures**: Verify that data hasn’t been tampered with.  
- **Data Encryption**: Encrypt sensitive data (e.g., Farmer ID) using public-key cryptography.  
- **Anti-Counterfeiting Measures**: Embed invisible watermarks or use a unique design pattern.  

---

#### **7. Testing and Validation**  
- Test QR codes on multiple devices and under various conditions (e.g., lighting, angles).  
- Verify data consistency and journey reconstruction from scanned codes.  

Would you like specific examples of QR code data encoding for each actor?

# Step to install:
Command Promt:
1.cd path folders
2.python -m venv venv หรือ python3 -m venv venv
3.venv\Scripts\activate
4.install: pip install Flask qrcode python-barcode 

Run file:
1.ดู (venv) ข้างหน้า
2.python app.py
3.เปิด http://127.0.0.1:5000/
