# Hướng dẫn Deploy lên Railway

## Bước 1: Chuẩn bị Git Repository

```bash
# Khởi tạo git (nếu chưa có)
git init

# Thêm tất cả files
git add .

# Commit
git commit -m "Initial commit for deployment"

# Tạo repo trên GitHub và push
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Bước 2: Deploy lên Railway

1. **Đăng ký Railway:**
   - Truy cập: https://railway.app
   - Đăng nhập bằng GitHub

2. **Tạo Project mới:**
   - Click **"New Project"**
   - Chọn **"Deploy from GitHub repo"**
   - Chọn repository của bạn

3. **Thêm PostgreSQL Database:**
   - Trong project, click **"+ New"**
   - Chọn **"Database"** → **"Add PostgreSQL"**
   - Railway tự động tạo và set biến môi trường `DATABASE_URL`

4. **Cấu hình Environment Variables (tùy chọn):**
   - Vào **Settings** → **Variables**
   - Thêm nếu cần:
     - `SECRET_KEY`: Django secret key (tạo mới cho production)
     - `DEBUG`: `False` (cho production)

5. **Chạy Migrations:**
   - Vào tab **"Deployments"**
   - Click vào deployment mới nhất
   - Mở **"View Logs"**
   - Trong tab **"Deploy Logs"**, tìm nơi có thể chạy command
   - Hoặc dùng Railway CLI:
     ```bash
     railway run python manage.py migrate
     railway run python manage.py createsuperuser
     ```

6. **Collect Static Files:**
   - Railway tự động chạy `collectstatic` khi deploy
   - Nếu không, chạy: `railway run python manage.py collectstatic --noinput`

## Bước 3: Truy cập ứng dụng

- Railway tự động tạo domain: `your-app-name.railway.app`
- Vào **Settings** → **Domains** để xem URL
- Hoặc thêm custom domain nếu muốn

## Lưu ý:

- **SECRET_KEY**: Nên tạo mới cho production (dùng `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- **DEBUG**: Nên set `False` trong production
- **ALLOWED_HOSTS**: Đã set `['*']` để Railway tự động handle
- Database migrations sẽ tự động chạy khi deploy

## Troubleshooting:

- Nếu lỗi static files: Kiểm tra `STATIC_ROOT` và `whitenoise` đã được cài
- Nếu lỗi database: Kiểm tra `DATABASE_URL` đã được set trong Railway
- Xem logs: Railway Dashboard → Deployments → View Logs
