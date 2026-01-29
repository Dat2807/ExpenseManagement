# Plan: Web Quản lý Chi tiêu với Django

## Tổng quan

Xây dựng web quản lý chi tiêu với Django + PostgreSQL theo mô hình **Monthly Budget Tracker**:
- Trang chủ: List các tháng với tổng income/expense/balance
- Chi tiết tháng: Xem và quản lý transactions trong tháng đó
- Budget planning: Nhập dự kiến chi cho mỗi tháng
- Global balance: Số dư tổng tích lũy (có thể nhập vốn ban đầu)

---

## Kiến trúc tổng quan

```
[Homepage: Monthly List]
    ↓ (Click vào tháng)
[Month Detail: Transactions + Budget]
    ↓ (Add/Edit transactions)
[Transaction Form]
    ↓
[Update Global Balance]
```

**Flow:**
- User vào trang chủ → Thấy list các tháng với income/expense/balance
- Click vào tháng → Xem chi tiết transactions + budget của tháng đó
- Thêm transaction → Tự động cập nhật balance tháng và global balance

---

## Cấu trúc thư mục dự án

```
expense_tracker/
├── manage.py
├── requirements.txt
├── expense_tracker/          # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── expenses/                 # Main app
│   ├── models.py            # Category, Transaction
│   ├── views.py             # CRUD views
│   ├── urls.py
│   ├── forms.py             # Django Forms
│   └── templates/
│       └── expenses/
│           ├── base.html
│           ├── transaction_list.html
│           ├── transaction_form.html
│           └── category_list.html
└── static/
    └── css/
        └── style.css
```

---

## Database Models

### Category (Danh mục)
| Field | Type | Mô tả |
|-------|------|-------|
| id | AutoField | Primary key |
| name | CharField | Tên danh mục |
| type | CharField | income / expense |
| created_at | DateTimeField | Ngày tạo |

### Transaction (Giao dịch)
| Field | Type | Mô tả |
|-------|------|-------|
| id | AutoField | Primary key |
| description | CharField | Mô tả giao dịch |
| amount | DecimalField | Số tiền |
| date | DateField | Ngày giao dịch |
| category | ForeignKey | Liên kết Category (type lấy từ Category) |
| created_at | DateTimeField | Ngày tạo |

### MonthlyBudget (Ngân sách tháng)
| Field | Type | Mô tả |
|-------|------|-------|
| id | AutoField | Primary key |
| year | IntegerField | Năm (2024, 2025, ...) |
| month | IntegerField | Tháng (1-12) |
| budgeted_expense | DecimalField | Số tiền dự kiến chi trong tháng |
| created_at | DateTimeField | Ngày tạo |
| updated_at | DateTimeField | Ngày cập nhật |

**Unique constraint:** `(year, month)` - Mỗi tháng chỉ có 1 budget

### GlobalBalance (Số dư tổng)
| Field | Type | Mô tả |
|-------|------|-------|
| id | AutoField | Primary key |
| initial_balance | DecimalField | Vốn ban đầu (nhập 1 lần) |
| current_balance | DecimalField | Số dư hiện tại (tự động tính) |
| updated_at | DateTimeField | Ngày cập nhật |

**Logic:** `current_balance = initial_balance + (tổng income - tổng expense)`

---

## Các Phase thực hiện

### Phase 1: Setup môi trường

- [ ] Tạo Python Virtual Environment
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- [ ] Cài đặt dependencies
  ```bash
  pip install django psycopg2-binary
  pip freeze > requirements.txt
  ```

- [ ] Tạo database trong pgAdmin
  - Mở pgAdmin → Click phải vào Databases → Create → Database
  - Tên: `expense_db`

---

### Phase 2: Tạo Django Project

- [ ] Tạo project
  ```bash
  django-admin startproject expense_tracker .
  ```

- [ ] Tạo app expenses
  ```bash
  python manage.py startapp expenses
  ```

