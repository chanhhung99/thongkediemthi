import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, Button, Label, Listbox, messagebox, Frame, MULTIPLE, StringVar
from tkinter import ttk, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Đọc file
data_files = {
    "2022": r"D:\Python\chanhhung\diem_thi_thpt_2022.csv",
    "2023": r"D:\Python\chanhhung\diem_thi_thpt_2023.csv",
    "2024": r"D:\Python\chanhhung\diem_thi_thpt_2024.csv",
}
data_sample = pd.read_csv(data_files["2024"])
subjects = list(data_sample.columns[1:-1])

# Ánh xạ môn thi sang Tiếng Việt có dấu
subject_mapping = {
    "toan": "Toán",
    "ngu_van": "Ngữ Văn",
    "ngoai_ngu": "Tiếng Anh",
    "vat_li": "Vật Lý",
    "hoa_hoc": "Hoá học",
    "sinh_hoc": "Sinh học",
    "lich_su": "Lịch sử",
    "dia_li": "Địa lí",
    "gdcd": "Giáo dục công dân",
}

# Ánh xạ mã tỉnh sang tên tỉnh
province_mapping = {
    "01": "Thành phố Hà Nội",
    "02": "Thành phố Hồ Chí Minh",
    "03": "Thành phố Hải Phòng",
    "04": "Thành phố Đà Nẵng",
    "05": "Tỉnh Hà Giang",
    "06": "Tỉnh Cao Bằng",
    "07": "Tỉnh Lai Châu",
    "08": "Tỉnh Lào Cai",
    "09": "Tỉnh Tuyên Quang",
    "10": "Tỉnh Lạng Sơn",
    "11": "Tỉnh Bắc Kạn",
    "12": "Tỉnh Thái Nguyên",
    "13": "Tỉnh Yên Bái",
    "14": "Tỉnh Sơn La",
    "15": "Tỉnh Phú Thọ",
    "16": "Tỉnh Vĩnh Phúc",
    "17": "Tỉnh Quảng Ninh",
    "18": "Tỉnh Bắc Giang",
    "19": "Tỉnh Bắc Ninh",
    "21": "Tỉnh Hải Dương",
    "22": "Tỉnh Hưng Yên",
    "23": "Tỉnh Hòa Bình",
    "24": "Tỉnh Hà Nam",
    "25": "Tỉnh Nam Định",
    "26": "Tỉnh Thái Bình",
    "27": "Tỉnh Ninh Bình",
    "28": "Tỉnh Thanh Hóa",
    "29": "Tỉnh Nghệ An",
    "30": "Tỉnh Hà Tĩnh",
    "31": "Tỉnh Quảng Bình",
    "32": "Tỉnh Quảng Trị",
    "33": "Tỉnh Thừa Thiên - Huế",
    "34": "Tỉnh Quảng Nam",
    "35": "Tỉnh Quảng Ngãi",
    "36": "Tỉnh Kon Tum",
    "37": "Tỉnh Bình Định",
    "38": "Tỉnh Gia Lai",
    "39": "Tỉnh Phú Yên",
    "40": "Tỉnh Đắk Lắk",
    "41": "Tỉnh Khánh Hòa",
    "42": "Tỉnh Lâm Đồng",
    "43": "Tỉnh Bình Phước",
    "44": "Tỉnh Bình Dương",
    "45": "Tỉnh Ninh Thuận",
    "46": "Tỉnh Tây Ninh",
    "47": "Tỉnh Bình Thuận",
    "48": "Tỉnh Đồng Nai",
    "49": "Tỉnh Long An",
    "50": "Tỉnh Đồng Tháp",
    "51": "Tỉnh An Giang",
    "52": "Tỉnh Bà Rịa Vũng Tàu",
    "53": "Tỉnh Tiền Giang",
    "54": "Tỉnh Kiên Giang",
    "55": "Thành phố Cần Thơ",
    "56": "Tỉnh Bến Tre",
    "57": "Tỉnh Vĩnh Long",
    "58": "Tỉnh Trà Vinh",
    "59": "Tỉnh Sóc Trăng",
    "60": "Tỉnh Bạc Liêu",
    "61": "Tỉnh Cà Mau",
    "62": "Tỉnh Điện Biên",
    "63": "Tỉnh Đắk Nông",
    "64": "Tỉnh Hậu Giang",
}

