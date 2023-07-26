from django.contrib.auth import get_user_model


from rest_framework import serializers

from .models import CustomUser

User = get_user_model()


class UserProductsSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    price = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True,
    )
    hyperlink = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field="pk",
        read_only=True,
    )


class UserPublicSerializer(serializers.ModelSerializer):
    # other_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            # "other_products",
        )
        read_only_fields = (
            "pk",
            "username",
        )

    # def get_other_products(self, obj):
    #     other_products = obj.products.all()[:3]
    #     return UserProductsSerializer(
    #         other_products,
    #         many=True,
    #         context=self.context,
    #     ).data
