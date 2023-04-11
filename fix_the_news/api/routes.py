from rest_framework.routers import DefaultRouter
from fix_the_news.api.comments import views as comments_views
from fix_the_news.api.communications import views as communications_views
from fix_the_news.api.likes import views as likes_views
from fix_the_news.api.news_items import views as news_items_views
from fix_the_news.api.users import views as user_views
from fix_the_news.api.subscriptions import views as subscription_views
from fix_the_news.api.topics import views as topics_views

api_router = DefaultRouter()
api_router.register(r'comments', comments_views.CommentViewSet)
api_router.register(
    r'communications', communications_views.CommunicationViewSet)
api_router.register(r'likes', likes_views.LikeViewSet)
api_router.register(r'messages', user_views.MessageViewSet)
api_router.register(r'news-items', news_items_views.NewsItemViewSet)
api_router.register(r'subscriptions', subscription_views.SubscriptionViewSet)
api_router.register(r'topics', topics_views.TopicViewSet)
