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

### Phase 5.5: Dashboard Layout with Sidebar Navigation

**Mục tiêu:** Tạo layout tổng thể với sidebar navigation để dễ mở rộng tính năng

**Layout Structure:**
```
┌─────────────────────────────────────────┐
│  [Logo] Expense Tracker                 │
├──────────┬──────────────────────────────┤
│          │                              │
│ Sidebar  │      Main Content            │
│          │                              │
│ • Home   │  Welcome to Expense Tracker  │
│ • Monthly│                              │
│   Budget │  [Dashboard content here]    │
│ • Catego │                              │
│   ries   │                              │
│ • Statis │                              │
│   tics   │                              │
│ • Settin │                              │
│   gs     │                              │
│          │                              │
└──────────┴──────────────────────────────┘
```

**Sidebar Menu Items:**
- [ ] **Home / Dashboard** - Welcome page (trang trống với lời chào)
- [ ] **Monthly Budget** - Quản lý ngân sách theo tháng
- [ ] **Categories** - Quản lý danh mục thu/chi
- [ ] **Statistics** (Future) - Biểu đồ thống kê
- [ ] **Settings** (Future) - Cài đặt, user profile

**Templates:**
- [ ] `base.html` - Cập nhật layout với sidebar
  - Header với logo/title
  - Sidebar navigation (fixed, responsive)
  - Main content area
- [ ] `dashboard/home.html` - Trang chủ welcome
  - "Welcome to Expense Tracker"
  - Quick stats overview (optional)
  - Recent activities (optional)

**Static Files:**
- [ ] `css/sidebar.css` - Style cho sidebar
  - Fixed sidebar on desktop
  - Collapsible on mobile
  - Active menu highlighting
  - Hover effects

**URLs Structure:**
- [ ] `/` → Dashboard home (welcome page)
- [ ] `/monthly/` → Monthly budget list
- [ ] `/categories/` → Category management
- [ ] `/statistics/` → Statistics (future)
- [ ] `/settings/` → Settings (future)

**Implementation Steps:**
1. [ ] Tạo `dashboard` app mới (hoặc dùng expenses app)
2. [ ] Cập nhật `base.html` với sidebar layout
3. [ ] Tạo `dashboard/home.html` - Welcome page
4. [ ] Tạo `sidebar.css` với responsive design
5. [ ] Update URLs - `/` → dashboard home
6. [ ] Thêm active state cho menu items
7. [ ] Test responsive behavior (mobile/tablet/desktop)

---

### Phase 6: Monthly Budget System

**Flow tổng quan:**
```
1. Homepage (Monthly List) → Click [+ Tạo tháng mới]
2. Modal: Chọn tháng/năm → Tạo MonthlyBudget
3. Redirect → Month Detail (2 tabs):
   ├─ Tab 1: "Tóm tắt" - Budget Planning
   │   ├─ Chi phí: Dự kiến | Thực tế | Chênh lệch (theo category)
   │   └─ Thu nhập: Dự kiến | Thực tế | Chênh lệch (theo category)
   └─ Tab 2: "Giao dịch" - Transactions List
       └─ Danh sách transactions trong tháng (như hiện tại)
```

**Models:**
- [ ] Tạo model `MonthlyBudget`
  ```python
  year = IntegerField()
  month = IntegerField()
  created_at = DateTimeField(auto_now_add=True)
  unique_together = ('year', 'month')
  ```
- [ ] Tạo model `CategoryBudget`
  ```python
  monthly_budget = ForeignKey(MonthlyBudget)
  category = ForeignKey(Category)
  budgeted_amount = DecimalField(default=0)  # Dự kiến
  unique_together = ('monthly_budget', 'category')
  ```
  - **Lưu ý**: Thực tế sẽ tính từ Transaction, không lưu vào DB
- [ ] Tạo model `GlobalBalance` (initial_balance, current_balance)
- [ ] Chạy migrations

