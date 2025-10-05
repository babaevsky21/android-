from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Создает простую иконку для приложения"""
    # Размеры для Android иконки
    size = 512
    
    # Создаем изображение
    img = Image.new('RGBA', (size, size), (70, 130, 180, 255))  # Steel blue background
    draw = ImageDraw.Draw(img)
    
    # Рисуем круглую форму
    margin = size // 10
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(100, 149, 237, 255))  # Cornflower blue
    
    # Добавляем текст
    try:
        # Пытаемся использовать системный шрифт
        font_size = size // 8
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        # Используем стандартный шрифт если системный недоступен
        font = ImageFont.load_default()
    
    # Текст "SC" (SpellChecker)
    text = "SC"
    
    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Центрируем текст
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - size // 20
    
    # Рисуем белый текст
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Добавляем маленький значок проверки
    check_size = size // 10
    check_x = size - check_size - margin
    check_y = size - check_size - margin
    
    # Зеленая галочка
    draw.ellipse([check_x, check_y, check_x + check_size, check_y + check_size],
                fill=(34, 139, 34, 255))  # Forest green
    
    # Сохраняем иконку
    icon_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(icon_dir, 'icon.png')
    img.save(icon_path, 'PNG')
    
    print(f"✅ Иконка создана: {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_app_icon()
