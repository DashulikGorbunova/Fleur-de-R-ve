from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Product, Cart, Order, User

def home(request):
    """Главная страница"""
    featured_products = [
        {
            'id': 1,
            'name': 'Букет "Лунная ночь"',
            'price': 2500,
            'description': 'Изысканный букет в фиолетовых тонах',
            'img': 'https://i.pinimg.com/736x/5e/06/18/5e0618bf35f76b984d8ce6b0690062e7.jpg',
            'category': 'Готовые букеты'
        },
        {
            'id': 2,
            'name': 'Композиция "Мечта"', 
            'price': 1800,
            'description': 'Нежная композиция из розовых роз',
            'img': 'https://i.pinimg.com/1200x/34/c5/3a/34c53a5330f2bde8054f97167c0b2025.jpg',
            'category': 'Готовые букеты'
        },
        {
            'id': 5,
            'name': 'Розы в шляпной коробке',
            'price': 3200,
            'description': 'Элегантные белые розы в стильной коробке',
            'img': 'https://i.pinimg.com/1200x/c3/93/3d/c3933db27fd14c7634af0f69adb5689b.jpg',
            'category': 'Цветы в коробке'
        },
        {
            'id': 8,
            'name': 'Букет "Сюрприз" со скидкой',
            'price': 1900,
            'original_price': 2400,
            'description': 'Сезонный букет со скидкой 20%',
            'img': 'https://i.pinimg.com/736x/5e/06/18/5e0618bf35f76b984d8ce6b0690062e7.jpg',
            'category': 'Акции'
        }
    ]
    
    context = {
        'featured_products': featured_products
    }
    return render(request, 'main/home.html', context)

def about(request):
    """Страница о магазине"""
    return render(request, 'main/about.html')

def popular(request):
    """Популярные товары"""
    popular_products = [
        {
            'id': 1,
            'name': 'Букет "Лунная ночь"',
            'price': 2500,
            'category': 'Готовые букеты',
            'occasion': 'Романтика',
            'color': 'Фиолетовый',
            'description': 'Изысканный букет в фиолетовых тонах с орхидеями и эвкалиптом.',
            'img': 'https://i.pinimg.com/736x/5e/06/18/5e0618bf35f76b984d8ce6b0690062e7.jpg',
            'in_stock': True
        },
        {
            'id': 2, 
            'name': 'Композиция "Мечта"',
            'price': 1800,
            'category': 'Готовые букеты',
            'occasion': 'Универсальный',
            'color': 'Розовый',
            'description': 'Нежная композиция из розовых роз и пионов.',
            'img': 'https://i.pinimg.com/1200x/34/c5/3a/34c53a5330f2bde8054f97167c0b2025.jpg',
            'in_stock': True
        },
        {
            'id': 8,
            'name': 'Букет "Сюрприз" со скидкой',
            'price': 1900,
            'original_price': 2400,  # Добавлено поле для акции
            'category': 'Акции',
            'occasion': 'Сюрприз',
            'color': 'Разноцветный',
            'description': 'Сезонный букет со скидкой 20%.',
            'img': 'https://i.pinimg.com/736x/3e/87/56/3e87563699a8742c5ea9646756a3eaf8.jpg',
            'in_stock': True
        },
        # Добавим еще популярных товаров для полноты
        {
            'id': 5,
            'name': 'Розы в шляпной коробке',
            'price': 3200,
            'category': 'Цветы в коробке',
            'occasion': 'Роскошь',
            'color': 'Белый',
            'description': 'Элегантные белые розы в стильной шляпной коробке. Премиальный подарок.',
            'img': 'https://i.pinimg.com/1200x/7d/16/fd/7d16fdd26367be26bd0f6e06dceb6f2f.jpg',
            'in_stock': True
        },
        {
            'id': 3,
            'name': 'Розы красные (12 шт)',
            'price': 1500,
            'category': 'Цветы поштучно',
            'occasion': 'Любовь',
            'color': 'Красный',
            'description': 'Классические красные розы премиум-качества. Символ страсти и любви.',
            'img': 'https://i.pinimg.com/1200x/56/d1/f5/56d1f534c2968e2d86e8ae8a902c6743.jpg',
            'in_stock': True
        },
        {
            'id': 9,
            'name': 'Пионы розовые (7 шт)',
            'price': 1700,
            'category': 'Цветы поштучно',
            'occasion': 'Свадьба',
            'color': 'Розовый',
            'description': 'Пышные розовые пионы. Идеальны для свадебных букетов и декоров.',
            'img': 'https://i.pinimg.com/736x/2c/c4/d9/2cc4d9c0df6c2ff67e785864f52e2eb1.jpg',
            'in_stock': True
        }
    ]
    
    context = {
        'popular_products': popular_products
    }
    return render(request, 'main/popular.html', context)


