from rest_framework import serializers

from api.utils import get_day_name_from_int
from schedule.models import Course, Lesson, Program, Section


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    kod = serializers.CharField(source="code")
    ders_adi = serializers.CharField(source="name")

    class Meta:
        model = Course
        fields = ("id", "kod", "ders_adi")


class LessonSerializer(serializers.ModelSerializer):
    bina = serializers.SerializerMethodField()
    derslik = serializers.SerializerMethodField()
    gun = serializers.SerializerMethodField()
    saat1 = serializers.SerializerMethodField()
    saat2 = serializers.SerializerMethodField()

    def get_bina(self, obj):
        if obj.building:
            return obj.building.name
        else:
            return ""

    def get_derslik(self, obj):
        return obj.room or ""

    def get_gun(self, obj):
        if not obj.day:
            return ""

        return get_day_name_from_int(obj.day)

    def get_saat1(self, obj):
        if obj.start_time:
            return obj.start_time.strftime("%H%M")
        else:
            return ""

    def get_saat2(self, obj):
        if obj.end_time:
            return obj.end_time.strftime("%H%M")
        else:
            return ""

    class Meta:
        model = Lesson
        fields = ("bina", "derslik", "gun", "saat1", "saat2")


class SectionSerializer(serializers.ModelSerializer):
    kod = serializers.CharField(source="code")
    ogretim_uyesi = serializers.SerializerMethodField()
    bloklar = serializers.SerializerMethodField()
    bina = serializers.SerializerMethodField()
    gun = serializers.SerializerMethodField()
    derslik = serializers.SerializerMethodField()
    ders_adi = serializers.SerializerMethodField()
    saat = serializers.SerializerMethodField()

    def get_ogretim_uyesi(self, obj):
        if obj.lecturer:
            return obj.lecturer.name
        else:
            return ""

    def get_bloklar(self, obj):
        lessons = obj.lessons.all().order_by("day")
        serializer = LessonSerializer(lessons, many=True)

        return serializer.data

    def get_bina(self, obj):
        lessons = obj.lessons.all()
        buildings = lessons.values_list("building__code", flat=True)
        buildings = filter(lambda x: bool(x), buildings)

        if not buildings:
            return "---"

        return " ".join(buildings)

    def get_gun(self, obj):
        lessons = obj.lessons.all()
        days = lessons.values_list("day", flat=True) or []
        return " ".join(map(get_day_name_from_int, days))

    def get_derslik(self, obj):
        lessons = obj.lessons.all()
        rooms = [l.room or "" for l in lessons]

        return " ".join(rooms)

    def get_ders_adi(self, obj):
        return obj.course.name

    def get_saat(self, obj):
        def get_time_string(obj):
            if obj.start_time:
                start_time = obj.start_time.strftime("%H:%M")
            else:
                start_time = ""

            if obj.end_time:
                end_time = obj.end_time.strftime("%H:%M")
            else:
                end_time = ""

            return start_time + "/" + end_time

        lessons = obj.lessons.all()
        return " ".join(map(get_time_string, lessons))

    class Meta:
        model = Section
        fields = ("id", "kod", "ogretim_uyesi", "bloklar", "bina", "gun", "derslik", "ders_adi", "saat")
