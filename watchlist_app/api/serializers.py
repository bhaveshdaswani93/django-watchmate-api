from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review



def validate_min_length(value):
    min_length = 5
    if len(value) < min_length:
        raise serializers.ValidationError(f"Value must be at least {min_length} characters long")
    return value
"""
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, validators=[validate_min_length])
    description = serializers.CharField()
    active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    def validate(self, attrs):
        if attrs.get('name') == attrs.get('description'):
            raise serializers.ValidationError("Name and description cannot be the same")
        return super().validate(attrs)
    
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short")
        return value
"""

class ReviewSerializer(serializers.ModelSerializer):
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
    reviews = ReviewSerializer(many=True, read_only=True)
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
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watch-list-detail'
    # )
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
