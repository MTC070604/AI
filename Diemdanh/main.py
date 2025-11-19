import cv2
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from deepface import DeepFace
import datetime
import tempfile
import openpyxl
import subprocess

class util:
    @staticmethod
    def msg_box(title, message):
        messagebox.showinfo(title, message)

class FaceRecognitionApp:
    def __init__(self):
        self.db_dir = "face_db"
        self.excel_path = "diem_danh.xlsx"
        os.makedirs(self.db_dir, exist_ok=True)
        self.encode_known_faces()

        self.window = tk.Tk()
        self.window.title("Hệ Thống Điểm Danh Bằng Khuôn Mặt")
        self.window.geometry("600x750")
        self.window.configure(bg="#eaf2f8")

        # ===== TIÊU ĐỀ =====
        tk.Label(
            self.window,
            text="🎓 NHẬN DIỆN KHUÔN MẶT",
            font=("Helvetica", 20, "bold"),
            bg="#eaf2f8",
            fg="#2c3e50"
        ).pack(pady=15)

        # ===== ẢNH CAMERA =====
        self.label = tk.Label(self.window, bg="#bdc3c7", relief="groove", bd=2)
        self.label.pack(pady=10)

        # ===== Ô NHẬP TÊN =====
        self.entry_name = tk.Entry(self.window, font=("Helvetica", 14), justify="center", fg="#555")
        self.entry_name.pack(pady=10)
        self.entry_name.insert(0, "Nhập tên để đăng ký")

        # ===== NÚT =====
        self.create_button("📷 Đăng ký khuôn mặt", self.accept_register_new_user, "#27ae60").pack(pady=8)
        self.create_button("🔒 Đăng nhập bằng khuôn mặt", self.login, "#2980b9").pack(pady=8)
        self.create_button("📁 Xuất file điểm danh", self.open_excel, "#8e44ad").pack(pady=15)

        # ===== CAMERA =====
        self.cap = cv2.VideoCapture(0)
        self.update_frame()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def create_button(self, text, command, bg_color):
        btn = tk.Button(
            self.window,
            text=text,
            command=command,
            font=("Helvetica", 13, "bold"),
            bg=bg_color,
            fg="white",
            activebackground="#34495e",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=6,
            width=30
        )
        return btn

    def encode_known_faces(self):
        self.known_face_paths = []
        self.known_face_names = []

        for filename in os.listdir(self.db_dir):
            if filename.endswith(".jpg"):
                path = os.path.join(self.db_dir, filename)
                self.known_face_paths.append(path)
                self.known_face_names.append(os.path.splitext(filename)[0])

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.most_recent_capture_arr = frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img = img.resize((500, 350))  # Resize cho đẹp
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        self.window.after(10, self.update_frame)

    def login(self):
        rgb_frame = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            temp_path = tmp.name
            cv2.imwrite(temp_path, cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))

        for i, known_path in enumerate(self.known_face_paths):
            try:
                result = DeepFace.verify(img1_path=temp_path, img2_path=known_path, enforce_detection=False)
                if result["verified"]:
                    name = self.known_face_names[i]
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_to_excel(name, now)
                    util.msg_box("✅ Thành công", f"Chào mừng, {name}!\nĐã điểm danh lúc {now}")
                    os.remove(temp_path)
                    return
            except Exception as e:
                print("Lỗi xác thực:", e)
                continue

        os.remove(temp_path)
        util.msg_box("⚠️ Không nhận diện được", "Vui lòng thử lại hoặc đăng ký khuôn mặt.")

    def save_to_excel(self, name, timestamp):
        if not os.path.exists(self.excel_path):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Tên", "Thời gian điểm danh"])
        else:
            wb = openpyxl.load_workbook(self.excel_path)
            ws = wb.active
        ws.append([name, timestamp])
        wb.save(self.excel_path)

    def open_excel(self):
        if os.path.exists(self.excel_path):
            try:
                os.startfile(self.excel_path)  # Windows
            except AttributeError:
                subprocess.call(["open", self.excel_path])  # macOS/Linux
        else:
            util.msg_box("Chưa có dữ liệu", "Chưa có điểm danh nào để xuất.")

    def accept_register_new_user(self):
        name = self.entry_name.get().strip()
        if not name or name == "Nhập tên để đăng ký":
            util.msg_box("Lỗi", "Vui lòng nhập tên hợp lệ.")
            return

        path = os.path.join(self.db_dir, f"{name}.jpg")
        cv2.imwrite(path, self.most_recent_capture_arr)
        util.msg_box("🎉 Thành công", f"Đã lưu khuôn mặt cho {name}")
        self.encode_known_faces()

    def on_closing(self):
        self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    FaceRecognitionApp()