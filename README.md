# Face Recognition Attendance System 

Ứng dụng desktop điểm danh tự động bằng **nhận diện khuôn mặt**, phục vụ cho lớp học,phòng lab hoặc doanh nghiệp nhỏ.
Ứng dụng cho phép đăng ký người dùng mới, xác thực khuôn mặt qua camera thời gian thực và lưu lịch sử điểm danh.


# Tính năng chính

* Đăng ký khuôn mặt người dùng mới thông qua camera
* Nhận diện và đăng nhập bằng khuôn mặt (real-time)
* Điểm danh tự động và lưu thời gian điểm danh
* Xuất và xem lịch sử điểm danh dưới dạng file Excel
* Giao diện desktop trực quan, dễ sử dụng


# Công nghệ sử dụng

* Ngôn ngữ: Python
* Computer Vision: OpenCV
* Nhận diện khuôn mặt: DeepFace
* Giao diện: Tkinter
* Xử lý ảnh: Pillow (PIL)
* Lưu trữ dữ liệu: Excel (OpenPyXL)


# Cài đặt & Chạy chương trình
1. Cài đặt thư viện cần thiết
pip install opencv-python deepface pillow openpyxl tensorflow
2. Chạy ứng dụng
python main.py

# Quy trình hoạt động

1. Người dùng nhập tên và đăng ký khuôn mặt
2. Ảnh khuôn mặt được lưu vào thư mục `face_db`
3. Khi đăng nhập, hệ thống chụp ảnh từ camera
4. DeepFace so khớp khuôn mặt với dữ liệu đã lưu
5. Nếu khớp, hệ thống ghi nhận điểm danh và lưu vào Excel

# Điểm nổi bật kỹ thuật

* Ứng dụng mô hình Deep Learning thông qua thư viện DeepFace
* Xử lý camera và hình ảnh thời gian thực bằng OpenCV
* Thiết kế theo hướng lập trình hướng đối tượng (OOP)
* Quản lý dữ liệu điểm danh đơn giản, dễ mở rộng

# Tác giả
* **Ma Thế Chuyền**
* Sinh viên Công nghệ Thông tin – Trường Đại học Tây Nguyên
