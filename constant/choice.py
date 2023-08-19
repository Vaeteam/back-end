SEX = (
    ('male', "male"),
    ('female', "female"),
    ('any', "any"),
)

DAY_CHOICE = (
    ("Thứ Hai", "Thứ Hai"),  # thứ 2
    ("Thứ Ba", "Thứ Ba"),  # thứ 3
    ("Thứ Tư", "Thứ Tư"),  # thứ 4
    ("Thứ Năm", "Thứ Năm"),  # thứ 5
    ("Thứ Sáu", "Thứ Sáu"),  # thứ 6
    ("Thứ Bảy", "Thứ Bảy"),  # thứ 7
    ("Chủ Nhật", "Chủ Nhật")  # chủ nhật
)

DAY = [0, 1, 2, 3, 4, 5, 6]

STATE = (
    ("created", "Tạo bài thành công"),
    ("verified", "Bài đã được duyệt"),
    ("teacher_selected", "Đã chọn được giáo viên"),
    ("teacher_accepted", "Giáo viên đã đồng ý"),
    ("teacher_rejected ", "Giáo viên đã từ chối"),
    ("connected", "Đã kết nối giáo viên và học viên")
)

COMMON = ["Sáng thứ 2", "Sáng thứ 3", "Sáng thứ 4", "Sáng thứ 5", "Sáng thứ 6", "Sáng thứ 7", "Sáng chủ nhật", "Chiều thứ 2", "Chiều thứ 3", "Chiều thứ 4", "Chiều thứ 5", "Chiều thứ 6", "Chiều thứ 7", "Chiều chủ nhật"]

TIME = (
    ("Ca 1", "Ca 1"),
    ("Ca 2", "Ca 2"),
    ("Ca 3", "Ca 3"),
    ("Ca 4", "Ca 4"),
    ("Ca 5", "Ca 5"),
    ("Ca khác", "Ca khác")
)

TEACHING_LOCATION = (
    ("learner home", "Nhà người học"),
    ("teacher home", "Nhà giáo viên"),
    ("online", "Online"),
    ("leaner home hibrid", "Nhà người học và online"),
    ("teacher home hibrid", "Nhà giáo viên và online"),
)

TEACHING_TIME_UNIT = (
    ("Tháng", "Tháng"),
    ("Tuần", "Tuần"),
    ("Buổi", "Buổi"),
)

EDUCATION = (
    ('Tốt nghiệp lớp 12', 'Tốt nghiệp lớp 12'),
    ('Sinh Viên', 'Sinh Viên'),
    ('Cử Nhân/Kỹ Sư', 'Cử Nhân/Kỹ Sư'),
    ('Học Viên Cao Học', 'Học Viên Cao Học'),
    ('Thạc Sĩ', 'Thạc Sĩ'),
    ('Nghiên cứu sinh', 'Nghiên cứu sinh'),
    ('Tiến Sĩ', 'Tiến Sĩ'),
    ('Phó Giáo Sư', 'Phó Giáo Sư'),
    ('Giáo Sư', 'Giáo Sư')
)

YEAR_EXP = (
    ('1 năm', '1 năm'),
    ('2 năm', '2 năm'),
    ('3 năm', '3 năm'),
    ('4 năm', '4 năm'),
    ('5 năm', '5 năm'),
    ('Trên 5 năm', 'Trên 5 năm'),
)
