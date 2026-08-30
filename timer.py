import sys
import os
import ctypes
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                               QPushButton, QHBoxLayout, QVBoxLayout, 
                               QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QIntValidator, QFont

# --- 處理 PyInstaller 暫存路徑的函式 ---
def resource_path(relative_path):
    """取得資源的絕對路徑，支援 PyInstaller 的單一執行檔模式"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CountdownTimer(QWidget):
    def __init__(self):
        super().__init__()
        
        # --- 設定視窗基本屬性 ---
        self.setWindowTitle("倒數計時器")
        self.setFixedSize(320, 220)
        
        # --- 設定視窗與工作列圖示 ---
        try:
            myappid = 'my_custom_timer.version1' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            icon_path = resource_path('icon.ico')
            self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass

        self.total_seconds = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer) 

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- 1. 輸入區域 (時、分、秒) ---
        input_layout = QHBoxLayout()
        
        # 🔥 新增：設定元件之間的間距，數字越小越緊緊靠在一起
        input_layout.setSpacing(8) 
        
        # 🔥 新增：在最左側加入一個「彈性空間」，把後面的元件往右推
        input_layout.addStretch()
        input_layout.addSpacing(10)  # 👈 新增這行！括號內的數字越大，就會越往右推（例如 10~25）

        validator = QIntValidator(0, 99, self)

        # 小時
        self.hour_input = self.create_time_input(validator)
        input_layout.addWidget(self.hour_input)
        input_layout.addWidget(QLabel("時", font=QFont("微軟正黑體", 12)))

        # 分鐘
        self.min_input = self.create_time_input(validator)
        input_layout.addWidget(self.min_input)
        input_layout.addWidget(QLabel("分", font=QFont("微軟正黑體", 12)))

        # 秒數
        self.sec_input = self.create_time_input(validator)
        input_layout.addWidget(self.sec_input)
        input_layout.addWidget(QLabel("秒", font=QFont("微軟正黑體", 12)))

        # 🔥 新增：在最右側加入一個「彈性空間」，把前面的元件往左推 (達成完美置中)
        input_layout.addStretch()

        main_layout.addLayout(input_layout)

        # --- 2. 顯示倒數時間的大標籤 ---
        self.time_label = QLabel("00:00:00")
        self.time_label.setFont(QFont("Helvetica", 40, QFont.Bold))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("color: #333333;")
        main_layout.addWidget(self.time_label)

        # --- 3. 按鈕區域 ---
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(15)

        self.start_btn = QPushButton("開始倒數")
        self.start_btn.setFixedSize(100, 35)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white; 
                font-family: '微軟正黑體'; font-size: 14px; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:disabled { background-color: #cccccc; color: #777777; }
        """)
        self.start_btn.clicked.connect(self.start_timer)
        btn_layout.addWidget(self.start_btn)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setFixedSize(100, 35)
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336; color: white; 
                font-family: '微軟正黑體'; font-size: 14px; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        self.cancel_btn.clicked.connect(self.cancel_timer)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def create_time_input(self, validator):
        line_edit = QLineEdit("00")
        line_edit.setFixedSize(40, 35)
        line_edit.setMaxLength(2)
        line_edit.setValidator(validator)
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setFont(QFont("Helvetica", 16))
        line_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 4px; background: white;")
        return line_edit

    def start_timer(self):
        h = int(self.hour_input.text() or 0)
        m = int(self.min_input.text() or 0)
        s = int(self.sec_input.text() or 0)
        
        self.total_seconds = h * 3600 + m * 60 + s

        if self.total_seconds <= 0:
            QMessageBox.warning(self, "警告", "請輸入大於 0 的時間！")
            return

        self.start_btn.setEnabled(False)
        self.update_display() 
        self.timer.start(1000)

    def update_timer(self):
        if self.total_seconds > 0:
            self.total_seconds -= 1
            self.update_display()
        
        if self.total_seconds <= 0:
            self.timer.stop()
            self.reset_ui()
            
            # 將視窗拉至最上層並取得焦點（不修改 WindowFlags，避免關閉按鈕失效）
            self.raise_()
            self.activateWindow()
            
            # 直接以 self 為父視窗彈出提示，此提示對話框本身就會在最上層
            QMessageBox.information(self, "提示", "時間到囉！你設定的倒數已經結束。")
            self.show()

    def update_display(self):
        mins, secs = divmod(self.total_seconds, 60)
        hours, mins = divmod(mins, 60)
        self.time_label.setText(f"{hours:02d}:{mins:02d}:{secs:02d}")

    def cancel_timer(self):
        self.timer.stop()
        self.reset_ui()

    def reset_ui(self):
        self.hour_input.setText("00")
        self.min_input.setText("00")
        self.sec_input.setText("00")
        self.time_label.setText("00:00:00")
        self.start_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 這裡已經把舊版警告的 DPI 設定刪除囉！
    
    window = CountdownTimer()
    window.show()
    sys.exit(app.exec())
