from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review



def validate_min_length(value):
    min_length = 5
    if len(value) < min_length:
        raise serializers.ValidationError(f"Value must be at least {min_length} characters long")
    return value

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)  # Assuming you want to show the username

    class Meta:
        model = Review  # Using the through model for many-to-many relationship
        fields = '__all__'
        # exclude = ['id', 'active']
        extra_kwargs = {
            # 'rating': {'validators': [validate_min_length]},
            'description': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, attrs):
        if attrs.get('rating') < 1 or attrs.get('rating') > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return super().validate(attrs)

class WatchListSerializer(serializers.ModelSerializer):
    title_length = serializers.SerializerMethodField()
    platform = serializers.StringRelatedField(read_only=True)  # Assuming you want to show the platform name
    # reviews = ReviewSerializer(many=True, read_only=True)
    def get_title_length(self, obj):
        return len(obj.title)
    
    class Meta:
        model = WatchList
        fields = '__all__'
        # exclude = ['id', 'active']
        extra_kwargs = {
            'title': {'validators': [validate_min_length]},
            'storyline': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, attrs):
        if attrs.get('title') == attrs.get('storyline'):
            raise serializers.ValidationError("Name and storyline cannot be the same")
        return super().validate(attrs)

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
        # exclude = ['id', 'active']
        extra_kwargs = {
            'name': {'validators': [validate_min_length]},
            'about': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, attrs):
        if attrs.get('name') == attrs.get('about'):
            raise serializers.ValidationError("Name and about cannot be the same")
        return super().validate(attrs)
