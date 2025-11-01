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

    // NOTE: Only attach form listener if form exists (on homepage)
    if (form) {
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
            .then(response => {
                if (!response.ok) {
                    // Server returned an error response (4xx or 5xx)
                    return response.json().then(errorData => {
                        throw new Error(errorData.error || 'Lỗi không xác định từ server');
                    });
                }
                return response.json();
            })
            .then(data => {
                // Check if the response indicates an error
                if (data.success === false) {
                    throw new Error(data.error || 'Lỗi không xác định');
                }
                renderLaSoTuVi(data);
                resultContainer.style.display = 'block';
                resultContainer.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error('Error details:', error);
                // Display the actual error message to the user
                alert('Có lỗi xảy ra khi lập lá số:\n\n' + error.message + '\n\nVui lòng kiểm tra lại thông tin nhập và thử lại!');
            });
        });
    }
});

// NOTE: Render Tuần and Triệt markers
// If they are at the same position, render combined "TUẦN - TRIỆT" marker
function renderTuanTrietMarkers(thapNhiCung) {
    console.log('renderTuanTrietMarkers called');

    const container = document.getElementById('tuan-markers-container');
    if (!container) {
        console.warn('tuan-markers-container not found');
        return;
    }

    // Clear existing markers
    container.innerHTML = '';

    // Find Tuần cung pairs
    const tuanCungs = [];
    for (let i = 1; i <= 12; i++) {
        if (thapNhiCung[i] && thapNhiCung[i].tuanTrung === true) {
            tuanCungs.push(i);
        }
    }

    // Find Triệt cung pairs
    const trietCungs = [];
    for (let i = 1; i <= 12; i++) {
        if (thapNhiCung[i] && thapNhiCung[i].trietLo === true) {
            trietCungs.push(i);
        }
    }

    console.log('Found tuanCungs:', tuanCungs);
    console.log('Found trietCungs:', trietCungs);

    // Position map for all possible pairs
    const positionMap = {
        '1-2': 'ty-suu',
        '3-4': 'dan-mao',
        '5-6': 'thin-ty',
        '7-8': 'ngo-mui',
        '9-10': 'than-dau',
        '11-12': 'tuat-hoi'
    };

    // Get pair keys
    const tuanPairKey = tuanCungs.length === 2 ? `${tuanCungs.sort((a, b) => a - b).join('-')}` : null;
    const trietPairKey = trietCungs.length === 2 ? `${trietCungs.sort((a, b) => a - b).join('-')}` : null;

    console.log('Tuần pair:', tuanPairKey);
    console.log('Triệt pair:', trietPairKey);

    // Check if Tuần and Triệt are at the same position
    if (tuanPairKey && trietPairKey && tuanPairKey === trietPairKey) {
        // Same position: render combined marker
        console.log('Tuần and Triệt at same position, rendering combined marker');
        const positionClass = positionMap[tuanPairKey];
        if (positionClass) {
            const marker = document.createElement('div');
            marker.className = `tuan-marker ${positionClass}`;
            marker.textContent = 'TUẦN - TRIỆT';
            container.appendChild(marker);
            console.log('Combined TUẦN - TRIỆT marker created');
        }
    } else {
        // Different positions: render separate markers
        // Render Tuần marker
        if (tuanPairKey) {
            const positionClass = positionMap[tuanPairKey];
            if (positionClass) {
                const marker = document.createElement('div');
                marker.className = `tuan-marker ${positionClass}`;
                marker.textContent = 'TUẦN';
                container.appendChild(marker);
                console.log('TUẦN marker created at', tuanPairKey);
            }
        }

        // Render Triệt marker
        if (trietPairKey) {
            const positionClass = positionMap[trietPairKey];
            if (positionClass) {
                const marker = document.createElement('div');
                marker.className = `triet-marker ${positionClass}`;
                marker.textContent = 'TRIỆT';
                container.appendChild(marker);
                console.log('TRIỆT marker created at', trietPairKey);
            }
        }
    }
}

