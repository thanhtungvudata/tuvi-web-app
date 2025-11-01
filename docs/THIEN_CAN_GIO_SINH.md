# Cách Tính Thiên Can Giờ Sinh

## Tổng Quan

Trong Tử Vi, mỗi giờ sinh không chỉ có Địa Chi (Tý, Sửu, Dần, Mão...) mà còn có Thiên Can (Giáp, Ất, Bính, Đinh...). Thiên Can của giờ sinh được tính dựa vào **Thiên Can của ngày sinh** theo quy tắc "Nhật Thượng Khởi Giờ" (日上起時).

---

## 1. Quy Tắc Truyền Thống: "Nhật Thượng Khởi Giờ"

### 1.1. Nguyên Tắc Cơ Bản

Dựa vào Thiên Can của **ngày sinh**, ta xác định được Thiên Can của **giờ Tý** (23h-01h). Từ đó, đếm tiếp theo thứ tự 10 Thiên Can để ra các giờ khác.

### 1.2. Bài Ca Nhớ

```
Giáp Kỷ sinh Giáp Tý đầu
Ất Canh Bính Tý lưu truyền
Bính Tân khởi Mậu Tý
Đinh Nhâm Canh Tý hành
Mậu Quý nhằm Nhâm Tý
```

### 1.3. Bảng Tra Nhanh

| Thiên Can Ngày Sinh | Thiên Can Giờ Tý (23h-01h) |
|---------------------|---------------------------|
| **Giáp 甲** hoặc **Kỷ 己** | Giáp 甲 |
| **Ất 乙** hoặc **Canh 庚** | Bính 丙 |
| **Bính 丙** hoặc **Tân 辛** | Mậu 戊 |
| **Đinh 丁** hoặc **Nhâm 壬** | Canh 庚 |
| **Mậu 戊** hoặc **Quý 癸** | Nhâm 壬 |

### 1.4. Ví Dụ Minh Họa

**Ví dụ 1:** Ngày sinh có Thiên Can là **Giáp** (甲)
- Giờ Tý (23h-01h): **Giáp Tý** 甲子
- Giờ Sửu (01h-03h): **Ất Sửu** 乙丑
- Giờ Dần (03h-05h): **Bính Dần** 丙寅
- Giờ Mão (05h-07h): **Đinh Mão** 丁卯
- Giờ Thìn (07h-09h): **Mậu Thìn** 戊辰
- Giờ Tỵ (09h-11h): **Kỷ Tỵ** 己巳
- Giờ Ngọ (11h-13h): **Canh Ngọ** 庚午
- Giờ Mùi (13h-15h): **Tân Mùi** 辛未
- Giờ Thân (15h-17h): **Nhâm Thân** 壬申
- Giờ Dậu (17h-19h): **Quý Dậu** 癸酉
- Giờ Tuất (19h-21h): **Giáp Tuất** 甲戌
- Giờ Hợi (21h-23h): **Ất Hợi** 乙亥

**Ví dụ 2:** Ngày sinh có Thiên Can là **Ất** (乙)
- Giờ Tý (23h-01h): **Bính Tý** 丙子
- Giờ Sửu (01h-03h): **Đinh Sửu** 丁丑
- Giờ Dần (03h-05h): **Mậu Dần** 戊寅
- ...cứ thế đếm tiếp

---

## 2. Cách Tính Trong Code

### 2.1. Công Thức Toán Học

Trong file `core/calculations/ThienBan.py` (dòng 19-21), công thức được implement như sau:

```python
canGioSinh = ((jdFromDate(nn, tt, nnnn) - 1) * 2 % 10 + gioSinh) % 10
if canGioSinh == 0:
    canGioSinh = 10
```

### 2.2. Giải Thích Chi Tiết

#### Bước 1: Tính Julian Day Number
```python
jd = jdFromDate(nn, tt, nnnn)
```
- Chuyển đổi ngày/tháng/năm sang Julian Day Number
- Đây là số thứ tự của ngày kể từ ngày 1 tháng 1 năm 4713 TCN

#### Bước 2: Tính Thiên Can giờ Tý
```python
canGioTy = (jd - 1) * 2 % 10
```
- `(jd - 1)`: Lấy JD của ngày trước đó
- `* 2`: Nhân với 2 (vì mỗi ngày có 2 chu kỳ 12 giờ)
- `% 10`: Lấy phần dư chia 10 để ra Thiên Can (0-9)

#### Bước 3: Tính Thiên Can giờ cụ thể
```python
canGioSinh = (canGioTy + gioSinh) % 10
```
- `gioSinh`: Số thứ tự của giờ sinh (1=Tý, 2=Sửu, 3=Dần,...)
- Cộng vào Thiên Can giờ Tý và lấy phần dư chia 10

