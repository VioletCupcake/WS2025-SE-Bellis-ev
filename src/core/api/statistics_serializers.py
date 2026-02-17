from rest_framework import serializers

from core.models import StatistikPreset


class StatisticsRequestSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    filters = serializers.JSONField(required=False, default=dict)
    modules = serializers.ListField(child=serializers.DictField(), required=False, default=list)

    def validate(self, attrs):
        date_from = attrs["date_from"]
        date_to = attrs["date_to"]
        if date_from > date_to:
            raise serializers.ValidationError({"date_to": "date_to must be on/after date_from"})
        return attrs


class StatsPresetSerializer(serializers.ModelSerializer):
    scope = serializers.SerializerMethodField()
    payload = serializers.JSONField(source='filter_config')
    owner = serializers.PrimaryKeyRelatedField(source='erstellt_von', read_only=True)
    is_system = serializers.BooleanField(source='ist_system_preset', read_only=True)
    created_at = serializers.DateTimeField(source='erstellungsdatum', read_only=True)

    class Meta:
        model = StatistikPreset
        fields = [
            "preset_id",
            "name",
            "scope",
            "owner",
            "is_system",
            "payload",
            "created_at",
        ]
        read_only_fields = ["preset_id", "owner", "is_system", "created_at"]

    def get_scope(self, obj):
        return "GLOBAL" if obj.ist_global else "PERSONAL"


class StatsPresetCreateSerializer(serializers.ModelSerializer):
    scope = serializers.ChoiceField(choices=[("PERSONAL", "Persönlich"), ("GLOBAL", "Für alle")], write_only=True)
    payload = serializers.JSONField(source='filter_config')

    class Meta:
        model = StatistikPreset
        fields = ["name", "scope", "payload"]

    def create(self, validated_data):
        scope = validated_data.pop('scope', 'PERSONAL')
        validated_data['ist_global'] = (scope == 'GLOBAL')
        return super().create(validated_data)

