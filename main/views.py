from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from openpyxl import load_workbook
from django.contrib import messages
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .forms import SupportExcelUploadForm, EmailAuthForm
from .models import Support
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation


def login_view(request):
    if request.user.is_authenticated:
        return redirect("main:supports_upload")
    
    if request.method == "POST":
        form = EmailAuthForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("main:supports_upload")
    else:
        form = EmailAuthForm()
        
    return render(request, "main/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("main:login")


@login_required
def supports_upload_view(request):
    if request.method == "GET":
        form = SupportExcelUploadForm()
        return render(request, "main/supports_upload.html", {"form": form})
    
    # AJAX загрузка файла
    elif request.method == "POST":
        try:
            form = SupportExcelUploadForm(request.POST, request.FILES)
            if not form.is_valid():
                return JsonResponse({
                    'success': False, 
                    'error': 'Форма содержит ошибки',
                    'form_errors': form.errors
                })

            file = request.FILES["file"]
            
            # Проверка размера файла
            if file.size > 50 * 1024 * 1024:  # 50MB
                return JsonResponse({
                    'success': False,
                    'error': 'Файл слишком большой. Максимальный размер: 50MB'
                })

            # Обработка файла
            result = process_excel_file(file)
            
            if result['success']:
                messages.success(
                    request, 
                    f"Импорт завершён. Создано: {result['created']}, обновлено: {result['updated']}."
                )
                
                return JsonResponse({
                    'success': True,
                    'created': result['created'],
                    'updated': result['updated'],
                    'total': result['created'] + result['updated'],
                    'message': f"Импорт завершён. Создано: {result['created']}, обновлено: {result['updated']}."
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result['error']
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Произошла ошибка при обработке файла: {str(e)}'
            })

def process_excel_file(file):
    """
    Обрабатывает Excel файл и возвращает результат
    """
    try:
        wb = load_workbook(file, data_only=True)
        ws = wb.active

        headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

        # карта заголовков → поля модели
        header_map = {
            "Населенный пункт": "settlement",
            "Филиал": "branch", 
            "Номер опоры": "support_number",
            "Название": "name",
            "Уточнение расположения(ГИД)": "address",
            "Долгота": "longitude",
            "Широта": "latitude",
            "Дата ввода в экспуатацию": "commissioning_date",
            "Владеющая организация": "owner",
            "Материал несущей конструкции": "material",
        }

        # Проверяем наличие необходимых заголовков
        missing_headers = []
        for header in header_map.keys():
            if header not in headers:
                missing_headers.append(header)
        
        if missing_headers:
            return {
                'success': False,
                'error': f'В файле отсутствуют обязательные колонки: {", ".join(missing_headers)}'
            }

        # индексы колонок
        idx = {}
        for i, h in enumerate(headers):
            if h in header_map:
                idx[header_map[h]] = i

        created = 0
        updated = 0
        errors = []

        # Получаем общее количество строк для прогресса
        total_rows = ws.max_row - 1  # исключаем заголовок
        processed_rows = 0

        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):
                processed_rows += 1
                continue

            try:
                data = {}
                for field, i in idx.items():
                    val = row[i] if i < len(row) else None
                    
                    if field in ("longitude", "latitude"):
                        try:
                            data[field] = Decimal(str(val).replace(",", ".")) if val else None
                        except (InvalidOperation, AttributeError):
                            data[field] = None
                    elif field == "commissioning_date":
                        if isinstance(val, datetime):
                            data[field] = val
                        elif isinstance(val, str) and val.strip():
                            try:
                                data[field] = datetime.strptime(val.strip(), "%d.%m.%Y %H:%M:%S")
                            except Exception:
                                try:
                                    data[field] = datetime.strptime(val.strip(), "%d.%m.%Y")
                                except Exception:
                                    data[field] = None
                        else:
                            data[field] = None
                    else:
                        data[field] = str(val).strip() if val else ""

                # Проверяем обязательные поля
                required_fields = ['settlement', 'branch', 'support_number']
                missing_required = [field for field in required_fields if not data.get(field)]
                
                if missing_required:
                    errors.append(f"Строка {row_num}: отсутствуют обязательные поля: {', '.join(missing_required)}")
                    processed_rows += 1
                    continue

                # обновляем или создаём
                obj, is_created = Support.objects.update_or_create(
                    settlement=data.get("settlement"),
                    branch=data.get("branch"),
                    support_number=data.get("support_number"),
                    defaults=data,
                )
                
                if is_created:
                    created += 1
                else:
                    updated += 1

            except Exception as e:
                errors.append(f"Строка {row_num}: ошибка обработки - {str(e)}")
            
            processed_rows += 1
        
        return {
            'success': True,
            'created': created,
            'updated': updated,
            'errors': errors[:10] if errors else [],  # Возвращаем только первые 10 ошибок
            'total_rows': total_rows,
            'processed_rows': processed_rows
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Ошибка чтения файла: {str(e)}. Убедитесь, что файл не поврежден и имеет правильный формат.'
        }


# Дополнительный view для получения прогресса (опционально)
@login_required
def upload_progress(request):
    """
    Возвращает прогресс загрузки (можно использовать с Celery для асинхронной обработки)
    """
    if request.method == "GET":
        # Здесь можно получить прогресс из кэша/сессии/базы данных
        # Для простоты возвращаем фиктивные данные
        progress = request.session.get('upload_progress', 0)
        return JsonResponse({
            'progress': progress,
            'status': 'processing' if progress < 100 else 'completed'
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)