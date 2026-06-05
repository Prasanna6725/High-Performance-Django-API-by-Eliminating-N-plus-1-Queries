from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from api.models import Author, Comment, Post


class Command(BaseCommand):
    help = "Seed the blog database with authors, posts, and comments."

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(42)

        with transaction.atomic():
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Author.objects.all().delete()

            authors = [
                Author(name=f"{fake.unique.name()} {index}", bio=fake.text(max_nb_chars=200))
                for index in range(20)
            ]
            Author.objects.bulk_create(authors, batch_size=20)
            authors = list(Author.objects.order_by("id"))

            posts = []
            for author in authors:
                for index in range(10):
                    posts.append(
                        Post(
                            author=author,
                            title=fake.sentence(nb_words=6).rstrip("."),
                            content=fake.paragraph(nb_sentences=5),
                            views=fake.random_int(min=0, max=5000),
                            published_at=timezone.now(),
                        )
                    )
            Post.objects.bulk_create(posts, batch_size=200)
            posts = list(Post.objects.order_by("id"))

            comments = []
            for post in posts:
                for index in range(10):
                    comments.append(
                        Comment(
                            post=post,
                            author_name=fake.name(),
                            body=fake.sentence(nb_words=14),
                            created_at=timezone.now(),
                        )
                    )
            Comment.objects.bulk_create(comments, batch_size=500)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
