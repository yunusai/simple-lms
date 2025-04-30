from django.shortcuts import render
from django.db.models import Count, Avg
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.

# Insert data user & Cek di DB viewer
User.objects.create_user(username="usertesting", email="usertest@email.com", 
                         password="sanditesting")
# Insert data course & Cek di DB viewer
Course.objects.create(name=row['name'], description=row['description'], 
					  price=row['price'], teacher=User.objects.get(pk=1))

# Select all data user
#     Tampilkan di HTML
#     Tampilkan melalui JSONResponse
# Select get
#     Tampilkan di HTML
# Select where user
# Update data user
# Delete data user
# Delete all course data
# Delete all user data except
def testing(request):
    user_test = User.objects.filter(username="usertesting")
    if not user_test.exists():
        user_test = User.objects.create_user(
                            username="usertesting", 
                            email="usertest@email.com", 
                            password="sanditesting")
    all_users = serializers.serialize('python', User.objects.all())

    admin = User.objects.get(pk=1)
    user_test.delete()

    after_delete = serializers.serialize('python', User.objects.all())

    response = {
            "admin_user": serializers.serialize('python', [admin])[0],
            "all_users" : all_users,
            "after_del" : after_delete,
        }
    return JsonResponse(response)

# Select course with teacher data
def allCourse(request):
    allCourse = Course.objects.all()
    result = []
    for course in allCourse:
        record = {'id': course.id, 'name': course.name, 
                  'description': course.description, 
                  'price': course.price,
                  'teacher': {
                      'id': course.teacher.id,
                      'username': course.teacher.username,
                      'email': course.teacher.email,
                      'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
                  }}
        result.append(record)
    return JsonResponse(result, safe=False)

# Select user data & his courses (as teacher)
def userCourses(request):
    user = User.objects.get(pk=3)
    courses = Course.objects.filter(teacher=user.id)
    course_data = []
    for course in courses:
        record = {'id': course.id, 'name': course.name, 
                  'description': course.description, 'price': course.price}
        course_data.append(record)
    result = {'id': user.id, 'username': user.username, 'email': user.email, 
              'fullname': f"{user.first_name} {user.last_name}", 
              'courses': course_data}
    return JsonResponse(result, safe=False)

# Select course data with aggregate
def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(max_price=Max('price'),
                                min_price=Min('price'),
                                avg_price=Avg('price'))
    result = {'course_count': len(courses), 'courses': stats}
    return JsonResponse(result, safe=False)

# Select filter course data with aggregate
def courseMemberStat(request):
    courses = Course.objects.filter(description__contains='python') \
                            .annotate(member_num=Count('coursemember'))
    course_data = []
    for course in courses:
        record = {'id': course.id, 'name': course.name, 'price': course.price, 
                  'member_count': course.member_num}
        course_data.append(record)
    result = {'data_count': len(course_data), 'data':course_data}
    return JsonResponse(result)

# Statistik Semua Course:

#     jumlah semua course,
#     course dengan harga tertinggi,
#     course dengan harga terendah,
#     course dengan jumlah member terbanyak,
#     course dengan jumlah member paling sedikit

def courseStat(request):
  courses = Course.objects.all()
  stats = courses.aggregate(max_price=Max('price'),
                              min_price=Min('price'),
                              avg_price=Avg('price'))
  cheapest = Course.objects.filter(price=stats['min_price'])
  expensive = Course.objects.filter(price=stats['max_price'])
  popular = Course.objects.annotate(member_count=Count('coursemember'))\
                          .order_by('-member_count')[:5]
  unpopular = Course.objects.annotate(member_count=Count('coursemember'))\
                          .order_by('member_count')[:5]

  result = {'course_count': len(courses), 'courses': stats,
            'cheapest': serializers.serialize('python', cheapest), 
            'expensive': serializers.serialize('python', expensive),
            'popular': serializers.serialize('python', popular), 
            'unpopular': serializers.serialize('python', unpopular)}
  return JsonResponse(result, safe=False)


# Detail Statistik Course:

#     Detail course
#     Jumlah member
#     jumlah konten
#     jumlah semua komentar
#     konten yang paling banyak dikomentari
def courseDetail(request, course_id):
   course = Course.objects.annotate(member_count=Count('coursemember'), 
                                 content_count=Count('coursecontent'),
                                 comment_count=Count('coursecontent__comment'))\
                           .get(pk=course_id)
   contents = CourseContent.objects.filter(course_id=course.id)\
               .annotate(count_comment=Count('comment'))\
               .order_by('-count_comment')[:3]
   result = {"name": course.name, 'description': course.description, 'price': course.price, 
             'member_count': course.member_count, 'content_count': course.content_count,
             'teacher': {'username': course.teacher.username, 'email': 
                         course.teacher.email, 'fullname': course.teacher.first_name},
             'comment_stat': {'comment_count': course.comment_count, 
                              'most_comment':[{'name': content.name, 
			                               'comment_count': content.count_comment} 
			                               for content in contents]},
             }

   return JsonResponse(result)

