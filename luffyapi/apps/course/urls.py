from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('free', views.CouresView, 'free')
router.register('categories', views.CourseCategoryView, 'categories')
router.register('chapters', views.CourseChapterView, 'coursechapter')
router.register('search', views.CouresSearchView, 'search')
urlpatterns = [

]

urlpatterns.extend(router.urls)