**Views:**
- [ ] `monthly_list` - Homepage (Trang chủ)
  - Hiển thị list các MonthlyBudget đã tạo
  - Mỗi row: Tháng/Năm | Income | Expense | Balance
  - Button [+ Tạo tháng mới]
  - Hiển thị Global Balance ở header
- [ ] `month_create` - Tạo tháng mới
  - Form chọn year/month (hoặc tự động = tháng hiện tại)
  - Tạo MonthlyBudget
  - Redirect về `month_detail`
- [ ] `month_detail` - Chi tiết tháng (2 tabs)
  - **Tab 1: "Tóm tắt"** (Budget Planning)
    - Bảng Chi phí: Category | Dự kiến | Thực tế | Chênh lệch
    - Bảng Thu nhập: Category | Dự kiến | Thực tế | Chênh lệch
    - Click vào "Dự kiến" → Edit inline hoặc modal
  - **Tab 2: "Giao dịch"** (Transactions)
    - Tái sử dụng transaction_list layout
    - Filter transactions theo tháng hiện tại
    - Button thêm transaction (modal)
- [ ] `category_budget_update` - Update dự kiến cho category
  - AJAX endpoint để update CategoryBudget.budgeted_amount
  - Hoặc form đơn giản nếu không dùng AJAX
- [ ] Logic tính toán:
  - **Thực tế**: `SUM(Transaction.amount)` WHERE `date` in month, GROUP BY `category`
  - **Chênh lệch**: `Dự kiến - Thực tế`
  - **Global Balance**: `initial_balance + SUM(income) - SUM(expense)`

**Templates:**
- [ ] `monthly_list.html` - Homepage
  - Bảng list MonthlyBudget
  - Button [+ Tạo tháng mới] → Modal hoặc redirect
  - Header hiển thị Global Balance
- [ ] `month_create_form.html` - Form tạo tháng (modal hoặc page)
  - Input: Year (dropdown hoặc number)
  - Input: Month (dropdown 1-12)
  - Submit → Tạo MonthlyBudget
- [ ] `month_detail.html` - Chi tiết tháng
  - Bootstrap Tabs: "Tóm tắt" | "Giao dịch"
  - Tab 1: 2 bảng (Chi phí + Thu nhập) với Dự kiến/Thực tế/Chênh lệch
  - Tab 2: Tái sử dụng transaction_list layout
- [ ] `category_budget_form.html` - Form edit dự kiến (nếu dùng modal)

**Forms:**
- [ ] `MonthlyBudgetForm` - Form tạo tháng mới (chọn year/month)
- [ ] `CategoryBudgetForm` - Form nhập/sửa dự kiến cho category
- [ ] `GlobalBalanceForm` - Form nhập vốn ban đầu (tùy chọn)

**URLs:**
- [ ] `/` → `monthly_list` (Homepage mới)
- [ ] `/month/create/` → `month_create`
- [ ] `/month/<year>/<month>/` → `month_detail` (default tab: Tóm tắt)
- [ ] `/month/<year>/<month>/transactions/` → `month_detail` (tab: Giao dịch)
- [ ] `/month/<year>/<month>/budget/update/` → `category_budget_update`
- [ ] `/transactions/` → Giữ lại transaction_list cũ (hoặc xóa nếu không dùng)

**Implementation Steps:**
1. [ ] Tạo models `MonthlyBudget` + `CategoryBudget` + migrations
2. [ ] Tạo view `month_create` + form tạo tháng mới
3. [ ] Tạo view `monthly_list` - Homepage list các tháng
4. [ ] Tạo view `month_detail` - Tab "Tóm tắt" (hiển thị bảng Dự kiến/Thực tế)
5. [ ] Implement logic tính "Thực tế" từ transactions
6. [ ] Tạo view `category_budget_update` - Edit dự kiến (inline hoặc modal)
7. [ ] Tạo Tab "Giao dịch" - Tái sử dụng transaction_list
8. [ ] Update URLs - Đổi homepage từ `/` → `monthly_list`
9. [ ] Tạo model `GlobalBalance` + logic tính tổng balance

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
