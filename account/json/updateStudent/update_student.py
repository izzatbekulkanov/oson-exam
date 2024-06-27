from django.contrib.sites import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def extract_bearer_token(token):
    # Tokenni "Bearer" so'zi orqasidan ajratamiz
    parts = token.split()
    # Agar tokenning uzunligi 2 bo'lmasa yoki birinchi qism "Bearer" emas bo'lsa, bo'sh qaytarib qo'yamiz
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    # Aks holda, "Bearer" so'zi keyingi bo'shliqdan keyin kelgan qismni qaytarib beramiz
    return parts[1]

@api_view(['GET'])
def get_student_info_profile(request):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1IiwianRpIjoiZmI4NzExMzdkYmVjNjdiZDA1ZjhlNWIwYmQ1MTQ0YjJhOWJmMTg2Mzc2MzZiNTE1MDM1MjY4YzBiMGQ1NWQ1YzU3OTYyZTllMmU5MzRiZTYiLCJpYXQiOjE3MTMwMjg1ODksIm5iZiI6MTcxMzAyODU4OSwiZXhwIjoxNzEzMDMyMTg5LCJzdWIiOiI0MTY2Iiwic2NvcGVzIjpbXX0.ollDiYVc-WJWgvHoDN9mykQa8YNgoh60oY0K3IfXUd0mUZLci0aUoh5M2zRwcEKPp0xN9iY7WMyQQjQu2axMeNJTcI6IUKPzMGHUIbXQjPgp-'
    # tokendan bearer tokenni ajratish va bearer_tokenga tenglash
    bearer_token = extract_bearer_token(token)

    print("Bearer Token:", bearer_token)

    url = 'https://student.namspi.uz/rest/v1/account/me'
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        return Response({"message": f"Student API dan ma'lumot olishda xatolik yuz berdi: {response.text}"}, status=response.status_code)
