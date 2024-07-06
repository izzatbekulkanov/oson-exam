from datetime import datetime

from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import CustomUser, Roles, Gender, StudentStatus, PaymentForm, Country, Province, District, \
    Accommodation, SocialCategory
from university.models import Specialty, EducationForm, EducationType, Department, EducationLang, Level, Semester, \
    GroupUniver, Curriculum, EducationYear

CLIENT_ID = '4'
CLIENT_SECRET = "sRfOvhFep_KA_IyvYIcGEfzzHqUcz4KfqYKMF7wB"
REDIRECT_URI = "https://webtest.namspi.uz/hemis/callback/student"
AUTHORIZE_URL = 'https://student.namspi.uz/oauth/authorize'
TOKEN_URL = 'https://student.namspi.uz/oauth/access-token'
RESOURCE_OWNER_URL = 'https://student.namspi.uz/oauth/api/user?fields=id,uuid,type,name,login,picture,email,university_id,phone'

from university.models import University
from .client import oAuth2Client


class OAuthAuthorizationStudentView(APIView):
    def get(self, request, *args, **kwargs):
        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        authorization_url = client.get_authorization_url()

        return redirect(authorization_url)
        # return Response(
        #     {
        #         'authorization_url': authorization_url
        #     },
        #     status=status.HTTP_200_OK)


def update_or_create_user(email, defaults):
    try:
        print('update or create user')
        user, created = CustomUser.objects.get_or_create(email=email, defaults=defaults)
        return user, created
    except IntegrityError:
        # Bazada allaqachon foydalanuvchi mavjud bo'lsa uni yangilab olamiz
        user = CustomUser.objects.get(email=email)
        for key, value in defaults.items():
            setattr(user, key, value)
        user.save()
        return user, False