# Tạo cửa sổ giao diện chính
root = Tk()
root.title("Chương trình thống kê điểm thi đại học (Version 1.0.1)")
root.state("zoomed")

# Hiển thị màn hình chính
def show_main_screen():
    global province_listbox, subject_listbox, year_listbox

    # Xóa các widget cũ
    for widget in root.pack_slaves():
        widget.destroy()
    
    # Tiêu đề Trang chủ
    title_font = font.Font(family="Arial", size=18, weight="bold")
    title_label = Label(root, text="Chương trình thống kê điểm thi đại học (version 1.0.1)", font=title_font)
    title_label.pack(pady=5)

    label = Label(root, text="Made by Chanh Hung \n Tính năng sắp update: Phát hiện gian lận, biểu đồ thay đổi thứ hạng,...", font=("Arial", 12))
    label.pack(pady=5)

    # Hướng dẫn
    label = Label(root, text="Chọn năm học, môn thi và tỉnh thành bạn muốn hiển thị phổ điểm", font=("Arial", 14))
    label.pack(pady=10)

    # Danh sách năm học
    year_label = Label(root, text="Chọn năm học:", font=("Arial", 12))
    year_label.pack(pady=5)

    year_listbox = Listbox(root, selectmode="browse", font=("Arial", 12), height=5, exportselection=False)
    for year in data_files.keys():
        year_listbox.insert("end", year)
    year_listbox.pack(pady=5)

    # Danh sách tỉnh thành
    province_label = Label(root, text="Chọn tỉnh:", font=("Arial", 12))
    province_label.pack(pady=5)

    province_listbox = Listbox(root, selectmode="browse", font=("Arial", 12), height=10, exportselection=False)
    province_listbox.insert("end", "Toàn quốc")
    for province in province_mapping.values():
        province_listbox.insert("end", province)
    province_listbox.pack(pady=5)

    # Danh sách môn thi
    subject_label = Label(root, text="Chọn môn thi:", font=("Arial", 12))
    subject_label.pack(pady=5)

    subject_listbox = Listbox(root, selectmode="browse", font=("Arial", 12), height=10, exportselection=False)
    for subject in subjects:
        subject_listbox.insert("end", subject_mapping.get(subject, subject))
    subject_listbox.pack(pady=5)
    
    # Nút hiển thị phổ điểm
    show_button = Button(root, text="Hiển thị phổ điểm", font=("Arial", 12), command=show_province_distribution)
    show_button.pack(pady=10)

    # Nút bảng xếp hạng
    rank_button = Button(root, text="Xem bảng xếp hạng", font=("Arial", 12), command=show_ranking_screen)
    rank_button.pack(pady=10)

# Giao diện bảng xếp hạng
def show_ranking_screen():
    global year_listbox, subject_listbox

    # Xoá các widget cũ
    for widget in root.pack_slaves():
        widget.destroy()

    # Tiêu đề bảng xếp hạng
    title_font = font.Font(family="Arial", size=18, weight="bold")
    title_label = Label(root, text=f"Bảng xếp hạng điểm trung bình", font=title_font)
    title_label.pack(pady=5)
    
    # Chọn năm
    year_label = Label(root, text="Chọn năm:", font=("Arial", 12))
    year_label.pack(pady=5)

    year_listbox = Listbox(root, selectmode="browse", font=("Arial", 12), height=5, exportselection=False)
    for year in data_files.keys():
        year_listbox.insert("end", year)
    year_listbox.pack(pady=5)

    # Chọn môn học
    subject_label = Label(root, text="Chọn môn học:", font=("Arial", 12))
    subject_label.pack(pady=5)

    subject_listbox = Listbox(root, selectmode="browse", font=("Arial", 12), height=10, exportselection=False)
    subject_listbox.insert("end", "Tất cả các môn")
    for subject in subjects:
        subject_listbox.insert("end", subject_mapping.get(subject, subject))
    subject_listbox.pack(pady=5)

    # Nút xem bảng xếp hạng
    show_rank_button = Button(root, text="Xem bảng xếp hạng", font=("Arial", 12), command=show_ranking)
    show_rank_button.pack(pady=10)

    # Nút quay lại
    back_button = Button(root, text="Quay lại", font=("Arial", 12), command=show_main_screen)
    back_button.pack(pady=10)

