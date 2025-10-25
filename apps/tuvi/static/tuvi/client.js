// Danh sách 45 sao quan trọng (luôn hiển thị)
const SAO_QUAN_TRONG_IDS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,  // 14 Chính tinh
    61, 62, 59, 60, 57, 58,  // 6 Cát tinh (Tả phù, Hữu bật, Thiên khôi, Thiên việt, Văn xương, Văn khúc)
    52, 51, 53, 54, 55, 56,  // 6 Hung tinh (Kình dương, Đà la, Địa không, Địa kiếp, Linh tinh, Hỏa tinh)
    94, 93, 92, 95,  // Tứ hóa (Hóa lộc, Hóa quyền, Hóa khoa, Hóa kỵ)
    73, 98,  // Thiên hình, Thiên mã
    27,      // Lộc tồn (sao quan trọng khác)
    39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50  // 12 sao Vòng Tràng Sinh
];

// NOTE: Phân loại sao tốt/xấu theo saoLoai (logic từ project cũ)
// - Sao tốt (trái): saoLoai !== 1 && saoLoai < 10
// - Sao xấu (phải): saoLoai !== 1 && saoLoai > 10

// Danh sách sao Vòng Tràng Sinh (hiển thị ở giữa dưới)
const SAO_TRANG_SINH_IDS = [39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50];

// Biến flag để tránh attach multiple listeners
let displayOptionsListenerAttached = false;

// Biến để track cung đang được highlight
let currentHighlightedCung = null;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('lstv-form');
    const resultContainer = document.getElementById('lasotuvi-result');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const params = new URLSearchParams();

        params.append('hoten', formData.get('hoten') || 'Chưa nhập');
        params.append('gioitinh', formData.get('gioitinh'));
        params.append('ngaysinh', formData.get('ngaysinh'));
        params.append('thangsinh', formData.get('thangsinh'));
        params.append('namsinh', formData.get('namsinh'));
        params.append('giosinh', formData.get('giosinh'));
        params.append('muigio', formData.get('muigio'));

        if (formData.get('amlich')) {
            params.append('amlich', 'on');
        }

        const apiUrl = '/api?' + params.toString();

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                renderLaSoTuVi(data);
                resultContainer.style.display = 'block';
                resultContainer.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Có lỗi xảy ra khi lập lá số. Vui lòng thử lại!');
            });
    });
});

function renderLaSoTuVi(data) {
    const thienBan = data.thienBan;
    const thapNhiCung = data.thapNhiCung;

    // Lưu lại data để có thể re-render khi toggle checkbox
    window.currentLaSoData = data;

    renderThienBan(thienBan);
    renderThapNhiCung(thapNhiCung, thienBan);

    // Attach event listener cho checkbox (chỉ attach 1 lần)
    attachDisplayOptionsListener();
}

function renderThienBan(thienBan) {
    const thienBanContent = document.querySelector('.thien-ban-content');

    const html = `
        <p><strong>Họ tên:</strong> <span class="value">${thienBan.ten}</span></p>
        <p><strong>Năm sinh:</strong> <span class="value">${thienBan.namDuong} - ${thienBan.canNamTen} ${thienBan.chiNamTen}</span></p>
        <p><strong>Tháng:</strong> <span class="value">${thienBan.canThangTen} ${thienBan.chiThangTen}</span></p>
        <p><strong>Ngày:</strong> <span class="value">${thienBan.canNgayTen} ${thienBan.chiNgayTen}</span></p>
        <p><strong>Giờ sinh:</strong> <span class="value">${thienBan.gioSinh}</span></p>
        <p><strong>Năm xem:</strong> <span class="value">(Sẽ cập nhật sau)</span></p>
        <p><strong>Âm dương:</strong> <span class="value">${thienBan.amDuongNamSinh} ${thienBan.namNu}</span></p>
        <p><strong>Mệnh:</strong> <span class="value">${thienBan.banMenh}</span></p>
        <p><strong>Cục:</strong> <span class="value">${thienBan.tenCuc}</span></p>
        <p><strong>Chủ mệnh:</strong> <span class="value">${thienBan.menhChu}</span></p>
        <p><strong>Chủ thân:</strong> <span class="value">${thienBan.thanChu}</span></p>
        <p><strong>Thân cư:</strong> <span class="value">(Sẽ cập nhật sau)</span></p>
    `;

    thienBanContent.innerHTML = html;
}

