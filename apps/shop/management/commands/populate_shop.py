from django.core.management.base import BaseCommand
from apps.shop.models import Category, Product, ProductVariation


class Command(BaseCommand):
    help = 'Populate the shop with sample Premier League products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample shop products...'))

        # Create categories
        categories_data = [
            {'name': 'Jerseys', 'description': 'Official team jerseys and kits'},
            {'name': 'Accessories', 'description': 'Scarves, hats, and accessories'},
            {'name': 'Training Gear', 'description': 'Training clothes and equipment'},
            {'name': 'Memorabilia', 'description': 'Collectibles and memorabilia'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            {
                'name': 'Malmö FF Home Jersey',
                'description': 'Official Malmö FF home jersey for the current season. Made with premium materials for comfort and style.',
                'category': 'Jerseys',
                'product_type': 'variable',
                'price': 899,
                'sku': 'MFF-HOME-2024',
                'featured_image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=400&fit=crop&q=80',
                'variations': [
                    {'size': 'S', 'color': 'Blue', 'quality': 'Home', 'price': 899, 'stock_quantity': 10},
                    {'size': 'M', 'color': 'Blue', 'quality': 'Home', 'price': 899, 'stock_quantity': 15},
                    {'size': 'L', 'color': 'Blue', 'quality': 'Home', 'price': 899, 'stock_quantity': 12},
                    {'size': 'XL', 'color': 'Blue', 'quality': 'Home', 'price': 899, 'stock_quantity': 8},
                ]
            },
            {
                'name': 'Hammarby FF Home Jersey',
                'description': 'Official Hammarby FF home jersey. Show your support for the green and white!',
                'category': 'Jerseys',
                'product_type': 'variable',
                'price': 849,
                'sku': 'HFF-HOME-2024',
                'featured_image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=400&fit=crop&q=80',
                'variations': [
                    {'size': 'S', 'color': 'Green', 'quality': 'Home', 'price': 849, 'stock_quantity': 12},
                    {'size': 'M', 'color': 'Green', 'quality': 'Home', 'price': 849, 'stock_quantity': 18},
                    {'size': 'L', 'color': 'Green', 'quality': 'Home', 'price': 849, 'stock_quantity': 14},
                    {'size': 'XL', 'color': 'Green', 'quality': 'Home', 'price': 849, 'stock_quantity': 9},
                ]
            },
            {
                'name': 'AIK Stockholm Scarf',
                'description': 'Classic AIK Stockholm supporters scarf. Perfect for cold match days.',
                'category': 'Accessories',
                'product_type': 'single',
                'price': 299,
                'sku': 'AIK-SCARF-2024',
                'featured_image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop&q=80',
                'stock_quantity': 50,
            },
            {
                'name': 'Djurgården Training Jacket',
                'description': 'Official Djurgården training jacket. Comfortable and stylish for everyday wear.',
                'category': 'Training Gear',
                'product_type': 'variable',
                'price': 649,
                'sku': 'DIF-TRAIN-2024',
                'featured_image': 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop&q=80',
                'variations': [
                    {'size': 'S', 'color': 'Blue', 'quality': 'Training', 'price': 649, 'stock_quantity': 8},
                    {'size': 'M', 'color': 'Blue', 'quality': 'Training', 'price': 649, 'stock_quantity': 12},
                    {'size': 'L', 'color': 'Blue', 'quality': 'Training', 'price': 649, 'stock_quantity': 10},
                    {'size': 'XL', 'color': 'Blue', 'quality': 'Training', 'price': 649, 'stock_quantity': 6},
                ]
            },
            {
                'name': 'IFK Göteborg Cap',
                'description': 'Official IFK Göteborg cap with embroidered logo.',
                'category': 'Accessories',
                'product_type': 'single',
                'price': 249,
                'sku': 'IFK-CAP-2024',
                'featured_image': 'https://images.unsplash.com/photo-1575428652377-a9d5d22a76a7?w=400&h=400&fit=crop&q=80',
                'stock_quantity': 25,
            },
            {
                'name': 'Allsvenskan Football',
                'description': 'Official Allsvenskan match ball. Perfect for training or collecting.',
                'category': 'Memorabilia',
                'product_type': 'single',
                'price': 399,
                'sku': 'ALLSV-BALL-2024',
                'featured_image': 'https://images.unsplash.com/photo-1511363838471-44c45c2e1fb9?w=400&h=400&fit=crop&q=80',
                'stock_quantity': 30,
            },
        ]

        for product_data in products_data:
            variations_data = product_data.pop('variations', [])
            category = categories[product_data.pop('category')]

            product, created = Product.objects.get_or_create(
                sku=product_data['sku'],
                defaults={
                    **product_data,
                    'category': category,
                }
            )

            if created:
                self.stdout.write(f'Created product: {product.name}')

                # Create variations if any
                for var_data in variations_data:
                    variation = ProductVariation.objects.create(
                        product=product,
                        **var_data
                    )
                    self.stdout.write(f'  - Created variation: {variation}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated shop with {Product.objects.count()} products '
                f'and {ProductVariation.objects.count()} variations'
            )
        )