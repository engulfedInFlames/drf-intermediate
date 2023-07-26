from rest_framework import serializers
from rest_framework.reverse import reverse


from .models import Product
from .validators import validate_title_no_admin, validate_product_title_is_unique
from users.serializers import UserPublicSerializer


class ProductInlineSerializer(serializers.Serializer):
    # ModelSerializer에서는 class Meta로 model과 fields를 지정해야 한다.
    title = serializers.CharField(read_only=True)
    hyperlink = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field="pk",
        read_only=True,
    )


class ProductSerializer(serializers.ModelSerializer):
    # 없는 필드라도 데이터를 받을 수 있음
    # write_only=True를 하지 않으면 오류 발생
    # email = serializers.EmailField(write_only=True)

    title = serializers.CharField(
        validators=[
            validate_title_no_admin,
            validate_product_title_is_unique,
        ]
    )
    body = serializers.CharField(
        source="content",
        required=False,
    )
    user = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "pk",
            "title",
            "body",
            "price",
            "user",
        )

    def create(self, validated_data):
        # return Product.objects.create(**validated_data)
        return super().create(validated_data)


class ProductDetailSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(
    #     source="user.username",
    #     read_only=True,
    # )
    owner = UserPublicSerializer(
        source="user",
        read_only=True,
    )
    discounted_price = serializers.SerializerMethodField(read_only=True)
    # First
    url = serializers.SerializerMethodField(read_only=True)
    # Second
    hyperlink = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field="pk",
        read_only=True,
    )

    other_owned_products = ProductInlineSerializer(
        source="user.products.all",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "pk",
            "owner",
            "title",
            "content",
            "price",
            "discounted_price",
            "url",
            "hyperlink",
            "other_owned_products",
        )

    def get_discounted_price(self, obj):
        # save 메소드가 호출되기 전까지는 객체가 존재하지 않기 때문에 discounted_price 메소드를 호출할 수 없다.
        try:
            return obj.discounted_price
        except:
            return 0.00

    def get_url(self, obj):
        # return f"/api/products/{obj.pk}"
        # edit_url 등 필드 생성 가능
        request = self.context.get("request")
        if request is None:
            return None
        return reverse(
            "product-detail",
            kwargs={"pk": obj.pk},
            request=request,
        )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