function renderThapNhiCung(thapNhiCung, thienBan) {
    // Kiểm tra trạng thái checkbox (mặc định TẮT = false = chỉ hiện sao quan trọng)
    const hienPhusao = document.getElementById('hienphusao')?.checked ?? false;

    // NOTE: Lưu lại cung đang được highlight trước khi re-render
    const savedHighlightedCung = currentHighlightedCung;

    thapNhiCung.forEach(cung => {
        if (cung.cungSo === 0) return;

        const cungElement = document.getElementById(`cung-${cung.cungSo}`);
        if (!cungElement) return;

        let html = '';

        // Header: Địa chi (trái) - Tên cung (giữa) - Đại hạn (phải)
        html += '<div class="cung-header">';

        // Địa chi - góc trái trên
        html += `<div class="cung-ten-chi">${cung.cungTen}</div>`;

        // Tên cung - giữa trên
        if (cung.cungChu) {
            let cungChuLabel = cung.cungChu.toUpperCase();
            if (cung.cungThan) {
                cungChuLabel += ' <THÂN>';
            }
            html += `<div class="cung-ten-chu">${cungChuLabel}</div>`;
        } else {
            html += '<div class="cung-ten-chu"></div>'; // Placeholder để giữ layout
        }

        // Đại hạn - góc phải trên
        if (cung.cungDaiHan) {
            html += `<div class="cung-dai-han">${cung.cungDaiHan}</div>`;
        } else {
            html += '<div class="cung-dai-han"></div>'; // Placeholder để giữ layout
        }

        html += '</div>'; // Đóng cung-header

        if (cung.cungSao && cung.cungSao.length > 0) {
            // ===== LỌC SAO THEO TÙY CHỌN =====
            let danhSachSaoHienThi = cung.cungSao;

            if (!hienPhusao) {
                // Chỉ hiển thị 32 sao quan trọng
                danhSachSaoHienThi = cung.cungSao.filter(sao =>
                    SAO_QUAN_TRONG_IDS.includes(sao.saoID)
                );
            }

            // ===== PHÂN LOẠI SAO: CHÍNH TINH, TRÀNG SINH, SAO TỐT, SAO XẤU, SAO KHÁC =====
            const chinhTinh = danhSachSaoHienThi.filter(sao => sao.saoLoai === 1);
            const saoTrangSinh = danhSachSaoHienThi.filter(sao => SAO_TRANG_SINH_IDS.includes(sao.saoID));

            // Phân loại theo saoLoai (logic từ project cũ)
            // NOTE: Lộc Tồn (ID: 27) luôn hiển thị trong cột sao tốt
            const saoTot = danhSachSaoHienThi.filter(sao =>
                sao.saoLoai !== 1 &&
                !SAO_TRANG_SINH_IDS.includes(sao.saoID) &&
                (sao.saoLoai < 10 || sao.saoID === 27)
            );
            const saoXau = danhSachSaoHienThi.filter(sao =>
                sao.saoLoai !== 1 &&
                sao.saoLoai > 10 &&
                !SAO_TRANG_SINH_IDS.includes(sao.saoID)
            );

            // Các sao còn lại (saoLoai === 10, trừ Lộc Tồn)
            const saoKhac = danhSachSaoHienThi.filter(sao =>
                sao.saoLoai !== 1 &&
                !SAO_TRANG_SINH_IDS.includes(sao.saoID) &&
                sao.saoLoai === 10 &&
                sao.saoID !== 27
            );

            // Hiển thị chính tinh ở trên cùng và giữa cung
            if (chinhTinh.length > 0) {
                html += '<div class="cung-chinh-tinh">';
                chinhTinh.forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-chinh ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });
                html += '</div>';
            }

            // Hiển thị sao tốt (trái) và sao xấu (phải) trong layout 2 cột
            if (saoTot.length > 0 || saoXau.length > 0) {
                html += '<div class="cung-phu-tinh">';

                // Cột trái - Thứ tự: 6 cát tinh → Lộc Tồn → Thiên Mã → Tứ Hóa → Phụ tinh khác
                html += '<div class="sao-tot-column">';
                const catTinhIDs = [61, 62, 59, 60, 57, 58];
                const tuHoaIDs = [94, 93, 92, 95];
                const thienMaID = 98;
                const locTonID = 27;

                // 1. Hiển thị 6 cát tinh (in đậm)
                saoTot.filter(sao => catTinhIDs.includes(sao.saoID)).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 2. Hiển thị Lộc Tồn (in đậm)
                saoTot.filter(sao => sao.saoID === locTonID).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 3. Hiển thị Thiên Mã (in đậm)
                saoTot.filter(sao => sao.saoID === thienMaID).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 4. Hiển thị Tứ Hóa (in đậm)
                saoTot.filter(sao => tuHoaIDs.includes(sao.saoID)).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 5. Hiển thị các phụ tinh còn lại
                saoTot.filter(sao =>
                    !catTinhIDs.includes(sao.saoID) &&
                    sao.saoID !== locTonID &&
                    sao.saoID !== thienMaID &&
                    !tuHoaIDs.includes(sao.saoID)
                ).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });
                html += '</div>';

                // Cột phải - Thứ tự: 6 hung tinh → Tứ Hóa → Phụ tinh khác
                html += '<div class="sao-xau-column">';
                const hungTinhIDs = [52, 51, 53, 54, 55, 56];

                // 1. Hiển thị 6 hung tinh (in đậm)
                saoXau.filter(sao => hungTinhIDs.includes(sao.saoID)).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 2. Hiển thị Tứ Hóa (in đậm)
                saoXau.filter(sao => tuHoaIDs.includes(sao.saoID)).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 3. Hiển thị các phụ tinh còn lại
                saoXau.filter(sao => !hungTinhIDs.includes(sao.saoID) && !tuHoaIDs.includes(sao.saoID)).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });
                html += '</div>';

                html += '</div>'; // Đóng cung-phu-tinh
            }

            // Hiển thị các sao khác
            if (saoKhac.length > 0) {
                html += '<div class="cung-sao-list">';
                saoKhac.forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });
                html += '</div>';
            }

            // Hiển thị sao Vòng Trường Sinh ở đáy cung, căn giữa
            if (saoTrangSinh.length > 0) {
                html += '<div class="cung-trang-sinh-wrapper">';
                saoTrangSinh.forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    // Đổi "Tràng sinh" thành "Trường sinh"
                    const tenSao = sao.saoTen === 'Tràng sinh' ? 'Trường sinh' : sao.saoTen;
                    html += `<span class="sao-trang-sinh ${hanhClass}">${tenSao}${dacTinh}</span> `;
                });
                html += '</div>';
            }
        }

        cungElement.innerHTML = html;

        // NOTE: Xóa event listener cũ và thêm mới để tránh duplicate
        const newCungElement = cungElement.cloneNode(true);
        cungElement.parentNode.replaceChild(newCungElement, cungElement);

        newCungElement.addEventListener('click', function() {
            highlightRelatedCung(cung.cungSo);
        });
    });

    // NOTE: Restore highlight sau khi re-render
    if (savedHighlightedCung !== null) {
        currentHighlightedCung = null; // Reset trước
        highlightRelatedCung(savedHighlightedCung); // Highlight lại
    }
}

