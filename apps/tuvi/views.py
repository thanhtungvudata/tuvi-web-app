import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.calculations.DiaBan import diaBan
from core.calculations.ThienBan import lapThienBan

from apps.tuvi.utils import lapDiaBan
from apps.tuvi.models import SavedLaSo, Folder


def api(request):
    now = datetime.datetime.now()
    hoTen = (request.GET.get('hoten'))
    ngaySinh = int(request.GET.get('ngaysinh', now.day))
    thangSinh = int(request.GET.get('thangsinh', now.month))
    namSinh = int(request.GET.get('namsinh', now.year))
    gioiTinh = 1 if request.GET.get('gioitinh') == 'nam' else -1
    gioSinh = int(request.GET.get('giosinh', 1))
    timeZone = int(request.GET.get('muigio', 7))
    duongLich = False if request.GET.get('amlich') == 'on' else True
    db = lapDiaBan(diaBan, ngaySinh, thangSinh, namSinh, gioSinh,
                   gioiTinh, duongLich, timeZone)
    thienBan = lapThienBan(ngaySinh, thangSinh, namSinh,
                           gioSinh, gioiTinh, hoTen, db)
    laso = {
        'thienBan': thienBan,
        'thapNhiCung': db.thapNhiCung
    }
    my_return = (json.dumps(laso, default=lambda o: o.__dict__))
    return HttpResponse(my_return, content_type="application/json")


def lasotuvi_new_index(request):
    """Trang chủ - Form nhập liệu"""
    # Lấy thông tin từ URL nếu có (khi quay lại từ trang kết quả để sửa)
    context = {
        'hoten': request.GET.get('hoten', ''),
        'ngaysinh': request.GET.get('ngaysinh', ''),
        'thangsinh': request.GET.get('thangsinh', ''),
        'namsinh': request.GET.get('namsinh', ''),
        'gioitinh': request.GET.get('gioitinh', 'nam'),
        'giosinh': request.GET.get('giosinh', ''),
        'muigio': request.GET.get('muigio', '7'),
        'amlich': request.GET.get('amlich', 'off'),
    }
    return render(request, 'tuvi/index.html', context)


def lasotuvi_new_result(request):
    """Trang kết quả - Hiển thị lá số"""
    # Lấy thông tin từ GET parameters
    context = {
        'hoten': request.GET.get('hoten', ''),
        'ngaysinh': request.GET.get('ngaysinh', '1'),
        'thangsinh': request.GET.get('thangsinh', '1'),
        'namsinh': request.GET.get('namsinh', '2000'),
        'gioitinh': request.GET.get('gioitinh', 'nam'),
        'giosinh': request.GET.get('giosinh', '1'),
        'muigio': request.GET.get('muigio', '7'),
        'amlich': request.GET.get('amlich', 'off'),
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
                               giosinh, 1 if gioitinh == 'nam' else -1, hoten, db)

        # Tạo chart_data JSON
        chart_data = {
            'thienBan': thienBan.__dict__,
            'thapNhiCung': [cung.__dict__ for cung in db.thapNhiCung]
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
