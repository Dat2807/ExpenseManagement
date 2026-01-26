# Plan: Web Quản lý Chi tiêu với Django

## Tổng quan

Xây dựng web quản lý chi tiêu với Django + PostgreSQL, bắt đầu từ CRUD cơ bản với phân loại danh mục, sử dụng Django Template cho frontend.

---

## Kiến trúc tổng quan

```
[Browser] → [Django Templates + Static Files]
                    ↓
            [Views (Logic)]
                    ↓
            [Models (Data)]
                    ↓
            [PostgreSQL Database]
```

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
| TransactionListView | `/` | Danh sách giao dịch |
| TransactionCreateView | `/add/` | Thêm giao dịch (chọn loại → filter danh mục) |
| TransactionUpdateView | `/edit/<id>/` | Sửa giao dịch |
| TransactionDeleteView | `/delete/<id>/` | Xóa giao dịch |

**Category Views:**
| View | URL | Chức năng |
|------|-----|-----------|
| CategoryListView | `/categories/` | Quản lý danh mục (tách 2 tab: Thu/Chi) |
| CategoryCreateView | `/categories/add/` | Thêm danh mục (chọn loại) |

---

### Phase 5: Templates

- [ ] Base template với Bootstrap 5 CDN
- [ ] Transaction list (trang chủ)
- [ ] Transaction form (thêm/sửa)
- [ ] Category list
- [ ] Delete confirmation

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

1. **Phase hiện tại**: CRUD + Categories ✅
2. **Phase 5**: Thống kê theo tuần/tháng/năm
3. **Phase 6**: Biểu đồ với Chart.js
4. **Phase 7**: User Authentication (đăng ký/đăng nhập)

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
