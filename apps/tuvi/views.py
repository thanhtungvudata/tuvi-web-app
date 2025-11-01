import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.calculations.DiaBan import diaBan
from core.calculations.ThienBan import lapThienBan
from core.calculations.AmDuong import thienCan, diaChi

from apps.tuvi.utils import lapDiaBan
from apps.tuvi.models import SavedLaSo, Folder


def api(request):
    try:
        now = datetime.datetime.now()
        hoTen = (request.GET.get('hoten'))
        # NOTE: Handle empty strings for numeric parameters
        ngaySinh = int(request.GET.get('ngaysinh') or now.day)
        thangSinh = int(request.GET.get('thangsinh') or now.month)
        namSinh = int(request.GET.get('namsinh') or now.year)
        gioiTinh = 1 if request.GET.get('gioitinh') == 'nam' else -1
        gioSinh = int(request.GET.get('giosinh') or 1)
        timeZone = int(request.GET.get('muigio', 7))
        duongLich = False if request.GET.get('amlich') == 'on' else True
        namXem = int(request.GET.get('namxem') or now.year)

        print("="*80)
        print(f"DEBUG API - ALL PARAMS: {dict(request.GET)}")
        print(f"DEBUG API - amlich param: {request.GET.get('amlich')}")
        print(f"DEBUG API - duongLich: {duongLich}")
        print(f"DEBUG API - namxem from request: {request.GET.get('namxem')}")
        print(f"DEBUG API - namXem parsed: {namXem}")
        print(f"DEBUG API - now.year: {now.year}")
        print("="*80)

        db = lapDiaBan(diaBan, ngaySinh, thangSinh, namSinh, gioSinh,
                       gioiTinh, duongLich, timeZone)
        thienBan = lapThienBan(ngaySinh, thangSinh, namSinh,
                               gioSinh, gioiTinh, hoTen, db, duongLich, timeZone)

        # NOTE: Calculate lunar age (Vietnamese traditional age)
        tuoiAmLich = thienBan.tinhTuoiAmLich(namXem)

        # NOTE: Calculate and assign Đại Vận palaces based on lunar age
        _ = db.nhapCungDaiVan(tuoiAmLich)

        # NOTE: Calculate and place Lưu Lộc Tồn Đại Vận star based on Can of Mệnh.ĐV palace
        _ = db.nhapSaoLuuLocTonDaiVan()

        # NOTE: Calculate and place Lưu Kình Dương và Lưu Đà La Đại Vận based on L.Lộc tồn.ĐV
        _ = db.nhapSaoLuuKinhDuongDaLaDaiVan()

        # NOTE: Calculate and place Tứ Hóa Lưu Đại Vận based on Can of Mệnh.ĐV palace
        _ = db.nhapSaoTuHoaLuuDaiVan()

        # NOTE: Calculate Can Chi for namXem (năm âm lịch tương ứng với năm dương lịch)
        # Năm dương lịch thường tương ứng với năm âm lịch cùng số (ví dụ: 2025 DL = Ất Tị 2025 ÂL)
        canNamXem = (namXem + 6) % 10 + 1
        chiNamXem = (namXem + 8) % 12 + 1
        canNamXemTen = thienCan[canNamXem]['tenCan']
        chiNamXemTen = diaChi[chiNamXem]['tenChi']
        namXemCanChi = f"{canNamXemTen} {chiNamXemTen}"

        # NOTE: Calculate and assign Tiểu Vận palaces based on địa chi of namXem
        _ = db.nhapCungTieuVan(chiNamXem)

        # NOTE: Calculate and place Lưu Lộc Tồn Tiểu Vận star based on Can of namXem
        _ = db.nhapSaoLuuLocTonTieuVan(canNamXem)

        # NOTE: Calculate and place Lưu Kình Dương và Lưu Đà La Tiểu Vận based on L.Lộc tồn.TV
        _ = db.nhapSaoLuuKinhDuongDaLaTieuVan()

        # NOTE: Calculate and place Tứ Hóa Lưu Tiểu Vận based on Can of namXem
        _ = db.nhapSaoTuHoaLuuTieuVan(canNamXem)

        # NOTE: An tháng của năm xem theo phái Lưu Thái Tuế
        # IMPORTANT: Use thienBan.thangAm (lunar month) not input thangSinh (may be solar)
        _ = db.nhapThangLuuThaiTue(thienBan.thangAm, gioSinh)

        laso = {
            'thienBan': thienBan,
            'thapNhiCung': db.thapNhiCung,
            'namXem': namXem,
            'tuoiAmLich': tuoiAmLich,
            'namXemCanChi': namXemCanChi
        }

        # NOTE: Custom JSON serializer that handles both objects and dicts
        def serialize_object(obj):
            if isinstance(obj, dict):
                # Already a dict, return as-is
                return obj
            elif hasattr(obj, '__dict__'):
                # Has __dict__ attribute, convert to dict
                return obj.__dict__
            else:
                # Primitive type, return as-is
                return obj

        my_return = (json.dumps(laso, default=serialize_object))
        return HttpResponse(my_return, content_type="application/json")
    except ValueError as e:
        # Handle invalid input values (e.g., invalid date, non-numeric input)
        error_msg = f"Dữ liệu nhập không hợp lệ: {str(e)}"
        print(f"ERROR API - ValueError: {error_msg}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=400)
    except Exception as e:
        # Handle any other unexpected errors
        error_msg = f"Lỗi khi tính toán lá số: {str(e)}"
        print(f"ERROR API - Exception: {error_msg}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=500)


def lasotuvi_new_index(request):
    """Trang chủ - Form nhập liệu"""
    # Lấy thông tin từ URL nếu có (khi quay lại từ trang kết quả để sửa)
    now = datetime.datetime.now()
    current_year = now.year
    year_range = list(range(1900, 2101))

    context = {
        'hoten': request.GET.get('hoten', ''),
        'ngaysinh': request.GET.get('ngaysinh', ''),
        'thangsinh': request.GET.get('thangsinh', ''),
        'namsinh': request.GET.get('namsinh', ''),
        'gioitinh': request.GET.get('gioitinh', 'nam'),
        'giosinh': request.GET.get('giosinh', ''),
        'muigio': request.GET.get('muigio', '7'),
        'amlich': request.GET.get('amlich', 'off'),
        'namxem': int(request.GET.get('namxem', str(current_year))),
        'year_range': year_range,
    }
    print(f"DEBUG index - namxem: {context['namxem']}, year_range length: {len(year_range)}, type: {type(year_range)}")
    return render(request, 'tuvi/index.html', context)


def lasotuvi_new_result(request):
    """Trang kết quả - Hiển thị lá số"""
    # NOTE: Check if loading from saved laso
    laso_id = request.GET.get('laso_id')
    now = datetime.datetime.now()
    current_year = now.year
    year_range = list(range(1900, 2101))

    if laso_id:
        # Load from saved laso
        try:
            laso = SavedLaSo.objects.get(id=laso_id)
            context = {
                'hoten': laso.hoten,
                'ngaysinh': str(laso.ngaysinh),
                'thangsinh': str(laso.thangsinh),
                'namsinh': str(laso.namsinh),
                'gioitinh': laso.gioitinh,
                'giosinh': str(laso.giosinh),
                'muigio': str(laso.muigio),
                'amlich': 'on' if laso.amlich else 'off',
                'namxem': current_year,
                'year_range': year_range,
            }
        except SavedLaSo.DoesNotExist:
            # If laso not found, use default values
            context = {
                'hoten': '',
                'ngaysinh': '1',
                'thangsinh': '1',
                'namsinh': '2000',
                'gioitinh': 'nam',
                'giosinh': '1',
                'muigio': '7',
                'amlich': 'off',
                'namxem': current_year,
                'year_range': year_range,
            }
    else:
        # Load from GET parameters
        context = {
            'hoten': request.GET.get('hoten', ''),
            'ngaysinh': request.GET.get('ngaysinh', '1'),
            'thangsinh': request.GET.get('thangsinh', '1'),
            'namsinh': request.GET.get('namsinh', '2000'),
            'gioitinh': request.GET.get('gioitinh', 'nam'),
            'giosinh': request.GET.get('giosinh', '1'),
            'muigio': request.GET.get('muigio', '7'),
            'amlich': request.GET.get('amlich', 'off'),
            'namxem': int(request.GET.get('namxem', str(current_year))),
            'year_range': year_range,
        }
    return render(request, 'tuvi/result.html', context)


def lasotuvi_new_manage(request):
    """Trang quản lý lá số"""
    return render(request, 'tuvi/manage.html')


@csrf_exempt
@require_http_methods(["POST"])
def save_laso(request):
    """API để lưu lá số mới"""
    try:
        data = json.loads(request.body)
        print(f"DEBUG save_laso - Received data: {data}")

        # Lấy thông tin từ request
        laso_name = data.get('name')
        hoten = data.get('hoten')
        ngaysinh = int(data.get('ngaysinh')) if data.get('ngaysinh') else None
        thangsinh = int(data.get('thangsinh')) if data.get('thangsinh') else None
        namsinh = int(data.get('namsinh')) if data.get('namsinh') else None
        giosinh = int(data.get('giosinh')) if data.get('giosinh') else None
        gioitinh = data.get('gioitinh')
        amlich = data.get('amlich') == 'on'
        muigio = int(data.get('muigio')) if data.get('muigio') else 7
        namxem = int(data.get('namxem')) if data.get('namxem') else None
        folder_id = data.get('folder_id')
        new_folder_name = data.get('new_folder_name')

        # Xử lý thư mục
        folder = None
        if new_folder_name:
            # Tạo thư mục mới
            folder, created = Folder.objects.get_or_create(name=new_folder_name)
        elif folder_id and folder_id != "":
            # Dùng thư mục có sẵn (chỉ khi folder_id không rỗng)
            try:
                folder = Folder.objects.get(id=int(folder_id))
            except (Folder.DoesNotExist, ValueError):
                pass

        # Tính toán lá số (giống API hiện tại)
        duongLich = not amlich
        db = lapDiaBan(diaBan, ngaysinh, thangsinh, namsinh, giosinh,
                       1 if gioitinh == 'nam' else -1, duongLich, muigio)
        thienBan = lapThienBan(ngaysinh, thangsinh, namsinh,
                               giosinh, 1 if gioitinh == 'nam' else -1, hoten, db, duongLich, muigio)

        # NOTE: Calculate lunar age if namxem is provided
        tuoiAmLich = thienBan.tinhTuoiAmLich(namxem) if namxem else None

        # NOTE: Calculate and assign Đại Vận palaces if age is available
        if tuoiAmLich:
            _ = db.nhapCungDaiVan(tuoiAmLich)
            # NOTE: Calculate and place Lưu Lộc Tồn Đại Vận star
            _ = db.nhapSaoLuuLocTonDaiVan()
            # NOTE: Calculate and place Lưu Kình Dương và Lưu Đà La Đại Vận
            _ = db.nhapSaoLuuKinhDuongDaLaDaiVan()
            # NOTE: Calculate and place Tứ Hóa Lưu Đại Vận
            _ = db.nhapSaoTuHoaLuuDaiVan()

        # NOTE: Calculate Can Chi for namxem if provided
        namXemCanChi = None
        if namxem:
            canNamXem = (namxem + 6) % 10 + 1
            chiNamXem = (namxem + 8) % 12 + 1
            canNamXemTen = thienCan[canNamXem]['tenCan']
            chiNamXemTen = diaChi[chiNamXem]['tenChi']
            namXemCanChi = f"{canNamXemTen} {chiNamXemTen}"

            # NOTE: Calculate and assign Tiểu Vận palaces based on địa chi of namxem
            _ = db.nhapCungTieuVan(chiNamXem)

            # NOTE: Calculate and place Lưu Lộc Tồn Tiểu Vận star based on Can of namxem
            _ = db.nhapSaoLuuLocTonTieuVan(canNamXem)

            # NOTE: Calculate and place Lưu Kình Dương và Lưu Đà La Tiểu Vận
            _ = db.nhapSaoLuuKinhDuongDaLaTieuVan()

            # NOTE: Calculate and place Tứ Hóa Lưu Tiểu Vận based on Can of namxem
            _ = db.nhapSaoTuHoaLuuTieuVan(canNamXem)

            # NOTE: An tháng của năm xem theo phái Lưu Thái Tuế
            # IMPORTANT: Use thienBan.thangAm (lunar month) not input thangsinh (may be solar)
            _ = db.nhapThangLuuThaiTue(thienBan.thangAm, giosinh)

        # Tạo chart_data JSON
        chart_data = {
            'thienBan': thienBan.__dict__,
            'thapNhiCung': [cung.__dict__ for cung in db.thapNhiCung],
            'namXem': namxem,
            'tuoiAmLich': tuoiAmLich,
            'namXemCanChi': namXemCanChi
        }

        # Lưu vào database
        saved_laso = SavedLaSo.objects.create(
            name=laso_name,
            hoten=hoten,
            ngaysinh=ngaysinh,
            thangsinh=thangsinh,
            namsinh=namsinh,
            giosinh=giosinh,
            gioitinh=gioitinh,
            amlich=amlich,
            muigio=muigio,
            namxem=namxem,
            folder=folder,
            chart_data=chart_data
        )

        return JsonResponse({
            'success': True,
            'message': 'Lưu lá số thành công!',
            'laso_id': saved_laso.id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }, status=400)


@require_http_methods(["GET"])
def get_lasos(request):
    """API để lấy danh sách lá số"""
    filter_type = request.GET.get('filter', 'all')  # all, favorites, folder_id

    if filter_type == 'favorites':
        lasos = SavedLaSo.objects.filter(is_favorite=True)
    elif filter_type.startswith('folder_'):
        folder_id = filter_type.replace('folder_', '')
        lasos = SavedLaSo.objects.filter(folder_id=folder_id)
    else:
        lasos = SavedLaSo.objects.all()

    data = [{
        'id': laso.id,
        'name': laso.name,
        'hoten': laso.hoten,
        'ngaysinh': laso.ngaysinh,
        'thangsinh': laso.thangsinh,
        'namsinh': laso.namsinh,
        'giosinh': laso.giosinh,
        'gioitinh': laso.gioitinh,
        'amlich': laso.amlich,
        'muigio': laso.muigio,
        'is_favorite': laso.is_favorite,
        'folder_name': laso.folder.name if laso.folder else None,
        'created_at': laso.created_at.strftime('%d/%m/%Y %H:%M')
    } for laso in lasos]

    return JsonResponse({'lasos': data})


@require_http_methods(["GET"])
def get_laso_detail(request, laso_id):
    """API để lấy chi tiết lá số (bao gồm chart_data)"""
    try:
        laso = SavedLaSo.objects.get(id=laso_id)
        return JsonResponse({
            'success': True,
            'laso': {
                'id': laso.id,
                'name': laso.name,
                'hoten': laso.hoten,
                'ngaysinh': laso.ngaysinh,
                'thangsinh': laso.thangsinh,
                'namsinh': laso.namsinh,
                'giosinh': laso.giosinh,
                'gioitinh': laso.gioitinh,
                'amlich': laso.amlich,
                'muigio': laso.muigio,
                'chart_data': laso.chart_data,  # Trả về toàn bộ JSON đã lưu
                'is_favorite': laso.is_favorite
            }
        })
    except SavedLaSo.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy lá số'
        }, status=404)


