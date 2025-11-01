# -*- coding: utf-8 -*-
"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""

from core.calculations.AmDuong import diaChi, thienCan, dichCung, khoangCachCung


class cungDiaBan(object):
    """docstring for cungDiaBan"""
    def __init__(self, cungID):
        # super(cungDiaBan, self).__init__()
        hanhCung = [None, "Thủy", "Thổ", "Mộc", "Mộc", "Thổ", "Hỏa",
                    "Hỏa", "Thổ", "Kim", "Kim", "Thổ", "Thủy"]
        self.cungSo = cungID
        self.hanhCung = hanhCung[cungID]
        self.cungSao = []
        self.cungAmDuong = -1 if (self.cungSo % 2 == 0) else 1
        self.cungTen = diaChi[self.cungSo]['tenChi']
        self.cungCan = None  # NOTE: Will be set by nhapCanCung() method
        self.cungThan = False

    def themSao(self, sao):
        dacTinhSao(self.cungSo, sao)
        self.cungSao.append(sao.__dict__)
        return self

    def cungChu(self, tenCungChu):
        self.cungChu = tenCungChu
        return self

    def daiHan(self, daiHan):
        self.cungDaiHan = daiHan
        return self

    def tieuHan(self, tieuHan):
        self.cungTieuHan = diaChi[tieuHan + 1]['tenChi']
        return self

    def anCungThan(self):
        self.cungThan = True

    def anTuan(self):
        self.tuanTrung = True

    def anTriet(self):
        self.trietLo = True

    def cungDaiVan(self, tenCungDaiVan):
        """Assign Đại Vận palace name to this palace."""
        self.cungDaiVan = tenCungDaiVan
        return self

    def cungTieuVan(self, tenCungTieuVan):
        """Assign Tiểu Vận palace name to this palace."""
        self.cungTieuVan = tenCungTieuVan
        return self