def reviews(request):
    """Страница отзывов"""
    from .models import Review
    from django.db.models import Avg, Count
    
    # Обработка отправки отзыва
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        text = request.POST.get('text', '').strip()
        rating = request.POST.get('rating', 5)
        
        if name and text:
            try:
                Review.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=name,
                    text=text,
                    rating=int(rating),
                    is_approved=False  # Отзыв требует модерации
                )
                messages.success(request, 'Спасибо за ваш отзыв! Он появится на сайте после модерации.')
            except Exception as e:
                messages.error(request, 'Произошла ошибка при отправке отзыва.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
        
        return redirect('reviews')
    
    # Получаем одобренные отзывы
    reviews_list = Review.objects.filter(is_approved=True)
    
    # Статистика
    stats = reviews_list.aggregate(
        avg_rating=Avg('rating'),
        total_count=Count('id')
    )
    
    avg_rating = round(stats['avg_rating'], 1) if stats['avg_rating'] else 5.0
    total_reviews = stats['total_count'] or 0
    
    # Процент рекомендаций (4-5 звёзд)
    positive_reviews = reviews_list.filter(rating__gte=4).count()
    recommend_percent = round((positive_reviews / total_reviews * 100)) if total_reviews > 0 else 100
    
    context = {
        'reviews': reviews_list,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'recommend_percent': recommend_percent,
    }
    return render(request, 'main/reviews.html', context)

def custom(request):
    """Авторский букет"""
    return render(request, 'main/custom.html')

# Замените функцию custom_bouquet
def custom_bouquet(request):
    """Страница авторского букета"""
    if request.method == 'POST':
        # Сохраняем заявку в базу данных
        from .models import CustomBouquetRequest
        
        try:
            CustomBouquetRequest.objects.create(
                occasion=request.POST.get('occasion'),
                preferred_flowers=request.POST.get('preferred_flowers'),
                color_scheme=request.POST.get('color_scheme'),
                budget=request.POST.get('budget'),
                wishes=request.POST.get('wishes'),
                name=request.POST.get('name', ''),
                phone=request.POST.get('phone'),
                email=request.POST.get('email', ''),
                status='новая'
            )
            messages.success(request, 'Ваша заявка успешно отправлена! Наш флорист свяжется с вами в ближайшее время.')
        except Exception as e:
            messages.error(request, f'Произошла ошибка при отправке заявки: {str(e)}')
        
        # После POST запроса делаем редирект, чтобы избежать повторной отправки
        return redirect('custom_bouquet')
    
    return render(request, 'main/custom_bouquet.html')

def catalog(request):
    """Каталог товаров с умной фильтрацией"""
    # Расширенные данные товаров
    products = [
        # ГОТОВЫЕ БУКЕТЫ
        {
            'id': 1,
            'name': 'Букет "Лунная ночь"',
            'price': 2500,
            'category': 'Готовые букеты',
            'occasion': 'Романтика',
            'color': 'Фиолетовый',
            'description': 'Изысканный букет в фиолетовых тонах с орхидеями и эвкалиптом. Идеален для романтических моментов.',
            'img': 'https://i.pinimg.com/736x/5e/06/18/5e0618bf35f76b984d8ce6b0690062e7.jpg',
            'in_stock': True
        },
        {
            'id': 2, 
            'name': 'Композиция "Мечта"',
            'price': 1800,
            'category': 'Готовые букеты',
            'occasion': 'Универсальный',
            'color': 'Розовый',
            'description': 'Нежная композиция из розовых роз и пионов. Подходит для любого повода.',
            'img': 'https://i.pinimg.com/1200x/34/c5/3a/34c53a5330f2bde8054f97167c0b2025.jpg',
            'in_stock': True
        },
        {
            'id': 11,
            'name': 'Букет "Нежность"',
            'price': 2200,
            'category': 'Готовые букеты',
            'occasion': 'Свидание',
            'color': 'Белый',
            'description': 'Белые розы и лилии в обрамлении зелени. Символ чистоты и невинности.',
            'img': 'https://i.pinimg.com/1200x/ce/30/e5/ce30e5112b209a6fc789917e88d09edd.jpg',
            'in_stock': True
        },
        {
            'id': 12,
            'name': 'Букет "Страсть"',
            'price': 2900,
            'category': 'Готовые букеты',
            'occasion': 'Любовь',
            'color': 'Красный',
            'description': 'Пылающие красные розы в сочетании с алыми гвоздиками. Выразите свои чувства!',
            'img': 'https://i.pinimg.com/1200x/9c/23/d1/9c23d1e5bb415d671f9084cfd670ded5.jpg',
            'in_stock': True
        },
        {
            'id': 13,
            'name': 'Букет "Весеннее утро"',
            'price': 1700,
            'category': 'Готовые букеты',
            'occasion': '8 марта',
            'color': 'Жёлтый',
            'description': 'Солнечные тюльпаны и нарциссы. Подарите кусочек весны!',
            'img': 'https://i.pinimg.com/1200x/31/c5/2a/31c52ab5c4227421dd48c53f4950b6c7.jpg',
            'in_stock': True
        },

        # ЦВЕТЫ ПОШТУЧНО
        {
            'id': 3,
            'name': 'Розы красные (12 шт)',
            'price': 1500,
            'category': 'Цветы поштучно',
            'occasion': 'Любовь',
            'color': 'Красный',
            'description': 'Классические красные розы премиум-качества. Символ страсти и любви.',
            'img': 'https://i.pinimg.com/1200x/56/d1/f5/56d1f534c2968e2d86e8ae8a902c6743.jpg',
            'in_stock': True
        },
        {
            'id': 4,
            'name': 'Тюльпаны микс (10 шт)',
            'price': 800,
            'category': 'Цветы поштучно', 
            'occasion': 'Весна',
            'color': 'Разноцветный',
            'description': 'Яркие тюльпаны разных цветов. Принесут весеннее настроение в любой дом.',
            'img': 'https://i.pinimg.com/736x/d1/1e/ba/d11eba27ab677a8a922627296ed6cf33.jpg',
            'in_stock': True
        },
        {
            'id': 9,
            'name': 'Пионы розовые (7 шт)',
            'price': 1700,
            'category': 'Цветы поштучно',
            'occasion': 'Свадьба',
            'color': 'Розовый',
            'description': 'Пышные розовые пионы. Идеальны для свадебных букетов и декоров.',
            'img': 'https://i.pinimg.com/736x/2c/c4/d9/2cc4d9c0df6c2ff67e785864f52e2eb1.jpg',
            'in_stock': True
        },
        {
            'id': 14,
            'name': 'Орхидеи фаленопсис (3 шт)',
            'price': 2100,
            'category': 'Цветы поштучно',
            'occasion': 'Роскошь',
            'color': 'Белый',
            'description': 'Элегантные белые орхидеи. Цветут несколько месяцев.',
            'img': 'https://i.pinimg.com/1200x/5a/b7/fe/5ab7fe0380bd126421c687c478b38ce2.jpg',
            'in_stock': True
        },
        {
            'id': 15,
            'name': 'Герберы разноцветные (15 шт)',
            'price': 1200,
            'category': 'Цветы поштучно',
            'occasion': 'День рождения',
            'color': 'Разноцветный',
            'description': 'Яркие и жизнерадостные герберы. Поднимут настроение!',
            'img': 'https://i.pinimg.com/736x/fa/82/de/fa82de937fbdf6e5d9f040f9b23ffaf8.jpg',
            'in_stock': True
        },

        # ЦВЕТЫ В КОРОБКЕ
        {
            'id': 5,
            'name': 'Розы в шляпной коробке',
            'price': 3200,
            'category': 'Цветы в коробке',
            'occasion': 'Роскошь',
            'color': 'Белый',
            'description': 'Элегантные белые розы в стильной шляпной коробке. Премиальный подарок.',
            'img': 'https://i.pinimg.com/1200x/7d/16/fd/7d16fdd26367be26bd0f6e06dceb6f2f.jpg',
            'in_stock': True
        },
        {
            'id': 16,
            'name': 'Пионы в круглой коробке',
            'price': 2800,
            'category': 'Цветы в коробке',
            'occasion': 'Свидание',
            'color': 'Розовый',
            'description': 'Нежные пионы в элегантной круглой коробке. Идеально для романтического вечера.',
            'img': 'https://i.pinimg.com/1200x/2e/cc/d1/2eccd14c4b52feb99539b07a21247218.jpg',
            'in_stock': True
        },
        {
            'id': 17,
            'name': 'Сухоцветы в стеклянной колбе',
            'price': 1900,
            'category': 'Цветы в коробке',
            'occasion': 'Дом',
            'color': 'Бежевый',
            'description': 'Композиция из сухоцветов в стильной стеклянной колбе. Сохраняется годами.',
            'img': 'https://i.pinimg.com/736x/b8/4e/5c/b84e5cac0db0b780bcb2a31ca2e1d4c6.jpg',
            'in_stock': True
        },

        # КОМНАТНЫЕ РАСТЕНИЯ
        {
            'id': 6,
            'name': 'Орхидея фаленопсис',
            'price': 1200,
            'category': 'Комнатные растения',
            'occasion': 'Дом',
            'color': 'Белый',
            'description': 'Изящная орхидея в горшке. Цветет несколько месяцев при правильном уходе.',
            'img': 'https://i.pinimg.com/736x/87/89/d2/8789d214146197f49fda65c209c79d2e.jpg',
            'in_stock': True
        },
        {
            'id': 10,
            'name': 'Мини-сад суккулентов',
            'price': 1400,
            'category': 'Комнатные растения',
            'occasion': 'Офис',
            'color': 'Зелёный',
            'description': 'Композиция из нескольких видов суккулентов в керамическом кашпо.',
            'img': 'https://i.pinimg.com/736x/8c/fa/11/8cfa11bb9e1697600fb3e60a28787ebb.jpg',
            'in_stock': True
        },
        {
            'id': 18,
            'name': 'Фикус Бенджамина',
            'price': 1800,
            'category': 'Комнатные растения',
            'occasion': 'Новоселье',
            'color': 'Зелёный',
            'description': 'Пушистое деревце для вашего дома. Очищает воздух и создает уют.',
            'img': 'https://i.pinimg.com/736x/af/eb/fa/afebfa01147d1ddd250756e4c201c182.jpg',
            'in_stock': True
        },
        {
            'id': 19,
            'name': 'Монстера деликатесная',
            'price': 2200,
            'category': 'Комнатные растения',
            'occasion': 'Офис',
            'color': 'Тёмно-зелёный',
            'description': 'Модное растение с резными листьями. Прекрасно вписывается в любой интерьер.',
            'img': 'https://i.pinimg.com/736x/f1/97/dd/f197ddc1ac11ea6116762d3de76a412f.jpg',
            'in_stock': True
        },

        # ПОДАРКИ И АКСЕССУАРЫ
        {
            'id': 7,
            'name': 'Подарочный набор "Для него"',
            'price': 2800,
            'category': 'Подарки',
            'occasion': 'Мужчине',
            'color': 'Зелёный',
            'description': 'Стильный набор: суккулент + ароматическая свеча + открытка.',
            'img': 'https://i.pinimg.com/1200x/01/94/c7/0194c7258a7709b4ca1d6e134a945f31.jpg',
            'in_stock': True
        },
        {
            'id': 20,
            'name': 'Набор "Ароматерапия"',
            'price': 1600,
            'category': 'Подарки',
            'occasion': 'Релакс',
            'color': 'Фиолетовый',
            'description': 'Эфирные масла, свечи и сухоцветы для создания уютной атмосферы.',
            'img': 'https://i.pinimg.com/736x/45/3f/69/453f692da16f5c51b501a474e74c2ab6.jpg',
            'in_stock': True
        },

        # АКЦИИ И РАСПРОДАЖИ
        {
            'id': 8,
            'name': 'Букет "Сюрприз" со скидкой',
            'price': 1900,
            'original_price': 2400,
            'category': 'Акции',
            'occasion': 'Сюрприз',
            'color': 'Разноцветный',
            'description': 'Сезонный букет со скидкой 20%. Флорист сам подберет лучшие цветы дня.',
            'img': 'https://i.pinimg.com/736x/3e/87/56/3e87563699a8742c5ea9646756a3eaf8.jpg',
            'in_stock': True
        },
        {
            'id': 21,
            'name': 'Распродажа: Осенняя коллекция',
            'price': 1500,
            'original_price': 2000,
            'category': 'Акции',
            'occasion': 'Осень',
            'color': 'Оранжевый',
            'description': 'Теплые осенние оттенки: хризантемы, герберы, декоративная зелень.',
            'img': 'https://i.pinimg.com/736x/e2/b9/8c/e2b98c24f2e26ddd68d69308a79cd321.jpg',
            'in_stock': True
        },
        {
            'id': 22,
            'name': 'Свадебный букет "Невеста"',
            'price': 3500,
            'original_price': 4200,
            'category': 'Акции',
            'occasion': 'Свадьба',
            'color': 'Белый',
            'description': 'Роскошный свадебный букет из белых роз и орхидей. Скидка 15%!',
            'img': 'https://i.pinimg.com/736x/4b/84/07/4b840785e7fcdebccaca160853483019.jpg',
            'in_stock': True
        },

        # СЕЗОННЫЕ ПРЕДЛОЖЕНИЯ
        {
            'id': 23,
            'name': 'Новогодняя композиция',
            'price': 3200,
            'category': 'Сезонные',
            'occasion': 'Новый год',
            'color': 'Красный',
            'description': 'Праздничная композиция с хвойными ветками, шишками и красными розами.',
            'img': 'https://i.pinimg.com/736x/36/eb/5b/36eb5b492403f856911672185b791bc9.jpg',
            'in_stock': True
        },
        {
            'id': 24,
            'name': 'Весенний микс',
            'price': 1800,
            'category': 'Сезонные',
            'occasion': '8 марта',
            'color': 'Разноцветный',
            'description': 'Свежие весенние цветы: тюльпаны, нарциссы, гиацинты и мускари.',
            'img': 'https://i.pinimg.com/1200x/88/d1/47/88d14743ac0f1a507a390c14fbfd5096.jpg',
            'in_stock': True
        }
    ]
    
    # Фильтрация (остается без изменений)
    category = request.GET.get('category', '')
    occasion = request.GET.get('occasion', '')
    color = request.GET.get('color', '')
    search = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    filtered_products = products
    
    # Фильтр по категории
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    # Фильтр по поводу
    if occasion:
        filtered_products = [p for p in filtered_products if p['occasion'] == occasion]
    
    # Фильтр по цвету
    if color:
        filtered_products = [p for p in filtered_products if color.lower() in p['color'].lower()]
    
    # Фильтр по цене
    if min_price:
        filtered_products = [p for p in filtered_products if p['price'] >= int(min_price)]
    if max_price:
        filtered_products = [p for p in filtered_products if p['price'] <= int(max_price)]
    
    # Поиск по названию
    if search:
        filtered_products = [p for p in filtered_products if search.lower() in p['name'].lower()]
    
    # Уникальные значения для фильтров
    categories = list(set(p['category'] for p in products))
    occasions = list(set(p['occasion'] for p in products))
    colors = list(set(p['color'] for p in products))
    
    context = {
        'products': filtered_products,
        'categories': categories,
        'occasions': occasions,
        'colors': colors,
        'selected_category': category,
        'selected_occasion': occasion,
        'selected_color': color,
        'search_query': search,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'main/catalog.html', context)

def flower_info(request, flower_name):
    """Информация о конкретном цветке"""
    flowers = {
        'Роза': {
            'desc': 'Классический символ любви и страсти. Идеально для романтических моментов.', 
            'img': 'https://i.pinimg.com/1200x/b9/f6/a8/b9f6a826c92f693291921119e185c066.jpg',
            'price': 150,
            'sticker': '🌹'
        },
        'Тюльпан': {
            'desc': 'Весенний цветок радости и нежности. Прекрасен в букетах и композициях.', 
            'img': 'https://i.pinimg.com/1200x/60/83/08/608308bfdfebbb4f8d4d8d9cf687a34d.jpg',
            'price': 100,
            'sticker': '🌷'
        },
        'Орхидея': {
            'desc': 'Экзотическая красота и изысканность. Символ роскоши и утонченности.', 
            'img': 'https://i.pinimg.com/736x/06/48/7f/06487f4d0ff574707d4d521f964837b7.jpg',
            'price': 300,
            'sticker': '🌺'
        }
    }
    
    flower_data = flowers.get(flower_name, {
        'desc': 'Такого цветка нет в каталоге.',
        'img': 'https://i.pinimg.com/736x/f4/86/1d/f4861d3d3066469b38db724d92ed0225.jpg',
        'price': 0,
        'sticker': '❓'
    })
    
    context = {
        'flower_name': flower_name,
        'flower_data': flower_data
    }
    return render(request, 'main/flower_info.html', context)

@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество {product.name} увеличено')
    else:
        messages.success(request, f'{product.name} добавлен в корзину')
    return redirect('cart')

@login_required
def cart(request):
    """Страница корзины"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'main/cart.html', context)

@login_required
def remove_from_cart(request, cart_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} удален из корзины')
    return redirect('cart')

@login_required
def update_cart(request, cart_id):
    """Обновление количества товара в корзине"""
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'Количество {cart_item.product.name} обновлено')
        else:
            cart_item.delete()
            messages.success(request, f'{cart_item.product.name} удален из корзины')
    return redirect('cart')

@login_required
def checkout(request):
    """Оформление заказа"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    if not cart_items:
        messages.warning(request, 'Корзина пуста')
        return redirect('cart')
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        # Создание заказа
        order = Order.objects.create(
            user=request.user,
            customer_name=request.POST.get('customer_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            delivery_date=request.POST.get('delivery_date'),
            delivery_time=request.POST.get('delivery_time'),
            payment_method=request.POST.get('payment_method'),
            wishes=request.POST.get('wishes', ''),
            total_price=total
        )
        
        # Очистка корзины
        cart_items.delete()
        
        messages.success(request, 'Заказ успешно оформлен!')
        return redirect('order_success', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'main/checkout.html', context)

@login_required
def order_success(request, order_id):
    """Страница успешного заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Получаем данные из заказа
    # Предполагаем, что у вас есть поле для цветов в заказе
    # Если нет, нужно изменить модель Order
    
    # Для примера: берем первый товар из заказа
    # Вам нужно адаптировать этот код под вашу модель Order
    flower_name = "Роза"  # Замените на реальное имя цветка из заказа
    count = 3  # Замените на реальное количество из заказа
    price = 150  # Замените на реальную цену
    total = order.total_price  # Итоговая сумма из заказа
    
    stickers = {
        'Роза': '🌹', 'Тюльпан': '🌷', 'Орхидея': '🌺'
    }
    sticker = stickers.get(flower_name, '')
    
    context = {
        'sticker': sticker,
        'flower_name': flower_name,
        'count': count,
        'price': price,
        'total': total,
        'order': order  # Сохраняем объект order для будущего использования
    }
    return render(request, 'main/order_success.html', context)
@login_required
def order_history(request):
    """История заказов"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/order_history.html', {'orders': orders})

@login_required
def profile(request):
    """Личный кабинет пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'main/profile.html', {'orders': orders})

def delivery_info(request):
    """Информация о доставке"""
    return render(request, 'main/delivery_info.html')

def care_guide(request):
    """Информация об уходе за цветами"""
    return render(request, 'main/care_guide.html')

# Аутентификация
def login_view(request):
    """Вход в систему"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'main/login.html')

def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')

def register_view(request):
    """Регистрация"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'main/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'main/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'main/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно! Добро пожаловать в Fleur de Rêve!')
        return redirect('home')
    
    return render(request, 'main/register.html')

# Дополнительные страницы
def delivery(request):
    return render(request, 'main/delivery.html')

def care(request):
    return render(request, 'main/care.html')

def contacts(request):
    return render(request, 'main/contacts.html')

# Обработчики ошибок
def page_not_found(request, exception):
    return render(request, 'main/404.html', status=404)

def server_error(request):
    return render(request, 'main/500.html', status=500)

def bad_request(request, exception):
    return render(request, 'main/400.html', status=400)

def permission_denied(request, exception):
    return render(request, 'main/403.html', status=403)