from django.core.management.base import BaseCommand
from news.models import Category, NewsArticle
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with mock news data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = ["সব", "মধ্যপ্রাচ্য", "ইউরোপ", "ভিসা ও ইমিগ্রেশন", "কর্মসংস্থান", "বাণিজ্য"]
        category_objects = {}
        for name in categories_data:
            cat, created = Category.objects.get_or_create(name=name, defaults={'slug': name.replace(" ", "-")})
            category_objects[name] = cat
        self.stdout.write(self.style.SUCCESS('Successfully created categories'))

        # Create admin user
        if not User.objects.filter(email='admin@probash.com').exists():
            User.objects.create_superuser('admin@probash.com', 'admin', 'adminpassword')
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))

        news_data = [
            {
                "title": "প্রবাসীদের জন্য নতুন ডিজিটাল ইকামা ঘোষণা করেছে সৌদি আরব",
                "description": "সৌদি আরবের পাসপোর্ট অধিদপ্তর একটি সম্পূর্ণ ডিজিটাল ইকামা চালু করেছে, যার মাধ্যমে প্রবাসীরা তাদের রেসিডেন্সি পারমিট স্মার্টফোনে বহন করতে পারবেন।",
                "category": "মধ্যপ্রাচ্য",
                "imageUrl": "/images/news1.jpg",
                "source": "সৌদি গেজেট",
                "is_featured": True
            },
            {
                "title": "নন-ইইউ নাগরিকদের জন্য ৪০,০০০ সিজনাল ওয়ার্ক ভিসা খুলল ইতালি",
                "description": "ইতালি সরকার অত্যন্ত প্রত্যাশিত 'ডিক্রেটো ফ্লুসি' প্রকাশ করেছে, যেখানে কৃষি ও পর্যটন খাতের জন্য কয়েক হাজার সিজনাল ওয়ার্ক ভিসা দেওয়া হচ্ছে।",
                "category": "ইউরোপ",
                "imageUrl": "/images/news2.jpg",
                "source": "দ্য লোকাল ইতালি",
                "is_featured": True
            },
            {
                "title": "ভিসা নিয়মে ওমানের নতুন আপডেট: প্রবাসীদের যা জানা প্রয়োজন",
                "description": "বিদেশি মেধা আকৃষ্ট করতে ওমান সরকার ফ্যামিলি জয়েনিং ভিসা এবং ইনভেস্টর ভিসার প্রক্রিয়াকে আরও সহজ করেছে।",
                "category": "ভিসা ও ইমিগ্রেশন",
                "imageUrl": "/images/news3.jpg",
                "source": "টাইমস অফ ওমান",
                "is_featured": True
            },
            {
                "title": "২০২৬ সালের জন্য স্টুডেন্ট ভিসার নিয়ম কঠোর করল নেদারল্যান্ডস",
                "description": "আগামী শিক্ষাবর্ষ থেকে নেদারল্যান্ডসে পড়তে ইচ্ছুক আন্তর্জাতিক শিক্ষার্থীদের জন্য ভাষার প্রয়োজনীয়তা এবং আর্থিক প্রমাণের থ্রেশহোল্ড আরও কঠোর করা হয়েছে।",
                "category": "ইউরোপ",
                "imageUrl": "/images/news4.jpg",
                "source": "ডাচ নিউজ",
                "is_trending": True
            },
            {
                "title": "এবছরের মধ্যেই ১০,০০০ স্বাস্থ্যকর্মী নিয়োগের লক্ষ্য কাতারের",
                "description": "চিকিৎসা খাতের বিশাল সম্প্রসারণের লক্ষ্যে কাতার দক্ষিণ এশিয়া এবং ফিলিপাইন থেকে প্রচুর ডাক্তার ও নার্স নিয়োগ করছে।",
                "category": "কর্মসংস্থান",
                "imageUrl": "/images/news5.jpg",
                "source": "গাল্ফ টাইমস",
                "is_trending": True
            }
        ]

        for item in news_data:
            cat = category_objects.get(item['category'])
            if cat:
                NewsArticle.objects.get_or_create(
                    title=item['title'],
                    defaults={
                        'description': item['description'],
                        'category': cat,
                        'image_url': item['imageUrl'],
                        'source': item['source'],
                        'is_featured': item.get('is_featured', False),
                        'is_trending': item.get('is_trending', False),
                        'views': 100
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded mock data'))
