from django.shortcuts import render

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