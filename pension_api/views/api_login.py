from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from pension_api.serializers.api_toke_serializer import ApiTokenSerializer
from pension_base.generic.execption.generi_execption import GenericException
from pension_base.models import ConsoleUser
from rest_framework_jwt.settings import api_settings
from rest_framework import status


class ApiLoginView(ObtainAuthToken):
    serializer_class = ApiTokenSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                users= ConsoleUser.objects.filter(user=serializer.validated_data['user'])
                current_user = users.first()
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(current_user.user)
                token = jwt_encode_handler(payload)
                _response = {
                    'token': token,
                    'success': True,
                    "login_info": {
                        "user_id": current_user.pk,
                        "username": current_user.user.username if current_user.user else None,
                        "designation": current_user.designation,
                        "name": current_user.name,
                    }
                }
                response = {
                    'results': _response
                }

                request.user = current_user
                return Response(response)
        except GenericException as exp:
            if hasattr(exp, 'status_code'):
                return Response(
                    {'message': exp.message, 'success': False},
                    status=exp.status_code
                )

        return Response(
            {'message': 'Cannot login with provided credentials.', 'success': False},
            status=status.HTTP_400_BAD_REQUEST
        )