class diaBan(object):
    def __init__(self, thangSinhAmLich, gioSinhAmLich):
        super(diaBan, self).__init__()
        self.thangSinhAmLich = thangSinhAmLich
        self.gioSinhAmLich = gioSinhAmLich
        self.thapNhiCung = [cungDiaBan(i) for i in range(13)]
        self.nhapCungChu()
        self.nhapCungThan()

    def cungChu(self, thangSinhAmLich, gioSinhAmLich):
        self.cungThan = dichCung(3, thangSinhAmLich - 1, gioSinhAmLich - 1)
        self.cungMenh = dichCung(3, thangSinhAmLich - 1, - (gioSinhAmLich) + 1)
        cungPhuMau = dichCung(self.cungMenh, 1)
        cungPhucDuc = dichCung(self.cungMenh, 2)
        cungDienTrach = dichCung(self.cungMenh, 3)
        cungQuanLoc = dichCung(self.cungMenh, 4)
        self.cungNoboc = dichCung(self.cungMenh, 5)  # Để an sao Thiên thương
        cungThienDi = dichCung(self.cungMenh, 6)
        self.cungTatAch = dichCung(self.cungMenh, 7)  # an sao Thiên sứ
        cungTaiBach = dichCung(self.cungMenh, 8)
        cungTuTuc = dichCung(self.cungMenh, 9)
        cungTheThiep = dichCung(self.cungMenh, 10)
        cungHuynhDe = dichCung(self.cungMenh, 11)

        cungChuThapNhiCung = [
            {
                'cungId': 1,
                'tenCung': "Mệnh",
                'cungSoDiaBan': self.cungMenh
            },
            {
                'cungId': 2,
                'tenCung': "Phụ mẫu",
                'cungSoDiaBan': cungPhuMau

            },
            {
                'cungId': 3,
                'tenCung': "Phúc đức",
                'cungSoDiaBan': cungPhucDuc

            },
            {
                'cungId': 4,
                'tenCung': "Điền trạch",
                'cungSoDiaBan': cungDienTrach

            },
            {
                'cungId': 5,
                'tenCung': "Quan lộc",
                'cungSoDiaBan': cungQuanLoc

            },
            {
                'cungId': 6,
                'tenCung': "Nô bộc",
                'cungSoDiaBan': self.cungNoboc

            },
            {
                'cungId': 7,
                'tenCung': "Thiên di",
                'cungSoDiaBan': cungThienDi

            },
            {
                'cungId': 8,
                'tenCung': "Tật Ách",
                'cungSoDiaBan': self.cungTatAch

            },
            {
                'cungId': 9,
                'tenCung': "Tài Bạch",
                'cungSoDiaBan': cungTaiBach

            },
            {
                'cungId': 10,
                'tenCung': "Tử tức",
                'cungSoDiaBan': cungTuTuc

            },
            {
                'cungId': 11,
                'tenCung': "Phu thê",
                'cungSoDiaBan': cungTheThiep

            },
            {
                'cungId': 12,
                'tenCung': "Huynh đệ",
                'cungSoDiaBan': cungHuynhDe

            }
        ]
        return cungChuThapNhiCung

    def nhapCungChu(self):
        for cung in self.cungChu(self.thangSinhAmLich, self.gioSinhAmLich):
            self.thapNhiCung[cung['cungSoDiaBan']].cungChu(cung['tenCung'])
        return self

    def nhapDaiHan(self, cucSo, gioiTinh):
        """Nhap dai han

        Args:
            cucSo (TYPE): Description
            gioiTinh (TYPE): Description

        Returns:
            TYPE: Description
        """
        for cung in self.thapNhiCung:
            khoangCach = khoangCachCung(cung.cungSo, self.cungMenh, gioiTinh)
            cung.daiHan(cucSo + khoangCach * 10)
        return self

    def nhapTieuHan(self, khoiTieuHan, gioiTinh, chiNam):
        # Vị trí khởi tiểu Hạn là của năm sinh theo chi
        # vì vậy cần phải tìm vị trí cung Tý của năm đó
        viTriCungTy1 = dichCung(khoiTieuHan, -gioiTinh * (chiNam - 1))

        # Tiếp đó là nhập hạn
        for cung in self.thapNhiCung:
            khoangCach = khoangCachCung(cung.cungSo, viTriCungTy1, gioiTinh)
            cung.tieuHan(khoangCach)
        return self

    def nhapCungDaiVan(self, tuoiAmLich):
        """
        Nhập cung Đại Vận dựa trên tuổi âm lịch.

        Logic: Tìm cung có Đại Hạn thỏa mãn điều kiện:
        tuoiAmLich >= cungDaiHan AND tuoiAmLich < cungDaiHan kế tiếp

        Sau đó an 12 cung đại vận theo chiều kim đồng hồ (thuận):
        Mệnh, Phụ mẫu, Phúc đức, Điền trạch, Quan lộc, Nô bộc,
        Thiên di, Tật Ách, Tài Bạch, Tử tức, Phu thê, Huynh đệ

        Args:
            tuoiAmLich (int): Tuổi âm lịch hiện tại

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Palace names in clockwise order with ".ĐV" suffix, all uppercase
        cungDaiVanNames = [
            "MỆNH.ĐV", "PHỤ MẪU.ĐV", "PHÚC ĐỨC.ĐV", "ĐIỀN TRẠCH.ĐV",
            "QUAN LỘC.ĐV", "NÔ BỘC.ĐV", "THIÊN DI.ĐV", "TẬT ÁCH.ĐV",
            "TÀI BẠCH.ĐV", "TỬ TỨC.ĐV", "PHU THÊ.ĐV", "HUYNH ĐỆ.ĐV"
        ]

        # NOTE: Find the palace where current age falls within Đại Hạn range
        # Each Đại Hạn period is 10 years: age from X to X+9 belongs to Đại Hạn X
        # Example: age 36 belongs to Đại Hạn 35 (covers ages 35-44)
        cungDaiVanStart = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue

            # Check if current age falls in this palace's Đại Hạn range
            # Age X belongs to Đại Hạn Y if Y <= X < Y+10
            if cung.cungDaiHan <= tuoiAmLich < cung.cungDaiHan + 10:
                cungDaiVanStart = cung.cungSo
                break

        # NOTE: If no match found (edge case for very old age), use last palace
        if cungDaiVanStart is None:
            # Find palace with highest Đại Hạn
            maxDaiHan = max(c.cungDaiHan for c in self.thapNhiCung if c.cungSo != 0)
            for cung in self.thapNhiCung:
                if cung.cungSo != 0 and cung.cungDaiHan == maxDaiHan:
                    cungDaiVanStart = cung.cungSo
                    break

        # NOTE: Assign Đại Vận palace names clockwise starting from cungDaiVanStart
        for i in range(12):
            # Calculate target palace number (clockwise = +1 direction)
            targetCungSo = dichCung(cungDaiVanStart, i)
            self.thapNhiCung[targetCungSo].cungDaiVan(cungDaiVanNames[i])

        return self

    def nhapCungTieuVan(self, chiNamXem):
        """
        Nhập cung Tiểu Vận dựa trên địa chi của năm xem.

        Logic: Tìm cung có địa chi trùng với địa chi của năm xem, an Mệnh Tiểu Vận ở cung đó.
        Sau đó an 12 cung tiểu vận theo chiều kim đồng hồ (thuận):
        Mệnh, Phụ mẫu, Phúc đức, Điền trạch, Quan lộc, Nô bộc,
        Thiên di, Tật Ách, Tài Bạch, Tử tức, Phu thê, Huynh đệ

        Args:
            chiNamXem (int): Địa chi của năm xem (1-12)

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Palace names in clockwise order with ".TV" suffix, all uppercase
        cungTieuVanNames = [
            "MỆNH.TV", "PHỤ MẪU.TV", "PHÚC ĐỨC.TV", "ĐIỀN TRẠCH.TV",
            "QUAN LỘC.TV", "NÔ BỘC.TV", "THIÊN DI.TV", "TẬT ÁCH.TV",
            "TÀI BẠCH.TV", "TỬ TỨC.TV", "PHU THÊ.TV", "HUYNH ĐỆ.TV"
        ]

        # NOTE: Find the palace with matching địa chi (cungSo corresponds to địa chi)
        # Each cungSo represents a địa chi: 1=Tý, 2=Sửu, 3=Dần, ..., 12=Hợi
        cungTieuVanStart = chiNamXem

        # NOTE: Assign Tiểu Vận palace names clockwise starting from cungTieuVanStart
        for i in range(12):
            # Calculate target palace number (clockwise = +1 direction)
            targetCungSo = dichCung(cungTieuVanStart, i)
            self.thapNhiCung[targetCungSo].cungTieuVan(cungTieuVanNames[i])

        return self

    def nhapCanCung(self, canNamSinh):
        """
        Tính và gán Thiên Can cho 12 cung dựa trên Can năm sinh.

        Theo trường phái: Can của cung = Can của tháng tương ứng với vị trí cung.

        Logic:
        - Can tháng Giêng = (canNamSinh * 2 + 1) % 10
        - Can cung = ((viTriCung - 3) % 12 + canThangGieng) % 10
        - Vị trí 3 = Dần = Tháng Giêng (tháng 1)

        Args:
            canNamSinh (int): Can của năm sinh (1-10)

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Calculate Can of Giêng (first lunar month)
        canThangGieng = (canNamSinh * 2 + 1) % 10

        # NOTE: Calculate and assign Can for each of 12 palaces
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue

            # Calculate Can for this palace
            canCung = ((cung.cungSo - 3) % 12 + canThangGieng) % 10
            if canCung == 0:
                canCung = 10

            # Assign Can name to palace
            cung.cungCan = thienCan[canCung]['tenCan']

        return self

    def nhapSaoLuuLocTonDaiVan(self):
        """
        Tính và gán sao Lưu Lộc Tồn Đại Vận dựa trên Thiên Can của cung Mệnh.ĐV.

        Logic:
        1. Tìm cung có cungDaiVan = "MỆNH.ĐV"
        2. Lấy Thiên Can của cung đó (cungCan)
        3. Tra vị trí Lộc Tồn từ thienCan[canID]['vitriDiaBan']
        4. Đặt sao Lộc tồn.ĐV vào cung đó

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import sao definition and thienCan lookup table
        from core.calculations.Sao import saoLuuLocTonDaiVan

        # NOTE: Find palace with "MỆNH.ĐV"
        cungMenhDaiVan = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            if hasattr(cung, 'cungDaiVan') and cung.cungDaiVan == "MỆNH.ĐV":
                cungMenhDaiVan = cung
                break

        # NOTE: If no Mệnh.ĐV found or no Can assigned, skip
        if cungMenhDaiVan is None or cungMenhDaiVan.cungCan is None:
            return self

        # NOTE: Map Can name to Can ID
        canID = None
        for i, canData in enumerate(thienCan):
            if canData['tenCan'] == cungMenhDaiVan.cungCan:
                canID = i
                break

        # NOTE: If Can not found in lookup table, skip
        if canID is None or canID == 0:
            return self

        # NOTE: Get Lộc Tồn position from thienCan lookup table
        viTriLuuLocTonDaiVan = thienCan[canID]['vitriDiaBan']

        # NOTE: Place Lộc tồn.ĐV star at calculated position
        self.nhapSao(viTriLuuLocTonDaiVan, saoLuuLocTonDaiVan)

        return self

    def nhapSaoLuuLocTonTieuVan(self, canNamXem):
        """
        Tính và gán sao Lưu Lộc Tồn Tiểu Vận dựa trên Thiên Can của năm xem.

        Logic:
        1. Lấy Thiên Can của năm xem (canNamXem)
        2. Tra vị trí Lộc Tồn từ thienCan[canNamXem]['vitriDiaBan']
        3. Đặt sao Lộc tồn.TV vào cung đó

        Args:
            canNamXem (int): Can của năm xem (1-10)

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import sao definition
        from core.calculations.Sao import saoLuuLocTonTieuVan

        # NOTE: Validate canNamXem
        if canNamXem is None or canNamXem == 0:
            return self

        # NOTE: Get Lộc Tồn position from thienCan lookup table
        viTriLuuLocTonTieuVan = thienCan[canNamXem]['vitriDiaBan']

        # NOTE: Place Lộc tồn.TV star at calculated position
        self.nhapSao(viTriLuuLocTonTieuVan, saoLuuLocTonTieuVan)

        return self

    def nhapSaoLuuKinhDuongDaLaDaiVan(self):
        """
        Tính và gán sao Lưu Kình Dương và Lưu Đà La Đại Vận dựa trên vị trí Lộc Tồn.ĐV.

        Logic:
        1. Tìm cung chứa sao "Lộc tồn.ĐV"
        2. Đà la.ĐV = vị trí Lộc tồn.ĐV - 1 cung (ngược chiều)
        3. Kình dương.ĐV = vị trí Lộc tồn.ĐV + 1 cung (thuận chiều)

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import star definitions and helper function
        from core.calculations.Sao import saoLuuKinhDuongDaiVan, saoLuuDaLaDaiVan
        from core.calculations.AmDuong import dichCung

        # NOTE: Find palace containing Lộc tồn.ĐV star
        viTriLuuLocTonDaiVan = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            # Check if this palace has Lộc tồn.ĐV star
            for sao in cung.cungSao:
                # NOTE: sao is already a dict (converted in themSao method)
                sao_ten = sao.get('saoTen') if isinstance(sao, dict) else sao.saoTen
                if sao_ten == "Lộc tồn.ĐV":
                    viTriLuuLocTonDaiVan = cung.cungSo
                    break
            if viTriLuuLocTonDaiVan is not None:
                break

        # NOTE: If Lộc tồn.ĐV not found, return without placing stars
        if viTriLuuLocTonDaiVan is None:
            return self

        # NOTE: Calculate positions based on Lộc tồn.ĐV
        # Đà la.ĐV is 1 palace backward (counter-clockwise)
        viTriLuuDaLaDaiVan = dichCung(viTriLuuLocTonDaiVan, -1)
        self.nhapSao(viTriLuuDaLaDaiVan, saoLuuDaLaDaiVan)

        # Kình dương.ĐV is 1 palace forward (clockwise)
        viTriLuuKinhDuongDaiVan = dichCung(viTriLuuLocTonDaiVan, 1)
        self.nhapSao(viTriLuuKinhDuongDaiVan, saoLuuKinhDuongDaiVan)

        return self

    def nhapSaoLuuKinhDuongDaLaTieuVan(self):
        """
        Place Kình Dương.TV and Đà La.TV stars based on Lộc tồn.TV position.

        Kình Dương.TV (Tiểu Vận) is placed 1 palace forward (clockwise) from Lộc tồn.TV.
        Đà La.TV (Tiểu Vận) is placed 1 palace backward (counter-clockwise) from Lộc tồn.TV.

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import star definitions and helper function
        from core.calculations.Sao import saoLuuKinhDuongTieuVan, saoLuuDaLaTieuVan
        from core.calculations.AmDuong import dichCung

        # NOTE: Find palace containing Lộc tồn.TV star
        viTriLuuLocTonTieuVan = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            # Check if this palace has Lộc tồn.TV star
            for sao in cung.cungSao:
                # NOTE: sao is already a dict (converted in themSao method)
                sao_ten = sao.get('saoTen') if isinstance(sao, dict) else sao.saoTen
                if sao_ten == "Lộc tồn.TV":
                    viTriLuuLocTonTieuVan = cung.cungSo
                    break
            if viTriLuuLocTonTieuVan is not None:
                break

        # NOTE: If Lộc tồn.TV not found, return without placing stars
        if viTriLuuLocTonTieuVan is None:
            return self

        # NOTE: Calculate positions based on Lộc tồn.TV
        # Đà la.TV is 1 palace backward (counter-clockwise)
        viTriLuuDaLaTieuVan = dichCung(viTriLuuLocTonTieuVan, -1)
        self.nhapSao(viTriLuuDaLaTieuVan, saoLuuDaLaTieuVan)

        # Kình dương.TV is 1 palace forward (clockwise)
        viTriLuuKinhDuongTieuVan = dichCung(viTriLuuLocTonTieuVan, 1)
        self.nhapSao(viTriLuuKinhDuongTieuVan, saoLuuKinhDuongTieuVan)

        return self

    def nhapSaoTuHoaLuuDaiVan(self):
        """
        Tính và gán Tứ Hóa Lưu Đại Vận dựa trên Thiên Can của cung Mệnh.ĐV.

        Logic:
        1. Tìm cung có cungDaiVan = "MỆNH.ĐV"
        2. Lấy Thiên Can của cung đó (cungCan)
        3. Dựa vào Thiên Can, tra bảng Tứ Hóa để tìm vị trí các sao Chính tinh
        4. Đặt 4 sao Hóa lộc.ĐV, Hóa quyền.ĐV, Hóa khoa.ĐV, Hóa kỵ.ĐV
           vào vị trí các sao Chính tinh tương ứng

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import star definitions
        from core.calculations.Sao import (
            saoLuuHoaLocDaiVan, saoLuuHoaQuyenDaiVan,
            saoLuuHoaKhoaDaiVan, saoLuuHoaKyDaiVan
        )

        # NOTE: Find palace with "MỆNH.ĐV"
        cungMenhDaiVan = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            if hasattr(cung, 'cungDaiVan') and cung.cungDaiVan == "MỆNH.ĐV":
                cungMenhDaiVan = cung
                break

        # NOTE: If no Mệnh.ĐV found or no Can assigned, skip
        if cungMenhDaiVan is None or cungMenhDaiVan.cungCan is None:
            return self

        # NOTE: Map Can name to Can ID
        canID = None
        for i, canData in enumerate(thienCan):
            if canData['tenCan'] == cungMenhDaiVan.cungCan:
                canID = i
                break

        # NOTE: If Can not found in lookup table, skip
        if canID is None or canID == 0:
            return self

        # NOTE: Find positions of major stars (Chính tinh) to apply Tứ Hóa
        # Build a map of star names to their palace positions
        viTriSaoChinhTinh = {}
        chinhTinhNames = [
            "Tử vi", "Liêm trinh", "Thiên đồng", "Vũ khúc", "Thái Dương",
            "Thiên cơ", "Thiên phủ", "Thái âm", "Tham lang", "Cự môn",
            "Thiên tướng", "Thiên lương", "Thất sát", "Phá quân",
            "Văn xương", "Văn Khúc"
        ]

        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            for sao in cung.cungSao:
                sao_ten = sao.get('saoTen') if isinstance(sao, dict) else sao.saoTen
                if sao_ten in chinhTinhNames:
                    viTriSaoChinhTinh[sao_ten] = cung.cungSo

        # NOTE: Tứ Hóa table based on Thiên Can (same as in App.py)
        tuHoaTable = {
            1: {"loc": "Liêm trinh", "quyen": "Phá quân", "khoa": "Vũ khúc", "ky": "Thái Dương"},
            2: {"loc": "Thiên cơ", "quyen": "Thiên lương", "khoa": "Tử vi", "ky": "Thái âm"},
            3: {"loc": "Thiên đồng", "quyen": "Thiên cơ", "khoa": "Văn xương", "ky": "Liêm trinh"},
            4: {"loc": "Thái âm", "quyen": "Thiên đồng", "khoa": "Thiên cơ", "ky": "Cự môn"},
            5: {"loc": "Tham lang", "quyen": "Thái âm", "khoa": "Thái Dương", "ky": "Thiên cơ"},
            6: {"loc": "Vũ khúc", "quyen": "Tham lang", "khoa": "Thiên lương", "ky": "Văn Khúc"},
            7: {"loc": "Thái Dương", "quyen": "Vũ khúc", "khoa": "Thái âm", "ky": "Thiên đồng"},
            8: {"loc": "Cự môn", "quyen": "Thái Dương", "khoa": "Văn Khúc", "ky": "Văn xương"},
            9: {"loc": "Thiên lương", "quyen": "Tử vi", "khoa": "Thiên phủ", "ky": "Vũ khúc"},
            10: {"loc": "Phá quân", "quyen": "Cự môn", "khoa": "Thái âm", "ky": "Tham lang"},
        }

        # NOTE: Get Tứ Hóa for this Can
        if canID not in tuHoaTable:
            return self

        tuHoa = tuHoaTable[canID]

        # NOTE: Place Tứ Hóa Lưu Đại Vận stars
        if tuHoa["loc"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["loc"]], saoLuuHoaLocDaiVan)

        if tuHoa["quyen"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["quyen"]], saoLuuHoaQuyenDaiVan)

        if tuHoa["khoa"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["khoa"]], saoLuuHoaKhoaDaiVan)

        if tuHoa["ky"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["ky"]], saoLuuHoaKyDaiVan)

        return self

    def nhapSaoTuHoaLuuTieuVan(self, canNamXem):
        """
        Tính và gán Tứ Hóa Lưu Tiểu Vận dựa trên Thiên Can của năm xem.

        Logic:
        1. Lấy Thiên Can của năm xem (canNamXem)
        2. Dựa vào Thiên Can, tra bảng Tứ Hóa để tìm vị trí các sao Chính tinh
        3. Đặt 4 sao Hóa lộc.TV, Hóa quyền.TV, Hóa khoa.TV, Hóa kỵ.TV
           vào vị trí các sao Chính tinh tương ứng

        Args:
            canNamXem (int): Can của năm xem (1-10)

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import star definitions
        from core.calculations.Sao import (
            saoLuuHoaLocTieuVan, saoLuuHoaQuyenTieuVan,
            saoLuuHoaKhoaTieuVan, saoLuuHoaKyTieuVan
        )

        # NOTE: Validate canNamXem
        if canNamXem is None or canNamXem == 0:
            return self

        # NOTE: Find positions of major stars (Chính tinh) to apply Tứ Hóa
        # Build a map of star names to their palace positions
        viTriSaoChinhTinh = {}
        chinhTinhNames = [
            "Tử vi", "Liêm trinh", "Thiên đồng", "Vũ khúc", "Thái Dương",
            "Thiên cơ", "Thiên phủ", "Thái âm", "Tham lang", "Cự môn",
            "Thiên tướng", "Thiên lương", "Thất sát", "Phá quân",
            "Văn xương", "Văn Khúc"
        ]

        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            for sao in cung.cungSao:
                sao_ten = sao.get('saoTen') if isinstance(sao, dict) else sao.saoTen
                if sao_ten in chinhTinhNames:
                    viTriSaoChinhTinh[sao_ten] = cung.cungSo

        # NOTE: Tứ Hóa table based on Thiên Can (same as in App.py)
        tuHoaTable = {
            1: {"loc": "Liêm trinh", "quyen": "Phá quân", "khoa": "Vũ khúc", "ky": "Thái Dương"},
            2: {"loc": "Thiên cơ", "quyen": "Thiên lương", "khoa": "Tử vi", "ky": "Thái âm"},
            3: {"loc": "Thiên đồng", "quyen": "Thiên cơ", "khoa": "Văn xương", "ky": "Liêm trinh"},
            4: {"loc": "Thái âm", "quyen": "Thiên đồng", "khoa": "Thiên cơ", "ky": "Cự môn"},
            5: {"loc": "Tham lang", "quyen": "Thái âm", "khoa": "Thái Dương", "ky": "Thiên cơ"},
            6: {"loc": "Vũ khúc", "quyen": "Tham lang", "khoa": "Thiên lương", "ky": "Văn Khúc"},
            7: {"loc": "Thái Dương", "quyen": "Vũ khúc", "khoa": "Thái âm", "ky": "Thiên đồng"},
            8: {"loc": "Cự môn", "quyen": "Thái Dương", "khoa": "Văn Khúc", "ky": "Văn xương"},
            9: {"loc": "Thiên lương", "quyen": "Tử vi", "khoa": "Thiên phủ", "ky": "Vũ khúc"},
            10: {"loc": "Phá quân", "quyen": "Cự môn", "khoa": "Thái âm", "ky": "Tham lang"},
        }

        # NOTE: Get Tứ Hóa for this Can
        if canNamXem not in tuHoaTable:
            return self

        tuHoa = tuHoaTable[canNamXem]

        # NOTE: Place Tứ Hóa Lưu Tiểu Vận stars
        if tuHoa["loc"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["loc"]], saoLuuHoaLocTieuVan)

        if tuHoa["quyen"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["quyen"]], saoLuuHoaQuyenTieuVan)

        if tuHoa["khoa"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["khoa"]], saoLuuHoaKhoaTieuVan)

        if tuHoa["ky"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["ky"]], saoLuuHoaKyTieuVan)

        return self

    def nhapSaoTuHoaLuuThang(self, thangAmXem):
        """
        Tính và gán Tứ Hóa Lưu Tháng dựa trên Thiên Can của tháng vận trùng với tháng âm lịch xem.

        Logic:
        1. Tìm cung có thangLuuThaiTue = thangAmXem (tháng vận trùng với tháng xem)
        2. Lấy Thiên Can từ thangLuuThaiTueCanChi của cung đó
        3. Dựa vào Thiên Can, tra bảng Tứ Hóa để tìm vị trí các sao Chính tinh
        4. Đặt 4 sao Hóa lộc.Th, Hóa quyền.Th, Hóa khoa.Th, Hóa kỵ.Th
           vào vị trí các sao Chính tinh tương ứng

        Args:
            thangAmXem (int): Tháng âm lịch xem (1-12)

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import star definitions
        from core.calculations.Sao import (
            saoLuuHoaLocThang, saoLuuHoaQuyenThang,
            saoLuuHoaKhoaThang, saoLuuHoaKyThang
        )
        from core.calculations.AmDuong import thienCan

        # NOTE: Validate thangAmXem
        if thangAmXem is None or thangAmXem < 1 or thangAmXem > 12:
            return self

        # NOTE: Find palace with thangLuuThaiTue matching thangAmXem
        cungThangXem = None
        thangCanChi = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            if hasattr(cung, 'thangLuuThaiTue') and cung.thangLuuThaiTue == thangAmXem:
                cungThangXem = cung
                if hasattr(cung, 'thangLuuThaiTueCanChi'):
                    thangCanChi = cung.thangLuuThaiTueCanChi
                break

        # NOTE: If month not found or no Can Chi, skip
        if cungThangXem is None or thangCanChi is None:
            return self

        # NOTE: Extract Can from Can Chi string (format: "Đ.Dần")
        # Get the first character before the period
        canVietTat = thangCanChi.split('.')[0]

        # NOTE: Map abbreviated Can to Can ID
        canID = None
        for i, canData in enumerate(thienCan):
            if canData['chuCaiDau'] == canVietTat:
                canID = i
                break

        # NOTE: If Can not found in lookup table, skip
        if canID is None or canID == 0:
            return self

        # NOTE: Find positions of major stars (Chính tinh) to apply Tứ Hóa
        # Build a map of star names to their palace positions
        viTriSaoChinhTinh = {}
        chinhTinhNames = [
            "Tử vi", "Liêm trinh", "Thiên đồng", "Vũ khúc", "Thái Dương",
            "Thiên cơ", "Thiên phủ", "Thái âm", "Tham lang", "Cự môn",
            "Thiên tướng", "Thiên lương", "Thất sát", "Phá quân",
            "Văn xương", "Văn Khúc"
        ]

        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            for sao in cung.cungSao:
                sao_ten = sao.get('saoTen') if isinstance(sao, dict) else sao.saoTen
                if sao_ten in chinhTinhNames:
                    viTriSaoChinhTinh[sao_ten] = cung.cungSo

        # NOTE: Tứ Hóa table based on Thiên Can (same as in App.py)
        tuHoaTable = {
            1: {"loc": "Liêm trinh", "quyen": "Phá quân", "khoa": "Vũ khúc", "ky": "Thái Dương"},
            2: {"loc": "Thiên cơ", "quyen": "Thiên lương", "khoa": "Tử vi", "ky": "Thái âm"},
            3: {"loc": "Thiên đồng", "quyen": "Thiên cơ", "khoa": "Văn xương", "ky": "Liêm trinh"},
            4: {"loc": "Thái âm", "quyen": "Thiên đồng", "khoa": "Thiên cơ", "ky": "Cự môn"},
            5: {"loc": "Tham lang", "quyen": "Thái âm", "khoa": "Thái Dương", "ky": "Thiên cơ"},
            6: {"loc": "Vũ khúc", "quyen": "Tham lang", "khoa": "Thiên lương", "ky": "Văn Khúc"},
            7: {"loc": "Thái Dương", "quyen": "Vũ khúc", "khoa": "Thái âm", "ky": "Thiên đồng"},
            8: {"loc": "Cự môn", "quyen": "Thái Dương", "khoa": "Văn Khúc", "ky": "Văn xương"},
            9: {"loc": "Thiên lương", "quyen": "Tử vi", "khoa": "Thiên phủ", "ky": "Vũ khúc"},
            10: {"loc": "Phá quân", "quyen": "Cự môn", "khoa": "Thái âm", "ky": "Tham lang"},
        }

        # NOTE: Get Tứ Hóa for this Can
        if canID not in tuHoaTable:
            return self

        tuHoa = tuHoaTable[canID]

        # NOTE: Place Tứ Hóa Lưu Tháng stars
        if tuHoa["loc"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["loc"]], saoLuuHoaLocThang)

        if tuHoa["quyen"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["quyen"]], saoLuuHoaQuyenThang)

        if tuHoa["khoa"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["khoa"]], saoLuuHoaKhoaThang)

        if tuHoa["ky"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["ky"]], saoLuuHoaKyThang)

        return self

    def nhapThangLuuThaiTue(self, thangSinh, gioSinh, canNamXem=None):
        """
        An tháng của năm xem theo phái Lưu Thái Tuế.

        Logic:
        1. Lấy cung có MỆNH.TV làm tháng Giêng (tháng 1 âm lịch)
        2. Đếm nghịch chiều kim đồng hồ (nghịch - đi ngược 12 cung) từ MỆNH.TV đến tháng sinh
        3. Từ cung tháng sinh, coi đó là giờ Tý
        4. Đếm thuận chiều kim đồng hồ (thuận - đi xuôi 12 cung) từ giờ Tý đến giờ sinh
        5. An tháng 1 (của năm xem) vào cung tìm được ở bước 4
        6. Các tháng còn lại (2-12) an thuận chiều kim đồng hồ

        Args:
            thangSinh (int): Tháng sinh âm lịch (1-12)
            gioSinh (int): Giờ sinh (1-12)
            canNamXem (int, optional): Can của năm xem (1-10) để tính Can Chi tháng

        Returns:
            self: DiaBan instance for chaining
        """
        from core.calculations.AmDuong import dichCung, thienCan, diaChi

        # NOTE: Step 1 - Find palace with MỆNH.TV
        cungMenhTV = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            if hasattr(cung, 'cungTieuVan') and cung.cungTieuVan == "MỆNH.TV":
                cungMenhTV = cung.cungSo
                break

        # NOTE: If MỆNH.TV not found, return without placing months
        if cungMenhTV is None:
            return self

        # NOTE: Step 2 - Count counter-clockwise (nghịch = -1) from MỆNH.TV to birth month
        # MỆNH.TV = tháng Giêng (1), so we need to go (thangSinh - 1) steps backward
        cungThangSinh = dichCung(cungMenhTV, -(thangSinh - 1))

        # NOTE: Step 3 - cungThangSinh is considered as giờ Tý (hour 1)
        # NOTE: Step 4 - Count clockwise (thuận = +1) from giờ Tý to birth hour
        # We need to go (gioSinh - 1) steps forward
        cungThang1 = dichCung(cungThangSinh, gioSinh - 1)

        # NOTE: Calculate Can of tháng Giêng (month 1) if canNamXem is provided
        # Formula: canThangGieng = (canNamXem * 2 + 1) % 10, if 0 then 10
        canThangGieng = None
        if canNamXem is not None:
            canThangGieng = (canNamXem * 2 + 1) % 10
            if canThangGieng == 0:
                canThangGieng = 10

        # NOTE: Step 5 & 6 - Place month 1-12 clockwise starting from cungThang1
        # Store month numbers and Can Chi in temporary attributes for display
        for i in range(12):
            thangSo = i + 1  # Month 1-12
            targetCung = dichCung(cungThang1, i)  # Clockwise direction

            # Add month marker to the palace
            if not hasattr(self.thapNhiCung[targetCung], 'thangLuuThaiTue'):
                self.thapNhiCung[targetCung].thangLuuThaiTue = thangSo

            # NOTE: Add Can Chi of month if canNamXem is provided
            if canThangGieng is not None:
                # Can of each month increases sequentially from tháng Giêng
                canThang = (canThangGieng + i - 1) % 10 + 1

                # Chi of month: Tháng Giêng (1) = Dần (3), Tháng 2 = Mão (4), ...
                # Formula: chiThang = (thangSo + 2) % 12, if 0 then 12
                chiThang = (thangSo + 2) % 12
                if chiThang == 0:
                    chiThang = 12

                # Get Can and Chi names
                canThangVietTat = thienCan[canThang]['chuCaiDau']
                chiThangTen = diaChi[chiThang]['tenChi']

                # Store Can Chi as "Đ.Dậu" format (abbreviated Can + full Chi, no space)
                self.thapNhiCung[targetCung].thangLuuThaiTueCanChi = f"{canThangVietTat}.{chiThangTen}"

        return self

    def nhapNgayThangXem(self, thangAmXem, soNgayTrongThang=30):
        """
        An các ngày trong tháng âm lịch vào 12 cung.

        Logic:
        1. Tìm cung có tháng xem âm lịch
        2. Cung đó chứa ngày 1
        3. Các ngày còn lại (2-30) được đặt thuận chiều kim đồng hồ
        4. Mỗi cung sẽ chứa 2-3 ngày

        Args:
            thangAmXem (int): Tháng âm lịch cần xem (1-12)
            soNgayTrongThang (int): Số ngày trong tháng (29 hoặc 30), mặc định 30

        Returns:
            self: DiaBan instance for chaining
        """
        from core.calculations.AmDuong import dichCung

        # NOTE: Find palace that has thangAmXem
        cungThangXem = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            if hasattr(cung, 'thangLuuThaiTue') and cung.thangLuuThaiTue == thangAmXem:
                cungThangXem = cung.cungSo
                break

        # NOTE: If month palace not found, return without placing days
        if cungThangXem is None:
            return self

        # NOTE: Initialize ngayThang list for each palace
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            cung.ngayThang = []

        # NOTE: Place days 1-30 clockwise starting from month palace
        for ngay in range(1, soNgayTrongThang + 1):
            # Calculate which palace this day goes to
            # Day 1 = cungThangXem, day 2 = next palace (clockwise), etc.
            targetCung = dichCung(cungThangXem, ngay - 1)

            # Add day to palace's list
            self.thapNhiCung[targetCung].ngayThang.append(ngay)

        # NOTE: Format ngayThang as comma-separated string for each palace
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            if hasattr(cung, 'ngayThang') and len(cung.ngayThang) > 0:
                cung.ngayThangStr = ','.join(map(str, cung.ngayThang))
            else:
                cung.ngayThangStr = None

        return self

    def nhapNgayLuuThaiTue(self, ngayAmXem, canNgayXem, chiNgayXem):
        """
        An Ngày vận (Ngày Lưu Thái Tuế) vào các cung.

        Logic:
        1. Tìm cung có ngày xem âm lịch (từ ngayThang list)
        2. An ngày xem với Can Chi vào cung đó
        3. Các ngày khác trong tháng được tính Can Chi và đặt vào các cung tương ứng

        Args:
            ngayAmXem (int): Ngày âm lịch xem (1-30)
            canNgayXem (int): Can của ngày xem (1-10)
            chiNgayXem (int): Chi của ngày xem (1-12)

        Returns:
            self: DiaBan instance for chaining
        """
        from core.calculations.AmDuong import thienCan, diaChi

        # NOTE: Initialize ngayLuuThaiTue list for each palace
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            cung.ngayLuuThaiTue = []

        # NOTE: Calculate Can Chi for each day in the month and place in corresponding palace
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue

            # Check if this palace has days
            if not hasattr(cung, 'ngayThang') or not cung.ngayThang:
                continue

            # For each day in this palace
            for ngay in cung.ngayThang:
                # NOTE: Calculate Can Chi for this day
                # Can cycles every 10 days, Chi cycles every 12 days
                # We know canNgayXem, chiNgayXem for ngayAmXem
                # So we can calculate for other days by offset

                offset = ngay - ngayAmXem

                # Calculate Can for this day (cycles 1-10)
                canNgay = (canNgayXem + offset - 1) % 10 + 1

                # Calculate Chi for this day (cycles 1-12)
                chiNgay = (chiNgayXem + offset - 1) % 12 + 1

                # Get abbreviated Can and full Chi names
                canNgayVietTat = thienCan[canNgay]['chuCaiDau']
                chiNgayTen = diaChi[chiNgay]['tenChi']

                # Store as "ngày (Can.Chi)" format, e.g., "15 (G.Tuất)"
                ngayCanChi = f"{ngay} ({canNgayVietTat}.{chiNgayTen})"
                cung.ngayLuuThaiTue.append(ngayCanChi)

        # NOTE: Format ngayLuuThaiTue as comma-separated string for each palace
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            if hasattr(cung, 'ngayLuuThaiTue') and len(cung.ngayLuuThaiTue) > 0:
                cung.ngayLuuThaiTueStr = ', '.join(cung.ngayLuuThaiTue)
            else:
                cung.ngayLuuThaiTueStr = None

        return self

    def nhapSaoTuHoaLuuNgay(self, ngayAmXem):
        """
        Tính và gán Tứ Hóa Lưu Ngày dựa trên Thiên Can của ngày vận trùng với ngày âm lịch xem.

        Logic:
        1. Tìm cung có ngayThang chứa ngayAmXem
        2. Tìm Can Chi tương ứng với ngày đó từ ngayLuuThaiTue
        3. Lấy Thiên Can từ Can Chi string
        4. Dựa vào Thiên Can, tra bảng Tứ Hóa để tìm vị trí các sao Chính tinh
        5. Đặt 4 sao Hóa lộc.Ng, Hóa quyền.Ng, Hóa khoa.Ng, Hóa kỵ.Ng
           vào vị trí các sao Chính tinh tương ứng

        Args:
            ngayAmXem (int): Ngày âm lịch xem (1-30)

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import star definitions
        from core.calculations.Sao import (
            saoLuuHoaLocNgay, saoLuuHoaQuyenNgay,
            saoLuuHoaKhoaNgay, saoLuuHoaKyNgay
        )
        from core.calculations.AmDuong import thienCan

        # NOTE: Validate ngayAmXem
        if ngayAmXem is None or ngayAmXem < 1 or ngayAmXem > 30:
            return self

        # NOTE: Find palace and Can Chi for the day matching ngayAmXem
        ngayCanChi = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue

            # Check if this palace has the viewing day
            if hasattr(cung, 'ngayThang') and ngayAmXem in cung.ngayThang:
                # Find the Can Chi for this day from ngayLuuThaiTue list
                if hasattr(cung, 'ngayLuuThaiTue'):
                    for ngayStr in cung.ngayLuuThaiTue:
                        # Format is "15 (G.Tuất)"
                        if ngayStr.startswith(f"{ngayAmXem} ("):
                            # Extract Can Chi part: "G.Tuất"
                            start = ngayStr.find('(') + 1
                            end = ngayStr.find(')')
                            if start > 0 and end > start:
                                ngayCanChi = ngayStr[start:end]
                                break
                break

        # NOTE: If day not found or no Can Chi, skip
        if ngayCanChi is None:
            return self

        # NOTE: Extract Can from Can Chi string (format: "G.Tuất")
        canVietTat = ngayCanChi.split('.')[0]

        # NOTE: Map abbreviated Can to Can ID
        canID = None
        for i, canData in enumerate(thienCan):
            if canData['chuCaiDau'] == canVietTat:
                canID = i
                break

        # NOTE: If Can not found in lookup table, skip
        if canID is None or canID == 0:
            return self

        # NOTE: Find positions of major stars (Chính tinh) to apply Tứ Hóa
        viTriSaoChinhTinh = {}
        chinhTinhNames = [
            "Tử vi", "Liêm trinh", "Thiên đồng", "Vũ khúc", "Thái Dương",
            "Thiên cơ", "Thiên phủ", "Thái âm", "Tham lang", "Cự môn",
            "Thiên tướng", "Thiên lương", "Thất sát", "Phá quân",
            "Văn xương", "Văn Khúc"
        ]

        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            for sao in cung.cungSao:
                sao_ten = sao.get('saoTen') if isinstance(sao, dict) else sao.saoTen
                if sao_ten in chinhTinhNames:
                    viTriSaoChinhTinh[sao_ten] = cung.cungSo

        # NOTE: Tứ Hóa table based on Thiên Can
        tuHoaTable = {
            1: {"loc": "Liêm trinh", "quyen": "Phá quân", "khoa": "Vũ khúc", "ky": "Thái Dương"},
            2: {"loc": "Thiên cơ", "quyen": "Thiên lương", "khoa": "Tử vi", "ky": "Thái âm"},
            3: {"loc": "Thiên đồng", "quyen": "Thiên cơ", "khoa": "Văn xương", "ky": "Liêm trinh"},
            4: {"loc": "Thái âm", "quyen": "Thiên đồng", "khoa": "Thiên cơ", "ky": "Cự môn"},
            5: {"loc": "Tham lang", "quyen": "Thái âm", "khoa": "Thái Dương", "ky": "Thiên cơ"},
            6: {"loc": "Vũ khúc", "quyen": "Tham lang", "khoa": "Thiên lương", "ky": "Văn Khúc"},
            7: {"loc": "Thái Dương", "quyen": "Vũ khúc", "khoa": "Thái âm", "ky": "Thiên đồng"},
            8: {"loc": "Cự môn", "quyen": "Thái Dương", "khoa": "Văn Khúc", "ky": "Văn xương"},
            9: {"loc": "Thiên lương", "quyen": "Tử vi", "khoa": "Thiên phủ", "ky": "Vũ khúc"},
            10: {"loc": "Phá quân", "quyen": "Cự môn", "khoa": "Thái âm", "ky": "Tham lang"},
        }

        # NOTE: Get Tứ Hóa for this Can
        if canID not in tuHoaTable:
            return self

        tuHoa = tuHoaTable[canID]

        # NOTE: Place Tứ Hóa Lưu Ngày stars
        if tuHoa["loc"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["loc"]], saoLuuHoaLocNgay)

        if tuHoa["quyen"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["quyen"]], saoLuuHoaQuyenNgay)

        if tuHoa["khoa"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["khoa"]], saoLuuHoaKhoaNgay)

        if tuHoa["ky"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["ky"]], saoLuuHoaKyNgay)

        return self

    def nhapSaoTuHoaLuuGio(self, ngayXem, thangXem, namXem, gioXem):
        """
        Tính và gán Tứ Hóa Lưu Giờ dựa trên Thiên Can của giờ xem.

        Logic:
        1. Tính Thiên Can của giờ xem dựa vào công thức từ ThienBan.py
        2. Dựa vào Thiên Can, tra bảng Tứ Hóa để tìm vị trí các sao Chính tinh
        3. Đặt 4 sao Hóa lộc.Gi, Hóa quyền.Gi, Hóa khoa.Gi, Hóa kỵ.Gi
           vào vị trí các sao Chính tinh tương ứng

        Args:
            ngayXem (int): Ngày xem (1-31)
            thangXem (int): Tháng xem (1-12)
            namXem (int): Năm xem
            gioXem (int): Giờ xem (1=Tý, 2=Sửu, 3=Dần,...12=Hợi)

        Returns:
            self: DiaBan instance for chaining
        """
        # NOTE: Import star definitions
        from core.calculations.Sao import (
            saoLuuHoaLocGio, saoLuuHoaQuyenGio,
            saoLuuHoaKhoaGio, saoLuuHoaKyGio
        )
        from core.calculations.AmDuong import jdFromDate

        # NOTE: Validate input parameters
        if not all([ngayXem, thangXem, namXem, gioXem]):
            return self
        if gioXem < 1 or gioXem > 12:
            return self

        # NOTE: Calculate Thiên Can of hour using same formula as in ThienBan.py
        # Formula: canGioXem = ((jdFromDate(ngayXem, thangXem, namXem) - 1) * 2 % 10 + gioXem) % 10
        jd = jdFromDate(ngayXem, thangXem, namXem)
        canGioXem = ((jd - 1) * 2 % 10 + gioXem) % 10
        if canGioXem == 0:
            canGioXem = 10

        # NOTE: Find positions of major stars (Chính tinh) to apply Tứ Hóa
        viTriSaoChinhTinh = {}
        chinhTinhNames = [
            "Tử vi", "Liêm trinh", "Thiên đồng", "Vũ khúc", "Thái Dương",
            "Thiên cơ", "Thiên phủ", "Thái âm", "Tham lang", "Cự môn",
            "Thiên tướng", "Thiên lương", "Thất sát", "Phá quân",
            "Văn xương", "Văn Khúc"
        ]

        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            for sao in cung.cungSao:
                sao_ten = sao.get('saoTen') if isinstance(sao, dict) else sao.saoTen
                if sao_ten in chinhTinhNames:
                    viTriSaoChinhTinh[sao_ten] = cung.cungSo

        # NOTE: Tứ Hóa table based on Thiên Can
        tuHoaTable = {
            1: {"loc": "Liêm trinh", "quyen": "Phá quân", "khoa": "Vũ khúc", "ky": "Thái Dương"},
            2: {"loc": "Thiên cơ", "quyen": "Thiên lương", "khoa": "Tử vi", "ky": "Thái âm"},
            3: {"loc": "Thiên đồng", "quyen": "Thiên cơ", "khoa": "Văn xương", "ky": "Liêm trinh"},
            4: {"loc": "Thái âm", "quyen": "Thiên đồng", "khoa": "Thiên cơ", "ky": "Cự môn"},
            5: {"loc": "Tham lang", "quyen": "Thái âm", "khoa": "Thái Dương", "ky": "Thiên cơ"},
            6: {"loc": "Vũ khúc", "quyen": "Tham lang", "khoa": "Thiên lương", "ky": "Văn Khúc"},
            7: {"loc": "Thái Dương", "quyen": "Vũ khúc", "khoa": "Thái âm", "ky": "Thiên đồng"},
            8: {"loc": "Cự môn", "quyen": "Thái Dương", "khoa": "Văn Khúc", "ky": "Văn xương"},
            9: {"loc": "Thiên lương", "quyen": "Tử vi", "khoa": "Thiên phủ", "ky": "Vũ khúc"},
            10: {"loc": "Phá quân", "quyen": "Cự môn", "khoa": "Thái âm", "ky": "Tham lang"},
        }

        # NOTE: Get Tứ Hóa for this Can
        if canGioXem not in tuHoaTable:
            return self

        tuHoa = tuHoaTable[canGioXem]

        # NOTE: Place Tứ Hóa Lưu Giờ stars
        if tuHoa["loc"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["loc"]], saoLuuHoaLocGio)

        if tuHoa["quyen"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["quyen"]], saoLuuHoaQuyenGio)

        if tuHoa["khoa"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["khoa"]], saoLuuHoaKhoaGio)

        if tuHoa["ky"] in viTriSaoChinhTinh:
            self.nhapSao(viTriSaoChinhTinh[tuHoa["ky"]], saoLuuHoaKyGio)

        return self

    def nhapGioCanChi(self, ngayAmXem, ngayXem, thangXem, namXem, gioXem=None):
        """
        Đặt giờ Can Chi vào các cung dựa theo ngày âm lịch xem.

        Logic:
        1. Tìm cung có ngày vận khớp với ngày âm lịch xem → an giờ Tý vào cung đó
        2. Các giờ tiếp theo được an theo chiều thuận kim đồng hồ (1→2→3→...→12)
        3. Mỗi giờ có đầy đủ Thiên Can + Địa Chi, tính theo công thức "Nhật Thượng Khởi Giờ"
        4. Giờ trùng với giờ xem sẽ được đánh dấu để in đậm

        Args:
            ngayAmXem (int): Ngày âm lịch xem (1-30)
            ngayXem (int): Ngày dương lịch xem (dùng để tính Julian Day)
            thangXem (int): Tháng dương lịch xem
            namXem (int): Năm dương lịch xem
            gioXem (int, optional): Giờ xem (1=Tý, 2=Sửu,...12=Hợi) để đánh dấu in đậm

        Returns:
            self: DiaBan instance for chaining
        """
        from core.calculations.AmDuong import jdFromDate

        if not all([ngayAmXem, ngayXem, thangXem, namXem]):
            return self

        # NOTE: Find palace with matching ngayThang (day transit)
        cungGioTy = None
        for cung in self.thapNhiCung:
            if cung.cungSo == 0:
                continue
            # Check if this palace has ngayThang and contains ngayAmXem
            if hasattr(cung, 'ngayThang') and ngayAmXem in cung.ngayThang:
                cungGioTy = cung.cungSo
                break

        if cungGioTy is None:
            return self

        # NOTE: Calculate Thiên Can of hour Tý using Julian Day
        # Formula from ThienBan.py: canGioTy = ((jd - 1) * 2 % 10 + 1) % 10
        jd = jdFromDate(ngayXem, thangXem, namXem)
        canGioTy = ((jd - 1) * 2 % 10 + 1) % 10
        if canGioTy == 0:
            canGioTy = 10

        # NOTE: Place 12 hours Can Chi clockwise starting from cungGioTy
        for i in range(12):
            # Calculate palace number (clockwise: 1→2→3→...→12→1)
            cungSo = (cungGioTy + i - 1) % 12 + 1

            # Calculate Thiên Can for this hour (cycles through 10 Cans)
            canGio = (canGioTy + i - 1) % 10 + 1

            # Địa Chi for this hour (i=0 is Tý, i=1 is Sửu, etc.)
            chiGio = i + 1

            # Get abbreviated Can and Chi names
            tenCan = thienCan[canGio]['tenCan'][0]  # First character
            tenChi = diaChi[chiGio]['tenChi']

            # Format: "Gi.B.Tuất" (Gi = Giờ, B = Bính)
            gioCanChi = f"Gi.{tenCan}.{tenChi}"

            # Assign to palace
            self.thapNhiCung[cungSo].gioCanChi = gioCanChi

            # NOTE: Mark hour matching gioXem for bold display
            if gioXem and chiGio == gioXem:
                self.thapNhiCung[cungSo].gioCanChiBold = True
            else:
                self.thapNhiCung[cungSo].gioCanChiBold = False

        return self

    def nhapCungThan(self):
        self.thapNhiCung[self.cungThan].anCungThan()

    def nhapSao(self, cungSo, *args):
        for sao in args:
            self.thapNhiCung[cungSo].themSao(sao)
        return self

    def nhapTuan(self, *args):
        for cung in args:
            self.thapNhiCung[cung].anTuan()
        return self

    def nhapTriet(self, *args):
        for cung in args:
            self.thapNhiCung[cung].anTriet()
        return self


def dacTinhSao(viTriDiaBan, sao):
    saoId = sao.saoID
    maTranDacTinh = {
        1: ["Tử vi", "B", "Đ", "M", "B", "V", "M", "M", "Đ", "M", "B", "V",
            "B"],
        2: ["Liêm trinh", "V", "Đ", "V", "H", "M", "H", "V", "Đ", "V", "H",
            "M", "H"],
        3: ["Thiên đồng", "V", "H", "M", "Đ", "H", "Đ", "H", "H", "M", "H",
            "H", "Đ"],
        4: ["Vũ khúc", "V", "M", "V", "Đ", "M", "H", "V", "M", "V", "Đ", "M",
            "H"],
        5: ["Thái dương", "H", "Đ", "V", "V", "V", "M", "M", "Đ", "H", "H",
            "H", "H"],
        6: ["Thiên cơ", "Đ", "Đ", "H", "M", "M", "V", "Đ", "Đ", "V", "M", "M",
            "H"],
        8: ["Thái âm", "V", "Đ", "H", "H", "H", "H", "H", "Đ", "V", "M",
            "M", "M"],
        9: ["Tham lang", "H", "M", "Đ", "H", "V", "H", "H", "M", "Đ", "H",
            "V", "H"],
        10: ["Cự môn", "V", "H", "V", "M", "H", "H", "V", "H", "Đ", "M", "H",
             "Đ"],
        11: ["Thiên tướng", "V", "Đ", "M", "H", "V", "Đ", "V", "Đ", "M", "H",
             "V", "Đ"],
        12: ["Thiên lương", "V", "Đ", "V", "V", "M", "H", "M", "Đ", "V", "H",
             "M", "H"],
        13: ["Thất sát", "M", "Đ", "M", "H", "H", "V", "M", "Đ", "M", "H",
             "H", "V"],
        14: ["Phá quân", "M", "V", "H", "H", "Đ", "H", "M", "V", "H", "H",
             "Đ", "H"],
        51: ["Đà la", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ",
             "H"],
        52: ["Kình dương", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H",
             "Đ", "H"],
        55: ["Linh tinh", "H", "H", "Đ", "Đ", "Đ", "Đ", "Đ", "H", "H", "H",
             "H", "H"],
        56: ["Hỏa tinh", "H", "H", "Đ", "Đ", "Đ", "Đ", "Đ", "H", "H", "H",
             "H", "H"],
        57: ["Văn xương", "H", "Đ", "H", "Đ", "H", "Đ", "H", "Đ", "H", "H",
             "Đ", "Đ"],
        58: ["Văn khúc", "H", "Đ", "H", "Đ", "H", "Đ", "H", "Đ", "H", "H",
             "Đ", "Đ"],
        53: ["Địa không", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H",
             "H", "Đ"],
        54: ["Địa kiếp", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H",
             "Đ"],
        95: ["Hóa kỵ", None, "Đ", None, None, "Đ", None, None, "Đ", None, None,
             "Đ", None],
        36: ["Đại hao", None, None, "Đ", "Đ", None, None, None, None, "Đ", "Đ",
             None, None],
        30: ["Tiểu Hao", None, None, "Đ", "Đ", None, None, None, None, "Đ",
             "Đ", None, None],
        69: ["Thiên khốc", "Đ", "Đ", None, "Đ", None, None, "Đ", "Đ", None,
             "Đ", None, None],
        70: ["Thiên hư", "Đ", "Đ", None, "Đ", None, None, "Đ", "Đ", None, "Đ",
             None, None],
        98: ["Thiên mã", None, None, "Đ", None, None, "Đ", None, None, None,
             None, None, None],
        73: ["Thiên Hình", None, None, "Đ", "Đ", None, None, None, None, "Đ",
             "Đ", None, None],
        74: ["Thiên riêu", None, None, "Đ", "Đ", None, None, None, None, None,
             "Đ", "Đ", None],

    }
    if sao.saoID in maTranDacTinh.keys():
        if maTranDacTinh[sao.saoID][viTriDiaBan] in ["M", "V", "Đ", "B", "H"]:
            sao.anDacTinh(maTranDacTinh[sao.saoID][viTriDiaBan])