function renderLaSoTuVi(data) {
    // NOTE: Validate data before processing
    if (!data || !data.thienBan || !data.thapNhiCung) {
        console.error('Invalid data received:', data);
        throw new Error('Dữ liệu trả về từ server không hợp lệ. Vui lòng thử lại!');
    }

    const thienBan = data.thienBan;
    // NOTE: Convert thapNhiCung from object to array if needed
    let thapNhiCung = data.thapNhiCung;
    if (!Array.isArray(thapNhiCung)) {
        // Convert object to array (handles both dict and list serialization)
        thapNhiCung = Object.values(thapNhiCung).map(value => {
            // If the value is a number (index), skip it
            if (typeof value === 'object' && value !== null) {
                return value;
            }
            return null;
        }).filter(v => v !== null);

        // If conversion failed, try direct object access with numeric keys
        if (thapNhiCung.length === 0) {
            thapNhiCung = [];
            for (let i = 0; i <= 12; i++) {
                if (data.thapNhiCung[i]) {
                    thapNhiCung[i] = data.thapNhiCung[i];
                }
            }
        }
    }

    const namXem = data.namXem;
    const tuoiAmLich = data.tuoiAmLich;
    const namXemCanChi = data.namXemCanChi;
    const ngayAmXem = data.ngayAmXem;
    const thangAmXem = data.thangAmXem;
    const ngayXemCanChi = data.ngayXemCanChi;

    // Lưu lại data để có thể re-render khi toggle checkbox
    window.currentLaSoData = data;
    window.currentLaSoData.thapNhiCung = thapNhiCung; // Save converted array

    renderThienBan(thienBan, thapNhiCung, namXem, tuoiAmLich, namXemCanChi, thangAmXem);
    renderThapNhiCung(thapNhiCung, thienBan, ngayAmXem, thangAmXem, ngayXemCanChi);
    renderTuanTrietMarkers(thapNhiCung);

    // Attach event listener cho checkbox (chỉ attach 1 lần)
    attachDisplayOptionsListener();
}

// NOTE: Helper function to get time range from Địa Chi name
function getGioTimeRange(chiName) {
    const gioMapping = {
        'Tý': '23h-1h',
        'Sửu': '1h-3h',
        'Dần': '3h-5h',
        'Mão': '5h-7h',
        'Thìn': '7h-9h',
        'Tỵ': '9h-11h',
        'Ngọ': '11h-13h',
        'Mùi': '13h-15h',
        'Thân': '15h-17h',
        'Dậu': '17h-19h',
        'Tuất': '19h-21h',
        'Hợi': '21h-23h'
    };
    return gioMapping[chiName] || '';
}

function renderThienBan(thienBan, thapNhiCung, namXem, tuoiAmLich, namXemCanChi, thangAmXem) {
    const thienBanContent = document.querySelector('.thien-ban-content');

    // NOTE: Find which palace has cungThan = True to get the palace name for "Thân cư"
    const cungThanCu = thapNhiCung.find(cung => cung.cungThan === true);
    const thanCuValue = cungThanCu ? cungThanCu.cungChu : '(Không xác định)';

    // NOTE: Extract Địa Chi from gioSinh (e.g., "Mậu Dần" -> "Dần")
    const chiGio = thienBan.chiGioSinh.tenChi;
    const timeRange = getGioTimeRange(chiGio);
    const gioSinhDisplay = timeRange ? `${timeRange} - ${thienBan.gioSinh}` : thienBan.gioSinh;

    // NOTE: Format năm xem with lunar age and Can Chi if available
    let namXemDisplay = namXem || '(Chưa chọn)';
    if (namXem && tuoiAmLich && namXemCanChi) {
        namXemDisplay = `${namXem} (${tuoiAmLich} tuổi) - ${namXemCanChi}`;
    } else if (namXem && tuoiAmLich) {
        namXemDisplay = `${namXem} (${tuoiAmLich} tuổi)`;
    }

    const html = `
        <p><strong>Họ tên:</strong> <span class="value">${thienBan.ten}</span></p>
        <p><strong>Năm sinh:</strong> <span class="value">${thienBan.namDuong} - ${thienBan.canNamTen} ${thienBan.chiNamTen}</span></p>
        <p><strong>Tháng sinh:</strong> <span class="value">${thienBan.thangDuong} (${thienBan.thangAm}) - ${thienBan.canThangTen} ${thienBan.chiThangTen}</span></p>
        <p><strong>Ngày sinh:</strong> <span class="value">${thienBan.ngayDuong} (${thienBan.ngayAm}) - ${thienBan.canNgayTen} ${thienBan.chiNgayTen}</span></p>
        <p><strong>Giờ sinh:</strong> <span class="value">${gioSinhDisplay}</span></p>
        <p><strong>Năm xem:</strong> <span class="value">${namXemDisplay}</span></p>
        <p><strong>Âm dương:</strong> <span class="value">${thienBan.amDuongNamSinh} ${thienBan.namNu}</span></p>
        <p><strong>Mệnh:</strong> <span class="value">${thienBan.banMenh}</span></p>
        <p><strong>Cục:</strong> <span class="value">${thienBan.tenCuc}</span></p>
        <p><strong>Chủ mệnh:</strong> <span class="value">${thienBan.menhChu}</span></p>
        <p><strong>Chủ thân:</strong> <span class="value">${thienBan.thanChu}</span></p>
        <p><strong>Thân cư:</strong> <span class="value">${thanCuValue}</span></p>
    `;

    thienBanContent.innerHTML = html;
}

