from django.db import models


class Folder(models.Model):
    """Thư mục để tổ chức lá số"""
    name = models.CharField(max_length=200, verbose_name="Tên thư mục")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'lasotuvi_folder'
        ordering = ['-created_at']
        verbose_name = 'Thư mục'
        verbose_name_plural = 'Thư mục'

    def __str__(self):
        return self.name


class SavedLaSo(models.Model):
    """Lá số đã lưu - Lưu cả thông tin đầu vào và kết quả JSON"""
    # Thông tin cơ bản
    name = models.CharField(max_length=200, verbose_name="Tên lá số")

    # Thông tin đầu vào
    hoten = models.CharField(max_length=200, verbose_name="Họ tên")
    ngaysinh = models.IntegerField(verbose_name="Ngày sinh")
    thangsinh = models.IntegerField(verbose_name="Tháng sinh")
    namsinh = models.IntegerField(verbose_name="Năm sinh")
    giosinh = models.IntegerField(verbose_name="Giờ sinh")
    gioitinh = models.CharField(max_length=10, verbose_name="Giới tính")  # 'nam' hoặc 'nu'
    amlich = models.BooleanField(default=False, verbose_name="Âm lịch")
    muigio = models.IntegerField(default=7, verbose_name="Múi giờ")
    namxem = models.IntegerField(null=True, blank=True, verbose_name="Năm xem")

    # Dữ liệu lá số (JSON) - Lưu toàn bộ kết quả đã tính
    chart_data = models.JSONField(verbose_name="Dữ liệu lá số", help_text="JSON chứa thienBan và thapNhiCung")

    # Tổ chức
    folder = models.ForeignKey(
        Folder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lasos',
        verbose_name="Thư mục"
    )
    is_favorite = models.BooleanField(default=False, verbose_name="Yêu thích")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'lasotuvi_saved_laso'
        ordering = ['-created_at']
        verbose_name = 'Lá số đã lưu'
        verbose_name_plural = 'Lá số đã lưu'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_favorite']),
        ]

    def __str__(self):
        return f"{self.name} - {self.hoten}"
