from rest_framework.authentication import TokenAuthentication as BaseTokenAuth #to override the TokenAuthentication class

class TokenAuthentication(BaseTokenAuth):
    keyword = 'Token'