function renderThapNhiCung(thapNhiCung, thienBan, ngayAmXem, thangAmXem, ngayXemCanChi) {
    // Kiểm tra trạng thái checkbox (mặc định TẮT = false = chỉ hiện sao quan trọng)
    const hienPhusao = document.getElementById('hienphusao')?.checked ?? false;
    const hienSaoLuuDaiVan = document.getElementById('hiensaoluudaivan')?.checked ?? false;
    const hienSaoLuuTieuVan = document.getElementById('hiensaoluutieuan')?.checked ?? false;
    const hienSaoLuuNguyetVan = document.getElementById('hiensaoluunguyetvan')?.checked ?? false;
    const hienSaoLuuNhatVan = document.getElementById('hiensaoluunhatvan')?.checked ?? false;

    // NOTE: Lưu lại cung đang được highlight trước khi re-render
    const savedHighlightedCung = currentHighlightedCung;

    thapNhiCung.forEach(cung => {
        if (cung.cungSo === 0) return;

        const cungElement = document.getElementById(`cung-${cung.cungSo}`);
        if (!cungElement) return;

        let html = '';

        // Header: Can Chi (trái) - Tên cung (giữa) - Đại hạn (phải)
        html += '<div class="cung-header">';

        // NOTE: Can Chi viết tắt - góc trái trên (ví dụ: K. Tỵ cho Kỷ Tỵ, M. Thìn cho Mậu Thìn)
        const canChiCung = cung.cungCan ? `${cung.cungCan.charAt(0)}. ${cung.cungTen}` : cung.cungTen;
        html += `<div class="cung-ten-chi">${canChiCung}</div>`;

        // Tên cung - giữa trên
        if (cung.cungChu) {
            let cungChuLabel = cung.cungChu.toUpperCase();
            if (cung.cungThan) {
                console.log(`DEBUG: Cung ${cung.cungChu} có cungThan = true`);
                cungChuLabel += ' [THÂN]';
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

            // NOTE: Helper functions to check star types
            const isSaoLuuDaiVan = (sao) => sao.saoTen && sao.saoTen.startsWith('L.') && sao.saoTen.endsWith('.ĐV');
            const isSaoLuuTieuVan = (sao) => sao.saoTen && sao.saoTen.startsWith('L.') && sao.saoTen.endsWith('.TV');
            const isSaoLuuNguyetVan = (sao) => sao.saoTen && sao.saoTen.startsWith('L.') && sao.saoTen.endsWith('.T');
            const isSaoLuuNhatVan = (sao) => sao.saoTen && sao.saoTen.startsWith('L.') && sao.saoTen.endsWith('.N');

            if (!hienPhusao) {
                // NOTE: Hiển thị 32 sao quan trọng + Sao Lưu Đại Vận + Sao Lưu Tiểu Vận + Sao Lưu Nguyệt Vận + Sao Lưu Nhật Vận (nếu checkbox tương ứng được bật)
                danhSachSaoHienThi = cung.cungSao.filter(sao =>
                    SAO_QUAN_TRONG_IDS.includes(sao.saoID) ||
                    (hienSaoLuuDaiVan && isSaoLuuDaiVan(sao)) ||
                    (hienSaoLuuTieuVan && isSaoLuuTieuVan(sao)) ||
                    (hienSaoLuuNguyetVan && isSaoLuuNguyetVan(sao)) ||
                    (hienSaoLuuNhatVan && isSaoLuuNhatVan(sao))
                );
            }

            // NOTE: Lọc bỏ sao lưu đại vận nếu checkbox không được chọn
            if (!hienSaoLuuDaiVan) {
                danhSachSaoHienThi = danhSachSaoHienThi.filter(sao => !isSaoLuuDaiVan(sao));
            }

            // NOTE: Lọc bỏ sao lưu tiểu vận nếu checkbox không được chọn
            if (!hienSaoLuuTieuVan) {
                danhSachSaoHienThi = danhSachSaoHienThi.filter(sao => !isSaoLuuTieuVan(sao));
            }

            // NOTE: Lọc bỏ sao lưu nguyệt vận nếu checkbox không được chọn
            if (!hienSaoLuuNguyetVan) {
                danhSachSaoHienThi = danhSachSaoHienThi.filter(sao => !isSaoLuuNguyetVan(sao));
            }

            // NOTE: Lọc bỏ sao lưu nhật vận nếu checkbox không được chọn
            if (!hienSaoLuuNhatVan) {
                danhSachSaoHienThi = danhSachSaoHienThi.filter(sao => !isSaoLuuNhatVan(sao));
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

            // NOTE: Hiển thị chính tinh ở trên cùng và giữa cung - LUÔN dành 2 dòng cho chính tinh
            html += '<div class="cung-chinh-tinh">';
            if (chinhTinh.length > 0) {
                chinhTinh.forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-chinh ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });
                // NOTE: Nếu chỉ có 1 chính tinh, thêm 1 dòng placeholder để đủ 2 dòng
                if (chinhTinh.length === 1) {
                    html += '<div class="sao-item sao-chinh" style="visibility: hidden;">.</div>';
                }
            } else {
                // NOTE: Không có chính tinh thì để trống 2 dòng
                html += '<div class="sao-item sao-chinh" style="visibility: hidden;">.</div>';
                html += '<div class="sao-item sao-chinh" style="visibility: hidden;">.</div>';
            }
            html += '</div>';

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
                const thienHinhID = 73;

                // 1. Hiển thị 6 hung tinh (in đậm)
                saoXau.filter(sao => hungTinhIDs.includes(sao.saoID)).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 2. Hiển thị Thiên Hình (in đậm)
                saoXau.filter(sao => sao.saoID === thienHinhID).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 3. Hiển thị Tứ Hóa (in đậm)
                saoXau.filter(sao => tuHoaIDs.includes(sao.saoID)).forEach(sao => {
                    const hanhClass = getHanhClass(sao.saoNguHanh);
                    const dacTinh = sao.saoDacTinh ? ` (${sao.saoDacTinh})` : '';
                    html += `<div class="sao-item sao-quan-trong ${hanhClass}">${sao.saoTen}${dacTinh}</div>`;
                });

                // 4. Hiển thị các phụ tinh còn lại
                saoXau.filter(sao => !hungTinhIDs.includes(sao.saoID) && !tuHoaIDs.includes(sao.saoID) && sao.saoID !== thienHinhID).forEach(sao => {
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

            // NOTE: Hiển thị Cung Đại Vận ở góc phải dưới (nếu checkbox được bật)
            const hienCungDaiVan = document.getElementById('hiencungdaivan')?.checked ?? false;
            if (hienCungDaiVan && cung.cungDaiVan) {
                html += `<div class="cung-dai-van">${cung.cungDaiVan}</div>`;
            }

            // NOTE: Hiển thị Cung Tiểu Vận ở góc trái dưới (nếu checkbox được bật)
            const hienCungTieuVan = document.getElementById('hiencungtieuan')?.checked ?? false;
            if (hienCungTieuVan && cung.cungTieuVan) {
                html += `<div class="cung-tieu-van">${cung.cungTieuVan}</div>`;
            }

            // NOTE: Hiển thị Hạn tháng (Tháng Lưu Thái Tuế) ở góc phải dưới (nếu checkbox được bật)
            const hienHanThang = document.getElementById('hienhanthang')?.checked ?? false;
            if (hienHanThang && cung.thangLuuThaiTue) {
                // Format: "T.1 (T.Tỵ)" if Can Chi available, otherwise "Tháng 1"
                const thangDisplay = cung.thangLuuThaiTueCanChi
                    ? `T.${cung.thangLuuThaiTue} (${cung.thangLuuThaiTueCanChi})`
                    : `Tháng ${cung.thangLuuThaiTue}`;
                // NOTE: Bold if matches thangAmXem
                const isBold = thangAmXem && cung.thangLuuThaiTue === thangAmXem;
                const styleClass = isBold ? 'thang-luu-thai-tue bold' : 'thang-luu-thai-tue';
                html += `<div class="${styleClass}">${thangDisplay}</div>`;
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

            // Hiển thị ngày vận ở góc trái dưới khi checkbox được bật
            const hienNgayVan = document.getElementById('hienngayvan')?.checked ?? false;

            if (hienNgayVan && cung.ngayThang && cung.ngayThang.length > 0) {
                // Hiển thị các số ngày, riêng ngày trùng với ngày xem thì in đậm và có Can Chi
                const ngayStrArray = cung.ngayThang.map(ngay => {
                    if (ngay === ngayAmXem && ngayXemCanChi) {
                        return `<span class="bold">${ngay} (${ngayXemCanChi})</span>`;
                    }
                    return ngay.toString();
                });
                html += `<div class="ngay-thang">${ngayStrArray.join(',')}</div>`;
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
            el.style.background = '#fef9f3';
            el.style.border = 'none';
        });
        currentHighlightedCung = null;
        return;
    }

    // Reset tất cả về trạng thái ban đầu
    document.querySelectorAll('.cung').forEach(el => {
        el.style.background = '#fef9f3';
        el.style.border = 'none';
    });

    // Highlight cung được click (chính cung)
    const clickedCung = document.getElementById(`cung-${cungSo}`);
    if (clickedCung) {
        clickedCung.style.background = '#fff3cd';
        clickedCung.style.border = 'none';
    }

    // Highlight cung đối diện
    const doiCung = (cungSo + 6) % 12;
    const doiCungElement = document.getElementById(`cung-${doiCung === 0 ? 12 : doiCung}`);
    if (doiCungElement) {
        doiCungElement.style.background = '#f8d7da';
        doiCungElement.style.border = 'none';
    }

    // Highlight 2 cung tam hợp
    const tamHop1 = (cungSo + 4) % 12;
    const tamHop2 = (cungSo + 8) % 12;
    [tamHop1, tamHop2].forEach(tc => {
        const el = document.getElementById(`cung-${tc === 0 ? 12 : tc}`);
        if (el) {
            el.style.background = '#d1ecf1';
            el.style.border = 'none';
        }
    });

    // Lưu lại cung đang được highlight
    currentHighlightedCung = cungSo;
}

// Attach event listener cho checkbox hiển thị phụ tinh, cung đại vận và cung tiểu vận
function attachDisplayOptionsListener() {
    if (displayOptionsListenerAttached) return;

    const hienphusaoCheckbox = document.getElementById('hienphusao');
    const hiencungdaivanCheckbox = document.getElementById('hiencungdaivan');
    const hiencungtieuanCheckbox = document.getElementById('hiencungtieuan');
    const hienhanthangCheckbox = document.getElementById('hienhanthang');
    const hienngayvanCheckbox = document.getElementById('hienngayvan');
    const hiensaoluudaivanCheckbox = document.getElementById('hiensaoluudaivan');
    const hiensaoluutieuanCheckbox = document.getElementById('hiensaoluutieuan');
    const hiensaoluunguyetvanCheckbox = document.getElementById('hiensaoluunguyetvan');
    const hiensaoluunhatvanCheckbox = document.getElementById('hiensaoluunhatvan');

    // NOTE: Handler function to re-render when any display option changes
    const handleDisplayChange = function() {
        if (window.currentLaSoData) {
            renderThapNhiCung(
                window.currentLaSoData.thapNhiCung,
                window.currentLaSoData.thienBan,
                window.currentLaSoData.ngayAmXem,
                window.currentLaSoData.thangAmXem,
                window.currentLaSoData.ngayXemCanChi
            );
        }
    };

    if (hienphusaoCheckbox) {
        hienphusaoCheckbox.addEventListener('change', handleDisplayChange);
    }

    if (hiencungdaivanCheckbox) {
        hiencungdaivanCheckbox.addEventListener('change', handleDisplayChange);
    }

    if (hiencungtieuanCheckbox) {
        hiencungtieuanCheckbox.addEventListener('change', handleDisplayChange);
    }

    if (hienhanthangCheckbox) {
        hienhanthangCheckbox.addEventListener('change', handleDisplayChange);
    }

    if (hienngayvanCheckbox) {
        hienngayvanCheckbox.addEventListener('change', handleDisplayChange);
    }

    if (hiensaoluudaivanCheckbox) {
        hiensaoluudaivanCheckbox.addEventListener('change', handleDisplayChange);
    }

    if (hiensaoluutieuanCheckbox) {
        hiensaoluutieuanCheckbox.addEventListener('change', handleDisplayChange);
    }

    if (hiensaoluunguyetvanCheckbox) {
        hiensaoluunguyetvanCheckbox.addEventListener('change', handleDisplayChange);
    }

    if (hiensaoluunhatvanCheckbox) {
        hiensaoluunhatvanCheckbox.addEventListener('change', handleDisplayChange);
    }

    displayOptionsListenerAttached = true;
}