# Tính điểm trung bình và xếp hạng
def show_ranking():
    try:
        selected_year_index = year_listbox.curselection()
        selected_subject_index = subject_listbox.curselection()

        if not selected_subject_index or not selected_year_index:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đầy đủ năm học và môn học!")

        selected_year = year_listbox.get(selected_year_index[0])
        selected_subject = subject_listbox.get(selected_subject_index[0])

        # Đọc file csv theo năm
        data_file = data_files[selected_year]
        data = pd.read_csv(data_file)
        data["sbd"] = data["sbd"].astype(str).str.zfill(8)

        # Xác định cột điểm số và chuyển tất cả các cột điểm thành dạng số
        score_columns = data.columns[1:-1]
        score_columns = [col for col in score_columns if col not in ["ma_ngoai_ngu"]]
        for col in score_columns[1:-1]:
            data[col] = pd.to_numeric(data[col], errors="coerce")

        # Tính điểm trung bình theo tỉnh
        data["Province"] = data["sbd"].str[:2]
        if selected_subject == "Tất cả các môn":
            data["Average"] = data[score_columns].mean(axis=1, skipna=True)
        else:
            # Ánh xạ ngược tên môn học hiển thị sang tên cột csv
            inverse_subject_mapping = {v: k for k, v in subject_mapping.items()}
            if selected_subject not in inverse_subject_mapping:
                raise ValueError(f"Môn học '{selected_subject}' không tồn tại trong dữ liệu")
            subject_key = inverse_subject_mapping[selected_subject]
            
            if subject_key not in data.columns:
                raise ValueError(f"Cột {subject_key} không tồn tại trong dữ liệu")

            if data[subject_key].isna().all():
                raise ValueError(f"Dữ liệu môn {selected_subject} (cột {subject_key}) không hợp lệ hoặc rỗng")
            
            data["Average"] = data[subject_key]
        
        # Tính điểm trung bình theo tỉnh
        ranking = data.groupby("Province")["Average"].mean().reset_index()
        ranking["Province"] = ranking["Province"].map(province_mapping)
        ranking = ranking.sort_values(by="Average", ascending=False).reset_index(drop=True)
    
        # Xoá các widget cũ
        for widget in root.pack_slaves():
            widget.destroy()

        # Tiêu đề bảng xếp hạng
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title_label = Label(root, text=f"Bảng xếp hạng điểm Trung bình môn {selected_subject} năm {selected_year}",
                            font=title_font)
        title_label.pack(pady=5)

        # Định dạng cỡ chữ lớn cho BXH
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10))

        # Hiển thị bảng xếp hạng
        root.resizable(True, True)
        root.state("zoomed")
        tree = ttk.Treeview(root, columns=("Rank", "Province", "Average"), show="headings", height=43)
        tree.heading("Rank", text="Thứ hạng")
        tree.heading("Province", text="Tên tỉnh")
        tree.heading("Average", text="Điểm trung bình")

        tree.column("Rank", anchor="center", width=100)
        tree.column("Province", anchor="center", width=150)
        tree.column("Average", anchor="center", width=120)

        # Thêm dữ liệu vào Treeview
        for idx, row in ranking.iterrows():
            tree.insert("", "end", values=(idx + 1, row["Province"], f"{row["Average"]:.3f}"))
        
        tree.pack(pady=5)

        # Nút quay lại
        back_button = Button(root, text="Quay lại", font=("Arial", 12), command=show_ranking_screen)
        back_button.pack(pady=10)


    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

