import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from main.models import Product

def create_sample_products():
    products_data = [
        {
            'name': 'Букет "Лунная ночь"',
            'price': 2500,
            'category': 'bouquet',
            'occasion': 'love',
            'color': 'Фиолетовый',
            'description': 'Изысканный букет в фиолетовых тонах с орхидеями и эвкалиптом.',
            'image': 'products/luna.jpg',
            'in_stock': True
        },
        {
            'name': 'Композиция "Мечта"',
            'price': 1800,
            'category': 'bouquet',
            'occasion': 'universal',
            'color': 'Розовый',
            'description': 'Нежная композиция из розовых роз и пионов.',
            'image': 'products/dream.jpg',
            'in_stock': True
        },
        # Добавьте остальные товары из вашего списка...
    ]
    
    for product_data in products_data:
        Product.objects.create(**product_data)
    
    print("Sample products created!")

if __name__ == '__main__':
    create_sample_products()