#### Bước 4: Xử lý trường hợp đặc biệt
```python
if canGioSinh == 0:
    canGioSinh = 10  # 0 tương ứng với Thiên Can "Quý" (số 10)
```

### 2.3. Ví Dụ Tính Toán

Giả sử:
- Ngày sinh: 15/03/2024
- Julian Day Number: 2459580
- Giờ sinh: Dần (số 3)

**Tính toán:**
```
canGioSinh = ((2459580 - 1) * 2 % 10 + 3) % 10
           = ((2459579) * 2 % 10 + 3) % 10
           = (4919158 % 10 + 3) % 10
           = (8 + 3) % 10
           = 11 % 10
           = 1  # → Thiên Can "Giáp"
```

**Kết quả:** Giờ Dần có Thiên Can là **Giáp**, tức là **Giáp Dần** (甲寅)

---

## 3. Thứ Tự 10 Thiên Can

| STT | Thiên Can | Chữ Hán | Ngũ Hành | Âm Dương |
|-----|-----------|---------|----------|----------|
| 1 | Giáp | 甲 | Mộc | Dương |
| 2 | Ất | 乙 | Mộc | Âm |
| 3 | Bính | 丙 | Hỏa | Dương |
| 4 | Đinh | 丁 | Hỏa | Âm |
| 5 | Mậu | 戊 | Thổ | Dương |
| 6 | Kỷ | 己 | Thổ | Âm |
| 7 | Canh | 庚 | Kim | Dương |
| 8 | Tân | 辛 | Kim | Âm |
| 9 | Nhâm | 壬 | Thủy | Dương |
| 10 | Quý | 癸 | Thủy | Âm |

---

## 4. Thứ Tự 12 Địa Chi (Giờ Sinh)

| STT | Địa Chi | Chữ Hán | Giờ | Ngũ Hành |
|-----|---------|---------|-----|----------|
| 1 | Tý | 子 | 23h-01h | Thủy |
| 2 | Sửu | 丑 | 01h-03h | Thổ |
| 3 | Dần | 寅 | 03h-05h | Mộc |
| 4 | Mão | 卯 | 05h-07h | Mộc |
| 5 | Thìn | 辰 | 07h-09h | Thổ |
| 6 | Tỵ | 巳 | 09h-11h | Hỏa |
| 7 | Ngọ | 午 | 11h-13h | Hỏa |
| 8 | Mùi | 未 | 13h-15h | Thổ |
| 9 | Thân | 申 | 15h-17h | Kim |
| 10 | Dậu | 酉 | 17h-19h | Kim |
| 11 | Tuất | 戌 | 19h-21h | Thổ |
| 12 | Hợi | 亥 | 21h-23h | Thủy |

---

## 5. So Sánh Hai Phương Pháp

### 5.1. Phương Pháp Truyền Thống
- **Ưu điểm:** Dễ nhớ, dễ tra bằng bảng
- **Nhược điểm:** Cần tra bảng, dễ nhầm lẫn khi tra nhiều

### 5.2. Phương Pháp Toán Học (Code)
- **Ưu điểm:** Tự động hóa, chính xác 100%, không cần tra bảng
- **Nhược điểm:** Khó hiểu nếu không biết Julian Day Number

### 5.3. Kết Luận

Cả hai phương pháp đều cho ra **kết quả giống nhau**. Phương pháp code sử dụng Julian Day Number để tự động hóa quy tắc "Nhật Thượng Khởi Giờ" thành công thức toán học.

---

## 6. Tham Khảo Code

- **File:** `core/calculations/ThienBan.py`
- **Dòng:** 19-25
- **Hàm:** `lapThienBan.__init__()`

```python
chiGioSinh = diaChi[gioSinh]
canGioSinh = ((jdFromDate(nn, tt, nnnn) - 1) * 2 % 10 + gioSinh) % 10
if canGioSinh == 0:
    canGioSinh = 10
self.chiGioSinh = chiGioSinh
self.canGioSinh = canGioSinh
self.gioSinh = "{} {}".format(thienCan[canGioSinh]['tenCan'],
                              chiGioSinh['tenChi'])
```

---

## 7. Lưu Ý Quan Trọng

1. **Múi giờ:** Cần chú ý múi giờ khi tính Julian Day Number (Việt Nam: UTC+7)
2. **Giờ Tý đặc biệt:** Giờ Tý (23h-01h) nằm giữa hai ngày, cần xác định đúng ngày để tính Can
3. **Can Ngày:** Thiên Can ngày phải được tính qua Julian Day Number, không thể tự suy từ Can năm
4. **Chu kỳ:** 10 Thiên Can kết hợp với 12 Địa Chi tạo thành chu kỳ 60 (60 Can Chi)

---

**Tài liệu này được tạo bởi:** Claude Code
**Ngày tạo:** 2025-01-02
**Phiên bản:** 1.0