function getSaoClass(sao) {
    if (sao.saoLoai === 1) {
        return 'sao-chinh';
    }
    return '';
}

function getHanhClass(nguHanh) {
    const hanhMap = {
        'M': 'hanh-moc',
        'H': 'hanh-hoa',
        'O': 'hanh-tho',
        'K': 'hanh-kim',
        'T': 'hanh-thuy'
    };
    return hanhMap[nguHanh] || '';
}

function highlightRelatedCung(cungSo) {
    // NOTE: Nếu click vào cùng cung đang highlight, thì tắt highlight
    if (currentHighlightedCung === cungSo) {
        // Reset tất cả về trạng thái ban đầu
        document.querySelectorAll('.cung').forEach(el => {
            el.style.background = '#fff';
            el.style.border = '1px solid #ecf0f1';
        });
        currentHighlightedCung = null;
        return;
    }

    // Reset tất cả về trạng thái ban đầu
    document.querySelectorAll('.cung').forEach(el => {
        el.style.background = '#fff';
        el.style.border = '1px solid #ecf0f1';
    });

    // Highlight cung được click (chính cung)
    const clickedCung = document.getElementById(`cung-${cungSo}`);
    if (clickedCung) {
        clickedCung.style.background = '#fff3cd';
        clickedCung.style.border = '2px solid #ffc107';
    }

    // Highlight cung đối diện
    const doiCung = (cungSo + 6) % 12;
    const doiCungElement = document.getElementById(`cung-${doiCung === 0 ? 12 : doiCung}`);
    if (doiCungElement) {
        doiCungElement.style.background = '#f8d7da';
        doiCungElement.style.border = '2px solid #f5c6cb';
    }

    // Highlight 2 cung tam hợp
    const tamHop1 = (cungSo + 4) % 12;
    const tamHop2 = (cungSo + 8) % 12;
    [tamHop1, tamHop2].forEach(tc => {
        const el = document.getElementById(`cung-${tc === 0 ? 12 : tc}`);
        if (el) {
            el.style.background = '#d1ecf1';
            el.style.border = '2px solid #bee5eb';
        }
    });

    // Lưu lại cung đang được highlight
    currentHighlightedCung = cungSo;
}

// Attach event listener cho checkbox hiển thị phụ tinh
function attachDisplayOptionsListener() {
    if (displayOptionsListenerAttached) return;

    const checkbox = document.getElementById('hienphusao');
    if (checkbox) {
        checkbox.addEventListener('change', function() {
            // Re-render lại lá số khi thay đổi tùy chọn
            if (window.currentLaSoData) {
                renderThapNhiCung(
                    window.currentLaSoData.thapNhiCung,
                    window.currentLaSoData.thienBan
                );
            }
        });
        displayOptionsListenerAttached = true;
    }
}
