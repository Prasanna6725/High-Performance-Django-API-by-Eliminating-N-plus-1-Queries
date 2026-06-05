from django.db.models import Count, IntegerField, OuterRef, Subquery, Sum
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from api.models import Post


def _serialize_posts(posts, include_total_author_views=False):
	response = []
	for post in posts:
		item = {
			"id": post.id,
			"title": post.title,
			"author_name": post.author.name,
			"comment_count": post.comments.count(),
		}
		if include_total_author_views:
			item["total_author_views"] = post.total_author_views
		response.append(item)
	return response


@require_GET
def healthz(_request):
	return JsonResponse({"status": "ok"})


@require_GET
def naive_posts(_request):
	posts = Post.objects.all().order_by("id")
	return JsonResponse(_serialize_posts(posts), safe=False)


@require_GET
def optimized_posts(_request):
	posts = (
		Post.objects.select_related("author")
		.annotate(comment_count=Count("comments"))
		.order_by("id")
	)
	response = [
		{
			"id": post.id,
			"title": post.title,
			"author_name": post.author.name,
			"comment_count": post.comment_count,
		}
		for post in posts
	]
	return JsonResponse(response, safe=False)


@require_GET
def advanced_posts(_request):
	author_totals = (
		Post.objects.filter(author_id=OuterRef("author_id"))
		.values("author_id")
		.annotate(total_views=Sum("views"))
		.values("total_views")
	)
	posts = (
		Post.objects.select_related("author")
		.annotate(
			comment_count=Count("comments"),
			total_author_views=Subquery(author_totals, output_field=IntegerField()),
		)
		.order_by("id")
	)
	response = [
		{
			"id": post.id,
			"title": post.title,
			"author_name": post.author.name,
			"comment_count": post.comment_count,
			"total_author_views": post.total_author_views,
		}
		for post in posts
	]
	return JsonResponse(response, safe=False)
