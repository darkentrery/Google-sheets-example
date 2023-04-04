from rest_framework import serializers

from google_sheets.supplies.models import Supply


class SupplySerializer(serializers.ModelSerializer):
    cost_rub = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Supply
        fields = ["number", "order", "cost", "date", "cost_rub"]
        read_only_fields = fields