# Select related
# Select prefetch
# Input data massal
with open(filepath+'contents.json') as jsonfile:
    comments = json.load(jsonfile)
    obj_create = []
    for num, row in enumerate(comments):
        if not CourseContent.objects.filter(pk=num+1).exists():
            obj_create.append(CourseContent(
			            course_id=Course.objects.get(pk=int(row['course_id'])), 
						 video_url=row['video_url'], name=row['name'], 
						 description=row['description'], id=num+1))
    CourseContent.objects.bulk_create(obj_create)


with open(filepath+'comments.json') as jsonfile:
    comments = json.load(jsonfile)
    obj_create = []
    for num, row in enumerate(comments):
        if int(row['user_id']) > 50:
            row['user_id'] = randint(5, 40)
        if not Comment.objects.filter(pk=num+1).exists():
            obj_create.append(Comment(
			            content_id=CourseContent.objects.get(pk=int(row['content_id'])), 
					   user_id=User.objects.get(pk=int(row['user_id'])), id=num+1,
					   comment=row['comment']))
    Comment.objects.bulk_create(obj_create)
    
    
# Jika menjadi 1
def statistics_view(request):
    # 1. Jumlah user yang membuat course
    users_with_courses = User.objects.filter(course_set__isnull=False).distinct().count()

    # 2. Jumlah user yang tidak memiliki course
    users_without_courses = User.objects.filter(course_set__isnull=True).count()

    # 3. Rata-rata jumlah course yang diikuti 1 user
    avg_courses_followed = User.objects.annotate(
        num_courses=Count('enrolled_courses')
    ).aggregate(avg_courses=Avg('num_courses'))['avg_courses'] or 0

    # 4. User yang mengikuti course terbanyak
    top_user = User.objects.annotate(
        num_courses=Count('enrolled_courses')
    ).order_by('-num_courses').first()

    # 5. List user yang tidak mengikuti course sama sekali
    users_not_following = User.objects.filter(enrolled_courses__isnull=True)

    # Siapkan respons
    response = {
        'users_with_courses': users_with_courses,
        'users_without_courses': users_without_courses,
        'avg_courses_followed': round(avg_courses_followed, 2),
        'top_user': {
            'id': top_user.id,
            'username': top_user.username,
            'num_courses': top_user.num_courses
        } if top_user else None,
        'users_not_following': [
            {'id': user.id, 'username': user.username}
            for user in users_not_following
        ],
    }
    return JsonResponse(response)

# Jika dipisah
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from .models import Course, CourseMember

# Jumlah user yang membuat course
def users_with_courses_count(request):
    """Jumlah user yang membuat course."""
    count = User.objects.filter(course_set__isnull=False).distinct().count()
    response = {
        'users_with_courses': count
    }
    return JsonResponse(response)

# Jumlah user yang tidak memiliki course
def users_without_courses_count(request):
    """Jumlah user yang tidak memiliki course."""
    count = User.objects.filter(course_set__isnull=True).count()
    response = {
        'users_without_courses': count
    }
    return JsonResponse(response)

# Rata2 jumlah course yang diikuti 1 user
def avg_courses_followed(request):
    """Rata-rata jumlah course yang diikuti per user."""
    avg = User.objects.annotate(
        num_courses=Count('coursemember')
    ).aggregate(avg_courses=Avg('num_courses'))['avg_courses'] or 0
    response = {
        'avg_courses_followed': round(avg, 2)
    }
    return JsonResponse(response)

# User yang mengikuti course terbanyak
def top_course_follower(request):
    """User yang mengikuti course terbanyak."""
    top_user = User.objects.annotate(
        num_courses=Count('coursemember')
    ).order_by('-num_courses').first()
    response = {
        'top_user': {
            'id': top_user.id,
            'username': top_user.username,
            'num_courses': top_user.num_courses
        } if top_user else None
    }
    return JsonResponse(response)

# List user yang tidak mengikuti course sama sekali
def users_not_following_courses(request):
    """List user yang tidak mengikuti course sama sekali."""
    users = User.objects.filter(coursemember__isnull=True)
    response = {
        'users_not_following': [
            {'id': user.id, 'username': user.username}
            for user in users
        ]
    }
    return JsonResponse(response)