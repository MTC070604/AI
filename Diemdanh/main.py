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

# ================== UTIL ==================
class util:
    @staticmethod
    def msg_box(title, message):
        messagebox.showinfo(title, message)

# ================== APP ==================
class FaceRecognitionApp:
    def __init__(self):
        self.db_dir = "face_db"
        self.excel_path = "diem_danh.xlsx"
        os.makedirs(self.db_dir, exist_ok=True)
        self.encode_known_faces()

        # ===== WINDOW =====
        self.window = tk.Tk()
        self.window.title("Hệ Thống Điểm Danh Khuôn Mặt")
        self.window.geometry("620x780")
        self.window.configure(bg="#f4f6f9")
        self.window.resizable(False, False)

        # ===== TITLE =====
        tk.Label(
            self.window,
            text="🎓 HỆ THỐNG NHẬN DIỆN KHUÔN MẶT",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50"
        ).pack(pady=18)

        # ===== CAMERA FRAME =====
        cam_frame = tk.Frame(self.window, bg="white", bd=0, highlightthickness=2,
                             highlightbackground="#dcdde1")
        cam_frame.pack(pady=10)

        self.label = tk.Label(cam_frame, bg="#ecf0f1")
        self.label.pack(padx=8, pady=8)

        # ===== NAME ENTRY =====
        self.entry_name = tk.Entry(
            self.window,
            font=("Segoe UI", 13),
            justify="center",
            fg="#7f8c8d",
            relief="solid",
            bd=1
        )
        self.entry_name.pack(pady=15, ipady=6, ipadx=10)
        self.entry_name.insert(0, "Nhập tên để đăng ký")

        self.entry_name.bind("<FocusIn>", self.clear_placeholder)
        self.entry_name.bind("<FocusOut>", self.restore_placeholder)

        # ===== BUTTONS =====
        btn_frame = tk.Frame(self.window, bg="#f4f6f9")
        btn_frame.pack(pady=10)

        self.create_button(btn_frame, "📷  Đăng ký khuôn mặt", self.accept_register_new_user, "#27ae60")
        self.create_button(btn_frame, "🔒  Đăng nhập bằng khuôn mặt", self.login, "#2980b9")
        self.create_button(btn_frame, "📁  Xuất file điểm danh", self.open_excel, "#8e44ad")

        # ===== FOOTER =====
        self.status = tk.Label(
            self.window,
            text="Sẵn sàng nhận diện khuôn mặt",
            font=("Segoe UI", 10),
            bg="#f4f6f9",
            fg="#7f8c8d"
        )
        self.status.pack(side="bottom", pady=8)

        # ===== CAMERA =====
        self.cap = cv2.VideoCapture(0)
        self.update_frame()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    # ================== UI ==================
    def create_button(self, parent, text, command, color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 12, "bold"),
            bg=color,
            fg="white",
            activebackground="#2c3e50",
            activeforeground="white",
            relief="flat",
            width=32,
            pady=8
        )
        btn.pack(pady=7)
        return btn

    def clear_placeholder(self, event):
        if self.entry_name.get() == "Nhập tên để đăng ký":
            self.entry_name.delete(0, tk.END)
            self.entry_name.config(fg="#2c3e50")

    def restore_placeholder(self, event):
        if not self.entry_name.get():
            self.entry_name.insert(0, "Nhập tên để đăng ký")
            self.entry_name.config(fg="#7f8c8d")

    # ================== FACE ==================
    def encode_known_faces(self):
        self.known_face_paths = []
        self.known_face_names = []

        for filename in os.listdir(self.db_dir):
            if filename.endswith(".jpg"):
                self.known_face_paths.append(os.path.join(self.db_dir, filename))
                self.known_face_names.append(os.path.splitext(filename)[0])

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.most_recent_capture_arr = frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize((520, 360))
            imgtk = ImageTk.PhotoImage(img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        self.window.after(10, self.update_frame)

    def login(self):
        self.status.config(text="Đang nhận diện khuôn mặt...")
        rgb_frame = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            temp_path = tmp.name
            cv2.imwrite(temp_path, cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))

        for i, known_path in enumerate(self.known_face_paths):
            try:
                result = DeepFace.verify(temp_path, known_path, enforce_detection=False)
                if result["verified"]:
                    name = self.known_face_names[i]
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_to_excel(name, now)
                    util.msg_box("Thành công", f"Chào mừng {name}\nĐiểm danh lúc {now}")
                    os.remove(temp_path)
                    self.status.config(text="Nhận diện thành công")
                    return
            except:
                pass

        os.remove(temp_path)
        self.status.config(text="Không nhận diện được")
        util.msg_box("Thất bại", "Không nhận diện được khuôn mặt")

    def save_to_excel(self, name, timestamp):
        if not os.path.exists(self.excel_path):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Tên", "Thời gian"])
        else:
            wb = openpyxl.load_workbook(self.excel_path)
            ws = wb.active
        ws.append([name, timestamp])
        wb.save(self.excel_path)

    def open_excel(self):
        if os.path.exists(self.excel_path):
            os.startfile(self.excel_path)
        else:
            util.msg_box("Thông báo", "Chưa có dữ liệu")

    def accept_register_new_user(self):
        name = self.entry_name.get().strip()
        if not name or name == "Nhập tên để đăng ký":
            util.msg_box("Lỗi", "Vui lòng nhập tên hợp lệ")
            return

        path = os.path.join(self.db_dir, f"{name}.jpg")
        cv2.imwrite(path, self.most_recent_capture_arr)
        util.msg_box("Thành công", f"Đã đăng ký khuôn mặt cho {name}")
        self.encode_known_faces()

    def on_closing(self):
        self.cap.release()
        self.window.destroy()

# ================== RUN ==================
if __name__ == "__main__":
    FaceRecognitionApp()
