from rest_framework.authentication import TokenAuthentication as BaseTokenAuth


class CustomTokenAuthentication(BaseTokenAuth):
    keyword = "Bearer"