# Vẽ biểu đồ phổ điểm
def plot_distribution(subject, province, year, figure, filtered_data):

    # Tạo khoảng điểm (Toán/Tiếng Anh khoảng cách 0.2)
    if subject == "toan" or subject == "ngoai_ngu":
        bins = np.arange(0, 10.2, 0.2)
        labels = [round(x, 1) for x in bins]
        filtered_data["Rounded"] = filtered_data[subject].round(1)
    # Các môn còn lại khoảng cách 0.25
    else:
        bins = np.arange(0, 10.25, 0.25)
        labels = [round(x, 2) for x in bins]
        filtered_data["Rounded"] = filtered_data[subject].round(2)

    # Đếm tổng số học sinh đạt mỗi mức điểm
    score_counts = filtered_data["Rounded"].value_counts().reindex(labels, fill_value=0)

    # Vẽ biểu đồ cột
    figure.clear() # Xoá biểu đồ cũ
    ax = figure.add_subplot(111)
    ax.clear()

    # Vẽ cột biểu đồ
    ax.bar(score_counts.index, score_counts.values, width=0.15, color="skyblue", edgecolor="black")

    # Chú thích số lượng ở đầu mỗi cột
    for x, y in zip(score_counts.index, score_counts.values):
        ax.text(x, y+0.5, str(int(y)), ha="center", va="bottom", fontsize=8, rotation=60)
    
    # Hiển thị tiêu đề và chú thích trục x, y
    ax.set_title("")  # Xóa tiêu đề cũ
    ax.set_xlabel("")  # Xóa nhãn trục x cũ
    ax.set_ylabel("")  # Xóa nhãn trục y cũ

    ax.set_title(f"Phổ điểm môn {subject_mapping.get(subject, subject)} của {province} ({year})", fontsize=16)
    ax.set_xlabel("Điểm số", fontsize=14)
    ax.set_ylabel("Số lượng thí sinh", fontsize=14)

    ax.set_xticks(labels)
    ax.set_xticklabels(labels, rotation=60)
    
    ax.grid(axis="y", linestyle="--", alpha=0.7)

# Lọc dữ liệu theo tỉnh
def filter_data_by_province(data, province_code):

    # 2 chữ số đầu tiên của sbd là mã tỉnh
    filtered_data = data[data["sbd"].str[:2] == province_code].copy()
    return filtered_data

# Hiển thị biểu đồ
def show_canvas(figure):
    # Xoá widget cũ
    for widget in root.pack_slaves():
        widget.destroy()
    
    # Thêm biểu đồ vào giao diện
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()

    # Nút quay lại
    back_button = Button(root, text="Quay lại màn hình chính", font=("Arial", 12), command=show_main_screen)
    back_button.pack(pady=10)

# Hiển thị biểu đồ phổ điểm theo tỉnh
def show_province_distribution():
    global year_listbox, province_listbox, subject_listbox

    try:
        # Lấy giá trị đã chọn từ listbox
        selected_year_index = year_listbox.curselection()
        selected_province_index = province_listbox.curselection()
        selected_subject_index = subject_listbox.curselection()
        
        if not selected_year_index or not selected_province_index or not selected_subject_index:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đầy đủ năm học, tỉnh thành và môn học")
            return
        
        selected_year = year_listbox.get(selected_year_index[0])
        selected_province = province_listbox.get(selected_province_index[0])
        selected_subject = subjects[selected_subject_index[0]]

        # Đọc file csv theo năm
        data_file = data_files[selected_year]
        data = pd.read_csv(data_file)
        data["sbd"] = data["sbd"].astype(str).str.zfill(8)

        # Khi in dữ liệu toàn quốc
        if selected_province == "Toàn quốc":
            filtered_data = data.copy()
        
        # Khi lọc dữ liệu theo tỉnh
        else:
            province_code = [code for code, name in province_mapping.items() if name == selected_province][0]
            filtered_data = data[data["sbd"].str[:2] == province_code].copy()

        if filtered_data.empty:
            messagebox.showinfo("Thông báo", f"Không có giữ liệu cho {province_mapping.get(province_code)}")
            return
        
        # Hiển thị biểu đồ
        figure = plt.Figure(figsize=(10,6))
        plot_distribution(selected_subject, selected_province, selected_year, figure, filtered_data)
        show_canvas(figure)

    except IndexError:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn đầy đủ thông tin!")

# Chạy chương trình
show_main_screen()
root.mainloop()