@require_http_methods(["GET"])
def get_folders(request):
    """API để lấy danh sách thư mục"""
    folders = Folder.objects.all()
    data = [{
        'id': folder.id,
        'name': folder.name,
        'laso_count': folder.lasos.count(),
        'created_at': folder.created_at.strftime('%d/%m/%Y')
    } for folder in folders]

    return JsonResponse({'folders': data})


@csrf_exempt
@require_http_methods(["POST"])
def update_laso(request):
    """API để cập nhật lá số"""
    try:
        data = json.loads(request.body)
        print("="*80)
        print(f"DEBUG update_laso - Received data: {data}")
        print(f"DEBUG update_laso - namxem value: {data.get('namxem')}")
        print(f"DEBUG update_laso - namxem type: {type(data.get('namxem'))}")
        print("="*80)
        laso_id = data.get('laso_id')

        if not laso_id:
            print("DEBUG update_laso - Missing laso_id")
            return JsonResponse({
                'success': False,
                'message': 'Thiếu laso_id'
            }, status=400)

        laso = SavedLaSo.objects.get(id=laso_id)

        # Cập nhật thông tin lá số
        laso.hoten = data.get('hoten', '')
        laso.ngaysinh = int(data.get('ngaysinh', 1))
        laso.thangsinh = int(data.get('thangsinh', 1))
        laso.namsinh = int(data.get('namsinh', 2000))
        laso.giosinh = int(data.get('giosinh', 1))
        laso.gioitinh = data.get('gioitinh', 'nam')
        laso.amlich = data.get('amlich', 'off') == 'on'
        laso.muigio = int(data.get('muigio', 7))
        laso.namxem = int(data.get('namxem')) if data.get('namxem') else None

        # Tính toán lại chart_data với thông tin mới
        duongLich = not laso.amlich
        db = lapDiaBan(diaBan, laso.ngaysinh, laso.thangsinh, laso.namsinh, laso.giosinh,
                       1 if laso.gioitinh == 'nam' else -1, duongLich, laso.muigio)
        thienBan = lapThienBan(laso.ngaysinh, laso.thangsinh, laso.namsinh,
                               laso.giosinh, 1 if laso.gioitinh == 'nam' else -1, laso.hoten, db, duongLich, laso.muigio)

        # NOTE: Calculate lunar age if namxem is provided
        tuoiAmLich = thienBan.tinhTuoiAmLich(laso.namxem) if laso.namxem else None

        # NOTE: Calculate and assign Đại Vận palaces if age is available
        if tuoiAmLich:
            _ = db.nhapCungDaiVan(tuoiAmLich)
            # NOTE: Calculate and place Lưu Lộc Tồn Đại Vận star
            _ = db.nhapSaoLuuLocTonDaiVan()
            # NOTE: Calculate and place Lưu Kình Dương và Lưu Đà La Đại Vận
            _ = db.nhapSaoLuuKinhDuongDaLaDaiVan()
            # NOTE: Calculate and place Tứ Hóa Lưu Đại Vận
            _ = db.nhapSaoTuHoaLuuDaiVan()

        # NOTE: Calculate Can Chi for namxem if provided
        namXemCanChi = None
        if laso.namxem:
            canNamXem = (laso.namxem + 6) % 10 + 1
            chiNamXem = (laso.namxem + 8) % 12 + 1
            canNamXemTen = thienCan[canNamXem]['tenCan']
            chiNamXemTen = diaChi[chiNamXem]['tenChi']
            namXemCanChi = f"{canNamXemTen} {chiNamXemTen}"

            # NOTE: Calculate and assign Tiểu Vận palaces based on địa chi of namxem
            _ = db.nhapCungTieuVan(chiNamXem)

            # NOTE: Calculate and place Lưu Lộc Tồn Tiểu Vận star based on Can of namxem
            _ = db.nhapSaoLuuLocTonTieuVan(canNamXem)

            # NOTE: Calculate and place Lưu Kình Dương và Lưu Đà La Tiểu Vận
            _ = db.nhapSaoLuuKinhDuongDaLaTieuVan()

            # NOTE: Calculate and place Tứ Hóa Lưu Tiểu Vận based on Can of namxem
            _ = db.nhapSaoTuHoaLuuTieuVan(canNamXem)

            # NOTE: An tháng của năm xem theo phái Lưu Thái Tuế
            # IMPORTANT: Use thienBan.thangAm (lunar month) not input thangsinh (may be solar)
            _ = db.nhapThangLuuThaiTue(thienBan.thangAm, laso.giosinh)

        # Tạo chart_data JSON
        laso.chart_data = {
            'thienBan': thienBan.__dict__,
            'thapNhiCung': [cung.__dict__ for cung in db.thapNhiCung],
            'namXem': laso.namxem,
            'tuoiAmLich': tuoiAmLich,
            'namXemCanChi': namXemCanChi
        }

        laso.save()

        return JsonResponse({
            'success': True,
            'message': 'Đã cập nhật lá số thành công!'
        })

    except SavedLaSo.DoesNotExist:
        print("DEBUG update_laso - Laso not found")
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy lá số'
        }, status=404)
    except Exception as e:
        print(f"DEBUG update_laso - Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_laso(request, laso_id):
    """API để xoá lá số"""
    try:
        laso = SavedLaSo.objects.get(id=laso_id)
        laso.delete()
        return JsonResponse({
            'success': True,
            'message': 'Đã xoá lá số thành công!'
        })
    except SavedLaSo.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy lá số'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_folder(request, folder_id):
    """API để xoá thư mục"""
    try:
        folder = Folder.objects.get(id=folder_id)
        # Kiểm tra xem thư mục có lá số không
        laso_count = folder.lasos.count()
        if laso_count > 0:
            return JsonResponse({
                'success': False,
                'message': f'Không thể xoá thư mục có {laso_count} lá số. Vui lòng xoá các lá số trước.'
            }, status=400)

        folder.delete()
        return JsonResponse({
            'success': True,
            'message': 'Đã xoá thư mục thành công!'
        })
    except Folder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy thư mục'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def toggle_favorite_laso(request, laso_id):
    """API để chuyển đổi trạng thái yêu thích của lá số"""
    try:
        laso = SavedLaSo.objects.get(id=laso_id)
        laso.is_favorite = not laso.is_favorite
        laso.save()
        return JsonResponse({
            'success': True,
            'is_favorite': laso.is_favorite,
            'message': 'Đã thêm vào yêu thích!' if laso.is_favorite else 'Đã bỏ khỏi yêu thích!'
        })
    except SavedLaSo.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy lá số'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def move_laso(request, laso_id):
    """API để di chuyển lá số sang thư mục khác"""
    try:
        import json
        data = json.loads(request.body)
        folder_id = data.get('folder_id')

        laso = SavedLaSo.objects.get(id=laso_id)

        if folder_id:
            folder = Folder.objects.get(id=folder_id)
            laso.folder = folder
            folder_name = folder.name
        else:
            laso.folder = None
            folder_name = "Tất cả lá số"

        laso.save()
        return JsonResponse({
            'success': True,
            'message': f'Đã di chuyển lá số đến "{folder_name}"!'
        })
    except SavedLaSo.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy lá số'
        }, status=404)
    except Folder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy thư mục'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }, status=400)
