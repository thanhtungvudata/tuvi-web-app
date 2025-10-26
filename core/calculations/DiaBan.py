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
