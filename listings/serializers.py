# serializers.py
from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    # Frontend-only helper fields
    customcategory = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    custombrand = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    customLocation = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price",

            "category",
            "customcategory",

            "brand",
            "custombrand",

            "condition",

            "province",
            "town",
            "village",
            "customLocation",

            "address",
        ]
        read_only_fields = ("user",)

    def validate(self, attrs):
        # CATEGORY
        if attrs.get("category") == "Other":
            custom = attrs.get("customcategory")
            if not custom:
                raise serializers.ValidationError({
                    "customcategory": "Custom category is required."
                })
            attrs["category"] = custom

        # BRAND
        if attrs.get("brand") == "Other":
            custom = attrs.get("custombrand")
            if not custom:
                raise serializers.ValidationError({
                    "custombrand": "Custom brand is required."
                })
            attrs["brand"] = custom

        # LOCATION → village
        if attrs.get("town") == "Other":
            custom_location = attrs.get("customLocation")
            if not custom_location:
                raise serializers.ValidationError({
                    "customLocation": "Village is required."
                })
            attrs["village"] = custom_location

        # Cleanup frontend-only fields
        attrs.pop("customcategory", None)
        attrs.pop("custombrand", None)
        attrs.pop("customLocation", None)

        return attrs