- [ ] Cấu hình PostgreSQL trong `settings.py`
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'expense_db',
          'USER': 'postgres',
          'PASSWORD': 'your_password',
          'HOST': 'localhost',
          'PORT': '5432',
      }
  }
  ```

- [ ] Thêm app vào `INSTALLED_APPS`
  ```python
  INSTALLED_APPS = [
      ...
      'expenses',
  ]
  ```

---

### Phase 3: Tạo Models

- [ ] Tạo models trong `expenses/models.py`

- [ ] Chạy migrations
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- [ ] Tạo superuser để dùng Admin
  ```bash
  python manage.py createsuperuser
  ```

- [ ] Đăng ký models trong `expenses/admin.py`

---

### Phase 4: CRUD Views

**Transaction Views:**
| View | URL | Chức năng |
|------|-----|-----------|
| TransactionListView | `/` | Danh sách giao dịch + tổng thu/chi |
| TransactionCreateView | `/add/` | Thêm giao dịch (chọn loại → filter danh mục) |
| TransactionUpdateView | `/edit/<id>/` | Sửa giao dịch |
| TransactionDeleteView | `/delete/<id>/` | Xóa giao dịch |

**Category Views:**
| View | URL | Chức năng |
|------|-----|-----------|
| CategoryListView | `/categories/` | Quản lý danh mục (tách 2 tab: Thu/Chi) |
| CategoryCreateView | `/categories/add/` | Thêm danh mục (chọn loại) |

---

### Phase 5: Templates & UX (đã làm gần xong)

- [x] Base template với Bootstrap 5 CDN
- [x] Transaction list (trang chủ, income/expense 2 cột + modal)
- [x] Transaction form (thêm/sửa)
- [x] Category list (income/expense tách cột)
- [x] Delete confirmation
- [x] **Category CRUD với Modal (AJAX load)**
  - ✅ Chuyển Create/Edit/Delete sang Bootstrap Modal
  - ✅ Load nội dung từ template hiện có qua AJAX
  - ✅ Ngăn xóa Category đang được sử dụng (PROTECT)
  - ⚠️ **Limitation:** 
    - Form submit vẫn reload trang (chưa dùng AJAX submit)
    - Message vẫn xuất hiện trên page (chưa dùng AJAX) 

**Cải tiến tương lai (Optional):**
- [ ] AJAX form submission (không reload trang)
  - Sửa views trả về JSON response
  - JavaScript intercept form submit
  - Update DOM manually sau khi success
  - Hiển thị validation errors trong modal
  - Message đổi thành dạng Toast  

---

### Phase 6: Monthly Budget System

**Models:**
- [ ] Tạo model `MonthlyBudget` (year, month, budgeted_expense)
- [ ] Tạo model `GlobalBalance` (initial_balance, current_balance)
- [ ] Chạy migrations

**Views:**
- [ ] Tạo `monthly_list` view - Trang chủ hiển thị list các tháng
  - Group transactions theo năm/tháng
  - Tính income/expense/balance cho mỗi tháng
  - Hiển thị global balance
- [ ] Tạo `month_detail` view - Chi tiết tháng
  - Hiển thị transactions trong tháng (income/expense 2 cột)
  - Form nhập/sửa budget cho tháng
  - Form thêm transaction (modal như hiện tại)
- [ ] Logic tính toán global balance tự động

**Templates:**
- [ ] `monthly_list.html` - Bảng list các tháng
  - Columns: Tháng/Năm | Income | Expense | Budget | Balance | Actions
  - Click vào row → chuyển đến `month_detail`
  - Hiển thị Global Balance ở trên
- [ ] `month_detail.html` - Chi tiết tháng
  - Tái sử dụng layout từ `transaction_list.html`
  - Thêm phần Budget (dự kiến vs thực tế)
  - List transactions trong tháng

**Forms:**
- [ ] `MonthlyBudgetForm` - Form nhập/sửa budget
- [ ] `GlobalBalanceForm` - Form nhập vốn ban đầu (tùy chọn)

**URLs:**
- [ ] Đổi homepage từ `transaction_list` → `monthly_list`
- [ ] Thêm route `month/<year>/<month>/` cho `month_detail`

---

### Phase 7: Biểu đồ & Chart.js

- [ ] Kết nối dữ liệu thống kê với Chart.js
- [ ] Biểu đồ cột theo tháng (Income vs Expense)
- [ ] Biểu đồ đường xu hướng balance theo thời gian

### Phase 8: User Authentication

- [ ] Đăng ký / đăng nhập
- [ ] Mỗi user có dữ liệu chi tiêu riêng

---

## Danh mục mặc định

### Thu nhập (income)
| Tên |
|-----|
| Lương |
| Thưởng |
| Đầu tư |
| Khác |

### Chi tiêu (expense)
| Tên |
|-----|
| Ăn uống |
| Di chuyển |
| Giải trí |
| Mua sắm |
| Hóa đơn |
| Khác |

---

## Roadmap tương lai

1. **Hiện tại**: CRUD + Categories + Templates ✅
2. **Tiếp theo**: Phase 6 – Monthly Budget System (đang làm)
3. Phase 7 – Filter theo tháng/năm + Biểu đồ với Chart.js
4. Phase 8 – User Authentication (đăng ký/đăng nhập)

---

## Lệnh hay dùng

```bash
# Chạy server
python manage.py runserver

# Tạo migrations sau khi sửa models
python manage.py makemigrations
python manage.py migrate

# Mở Django shell
python manage.py shell

# Tạo superuser
python manage.py createsuperuser
```

---

## Tài liệu tham khảo

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Girls Tutorial (Tiếng Việt)](https://tutorial.djangogirls.org/vi/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