class OAuthCallbackStudentView(APIView):
    def get(self, request, *args, **kwargs):
        full_info = {}
        auth_code = request.query_params.get('code')
        if not auth_code:
            return Response(
                {
                    'status': False,
                    'error': 'Authorization code is missing'
                },
                status=status.HTTP_400_BAD_REQUEST)

        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        access_token_response = client.get_access_token(auth_code)

        if 'access_token' in access_token_response:
            access_token = access_token_response['access_token']
            user_details = client.get_user_details(access_token)
            full_info['details'] = user_details
            full_info['token'] = access_token

            # Malumotlarni user_data ichiga saqlash
            user_data = user_details.get('data', {})
            print(user_data)

            # Tranzaksiya boshlanishi
            with transaction.atomic():
                gender = user_data.get('gender')
                if gender:
                    gender_code = gender.get('code')
                    gender_name = gender.get('name')
                    gender_instance, _ = Gender.objects.get_or_create(code=gender_code, name=gender_name)
                    print("Shu Jinsi:", gender_instance)

                # specialty = user_data.get('specialty')
                # if specialty:
                #     print(specialty)
                #     specialty_code = specialty.get('code')
                #     print(specialty_code)
                #     specialty_instance, _ = Specialty.objects.get_or_create(code=specialty_code)
                #     print("Shu Jinsi:", specialty_instance)

                studentStatus = user_data.get('studentStatus')
                if studentStatus:
                    studentStatus_code = studentStatus.get('code')
                    studentStatus_name = studentStatus.get('name')
                    studentStatus_instance, _ = StudentStatus.objects.get_or_create(code=studentStatus_code,
                                                                                    name=studentStatus_name)
                    print("Shu Talaba statusi:", studentStatus_instance)

                education_form = user_data.get('educationForm')
                if education_form:
                    education_form_code = education_form.get('code')
                    education_form_name = education_form.get('name')
                    education_form_instance, _ = EducationForm.objects.get_or_create(code=education_form_code,
                                                                                     name=education_form_name)
                    print("Shu Ta'lim shakli:", education_form_instance)

                education_type = user_data.get('educationType')
                if education_type:
                    education_type_code = education_type.get('code')
                    education_type_name = education_type.get('name')
                    education_type_instance, _ = EducationType.objects.get_or_create(code=education_type_code,
                                                                                     name=education_type_name)
                    print("Shu Ta'lim turi:", education_type_instance)

                payment_form = user_data.get('paymentForm')
                if payment_form:
                    payment_form_code = payment_form.get('code')
                    payment_form_name = payment_form.get('name')
                    payment_form_instance, _ = PaymentForm.objects.get_or_create(code=payment_form_code,
                                                                                 name=payment_form_name)
                    print("Shu To'lov shakli:", payment_form_instance)

                group = user_details.get('groups')
                if group:
                    group_id = group[0].get('id')
                    group_instance, _ = GroupUniver.objects.get_or_create(codeID=group_id)
                    print("Shu Guruh:", group_instance)

                    curriculum = group[0].get('curriculum', {})
                    if curriculum:
                        curriculum_id = curriculum.get('id')
                        curriculum_instance = Curriculum.objects.filter(codeID=curriculum_id).first()
                        print("Shu Curiculum:", curriculum_instance)

                department = user_data.get('faculty')
                if department:
                    department_id = department.get('id')
                    department_instance, _ = Department.objects.get_or_create(codeID=department_id)
                    print("Shu Fakultet:", department_instance)

                education_lang = user_data.get('educationLang')
                if education_lang:
                    education_lang_code = education_lang.get('code')
                    education_lang_name = education_lang.get('name')
                    education_lang_instance, _ = EducationLang.objects.get_or_create(code=education_lang_code,
                                                                                     name=education_lang_name)
                    print("Shu Ta'lim tili:", education_lang_instance)

                level = user_data.get('level')
                if level:
                    level_code = level.get('code')
                    level_name = level.get('name')
                    level_instance, _ = Level.objects.get_or_create(code=level_code, name=level_name)
                    print("Shu Darslik:", level_instance)

                semester = user_data.get('semester')
                if semester:
                    semester_id = semester.get('id')
                    semester_code = semester.get('code')
                    semester_name = semester.get('name')
                    semester_instance, _ = Semester.objects.get_or_create(id=semester_id, code=semester_code,
                                                                          name=semester_name)
                    print("Shu Semestr:", semester_instance)

                    education_year = semester.get('education_year', {})
                    if education_year:
                        education_year_code = education_year.get('code')
                        education_year_name = education_year.get('name')
                        education_year_instance, _ = EducationYear.objects.get_or_create(code=education_year_code,
                                                                                         name=education_year_name)
                        print("Shu O'quv yili:", education_year_instance)

                country = user_data.get('country')
                if country:
                    country_code = country.get('code')
                    country_name = country.get('name')
                    country_instance, _ = Country.objects.get_or_create(code=country_code, name=country_name)
                    print("Shu Mamlakat:", country_instance)

                province = user_data.get('province')
                if province:
                    province_code = province.get('code')
                    province_name = province.get('name')
                    province_instance, _ = Province.objects.get_or_create(code=province_code, name=province_name)
                    print("Shu Viloyat:", province_instance)

                district = user_data.get('district')
                if district:
                    district_code = district.get('code')
                    district_name = district.get('name')
                    district_instance, _ = District.objects.get_or_create(code=district_code, name=district_name)
                    print("Shu Tuman:", district_instance)

                social_category = user_data.get('socialCategory')
                if social_category:
                    social_category_code = social_category.get('code')
                    social_category_name = social_category.get('name')
                    social_category_instance, _ = SocialCategory.objects.get_or_create(code=social_category_code,
                                                                                       name=social_category_name)
                    print("Shu Ijtimoiy kategoriya:", social_category_instance)

                accommodation = user_data.get('accommodation')
                if accommodation:
                    accommodation_code = accommodation.get('code')
                    accommodation_name = accommodation.get('name')
                    accommodation_instance, _ = Accommodation.objects.get_or_create(code=accommodation_code,
                                                                                    name=accommodation_name)
                    print("Shu Yashash joyi:", accommodation_instance)

                # Tranzaksiya muvaffaqiyatli amalga oshirildi

            # Foydalanuvchi modeliga foydalanuvchi ma'lumotlarini qo'shish

            # Foydalanuvchi ma'lumotlarini olish
            student_id_number = user_details.get('student_id_number', None)
            old_date_str = user_details.get('birth_date', '')
            if old_date_str:
                # Convert the old date string to datetime object
                old_date = datetime.strptime(old_date_str, '%d-%m-%Y')

                # Convert datetime object to new string format 'YYYY-MM-DD'
                new_date_str = old_date.strftime('%Y-%m-%d')
            else:
                new_date_str = None
            existing_user = CustomUser.objects.filter(student_id_number=student_id_number).first()
            if existing_user:
                # Tekshirish: student_id_number ga teng foydalanuvchi mavjudmi?
                id_number = user_details.get('id', '')  # id bilan
                username = ('talaba' + str(id_number)).lower()
                # Foydalanuvchi malumotlarini yangilash
                existing_user.full_name = user_details.get('name', '')
                existing_user.first_name = user_details.get('firstname', '')
                existing_user.second_name = user_details.get('surname', '')
                existing_user.username = username
                existing_user.third_name = user_details.get('patronymic', '')
                existing_user.hash = user_data.get('hash', '')
                existing_user.birth_date = new_date_str
                existing_user.phone_number = user_details.get('phone', '')
                existing_user.token = access_token_response
                existing_user.image = user_details.get('picture', '')

                existing_user.educationYear = education_year_instance
                existing_user.level = level_instance
                existing_user.semester = semester_instance
                existing_user.country = country_instance
                existing_user.province = province_instance
                existing_user.district = district_instance
                existing_user.socialCategory = social_category_instance
                existing_user.accommodation = accommodation_instance
                existing_user.group = group_instance
                existing_user.department = department_instance
                existing_user.curriculum = curriculum_instance
                # existing_user.specialty = specialty_instance
                existing_user.accommodation = accommodation_instance
                existing_user.paymentForm = payment_form_instance
                existing_user.studentStatus = studentStatus_instance


                existing_user.save()
                oauth_login(request, existing_user.email, existing_user)  # Faydalanuvchini login qiling
            else:
                print('sadasdasd')
                # Yangi foydalanuvchi yaratish
                university_code = user_details.get('university_id', '')
                university = University.objects.get(code=university_code)
                id_number = user_details.get('id', '')  # id bilan
                username = ('talaba' + str(id_number)).lower()
                email = user_details.get('email', None)

                if not email:
                    email = f'talaba{id_number}@namdpi.uz'.lower()
                user_type = user_details.get('type', '')
                if user_type == 'teacher':
                    user_type = '3'  # o'qituvchi
                elif user_type == 'employee':
                    user_type = '2'  # Hodim
                elif user_type == 'student':
                    user_type = '1'  # Talaba

                user, created = CustomUser.objects.update_or_create(
                    email=email,
                    defaults={
                        'email': email,  # Foydalanuvchining email manzili
                        'student_id_number': student_id_number,
                        'university': university,
                        'full_id': student_id_number,
                        'full_name': user_details.get('name', ''),
                        'first_name': user_details.get('firstname', ''),
                        'second_name': user_details.get('surname', ''),
                        'username': username,
                        'gender': gender_instance,
                        # 'specialty': specialty_instance,
                        'department': department_instance,
                        'group': group_instance,
                        'paymentForm': payment_form_instance,
                        'curriculum': curriculum_instance,
                        'studentStatus': studentStatus_instance,
                        'socialCategory': social_category_instance,
                        'educationYear': education_year_instance,
                        'educationType': education_type_instance,
                        'educationForm': education_form_instance,
                        'level': level_instance,
                        'semester': semester_instance,
                        'country': country_instance,
                        'district': district_instance,
                        'province': province_instance,
                        'accommodation': accommodation_instance,
                        'third_name': user_details.get('patronymic', ''),
                        'birth_date': new_date_str,
                        'phone_number': user_details.get('phone', ''),
                        'token': access_token,
                        'image': user_details.get('picture', ''),
                        'address': user_details.get('address', ''),
                        'now_role': 'Student',
                        'user_type': user_type,
                        'hash': user_data.get('hash', ''),
                        'is_followers_book': True,
                        'is_student': True,
                        'is_employee': False,
                        # Boshqa ma'lumotlar
                    }
                )


                # Ro'larni qo'shish
                if 'roles' in user_details:
                    roles = user_details['roles']
                    for role in roles:
                        role_code = role.get('code', '')
                        role_name = role.get('name', '')
                        role_instance, created = Roles.objects.get_or_create(code=role_code, name=role_name)
                        user.hemis_role.add(role_instance)

                # Foydalanuvchini "Guest" guruhiga qo'shish
                guest_group, created = Group.objects.get_or_create(name='Student')
                user.groups.add(guest_group)

                oauth_login(request, email, user)  # Faydalanuvchini login qiling

            # return Response(full_info, status=status.HTTP_200_OK)
            return redirect('dashboard')
        else:
            return Response(
                {
                    'status': False,
                    'error': 'Failed to obtain access token'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


def oauth_login(request, email, user):
    # Faydalanuvchi obyektini olish
    # user = get_object_or_404(CustomUser, email=email)

    # Faydalanuvchini avtorizatsiya qilish
    user.backend = 'django.contrib.auth.backends.ModelBackend'  # Faydalanuvchi uchun kerakli backendni aniqlash
    login(request, user)