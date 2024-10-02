from rest_framework import serializers
from movies import models


class moviesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
            "review",
            "rating",
            "created_at",
            "Review_by",
        )
        model = models.movies