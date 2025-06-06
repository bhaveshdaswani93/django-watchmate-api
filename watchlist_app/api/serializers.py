from rest_framework import serializers
from watchlist_app.models import Movie



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
class MovieSerializer(serializers.ModelSerializer):
    name_length = serializers.SerializerMethodField()
    def get_name_length(self, obj):
        return len(obj.name)
    
    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ['id', 'active']
        extra_kwargs = {
            'name': {'validators': [validate_min_length]},
            'description': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, attrs):
        if attrs.get('name') == attrs.get('description'):
            raise serializers.ValidationError("Name and description cannot be the same")
        return super().validate(attrs)
