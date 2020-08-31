from functools import reduce
import operator
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from pension_api.manager.api_manager import ApiManager
from pension_base.engine.pagination.standard_pagination import StandardResultsSetPagination
from pension_base.models import ConsoleUser

__author__ = 'Fazlul Kabir Shohag'


class DomainEntityView(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination

    def __init__(self, **kwargs):
        self.model = self.serializer_class.Meta.model
        super().__init__(**kwargs)

    def get_queryset(self):
        _api = ApiManager()

        search_bys = self.request.GET.get("search_by", None)
        filter_names = self.request.GET.getlist("filter_name", None)
        filter_values = self.request.GET.getlist("filter_value", None)
        sort_bys = self.request.GET.getlist("sort_by", _api.default_sort_by)

        if not sort_bys:
            raise ValueError("The default sort by is not in the view's sorts list")

        search_list = _api.get_search_list(search_bys)
        filter_list = _api.get_filter_list(filter_names, filter_values)
        sort_list = _api.get_sort_list(sort_bys)

        # Search, filter, sort
        if search_list:
            list_of_search_bys_Q = [Q(**{key: value}) for key, value in search_list.items()]
            search_reduce = reduce(operator.or_, list_of_search_bys_Q)
        else:
            search_reduce = None

        if filter_list:
            list_of_filter_bys_Q = [[Q(**{key: value}) for value in array] for key, array in filter_list.items()]
            reduced_filters = []

            for array in list_of_filter_bys_Q:
                reduced_filters.append(reduce(operator.or_, array))

            filter_reduce = reduce(operator.and_, reduced_filters)
            _api.using_filters = True
        else:
            filter_reduce = None
            _api.using_filters = False

        if search_reduce and filter_reduce:
            queryset = self.model.objects.filter(search_reduce).filter(filter_reduce).defer(
                *_api.deferments).distinct().order_by(*sort_list)
        elif search_reduce:
            queryset = self.model.objects.filter(search_reduce).defer(*_api.deferments).distinct().order_by(
                *sort_list)
        elif filter_reduce:
            queryset = self.model.objects.filter(filter_reduce).defer(*_api.deferments).distinct().order_by(
                *sort_list)
        else:
            queryset = self.model.objects.defer(*_api.deferments).order_by(*sort_list)
            # queryset = sorted(self.model.objects.all(), key=lambda x: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', x.name)])

            # TODO: Find a way to natural sort the queryset
            # SELECT * FROM job
            # ORDER BY(substring('name', '^[0-9]+'))::int -- cast to integer\
            #     , coalesce(substring('name', '[^0-9_].*$'), '')

        _api.filtered_object_count = queryset.count()

        return queryset

    def perform_create(self, serializer):
        if self.request.user and User.objects.filter(pk=self.request.user.pk).exists():
            current_user = ConsoleUser.objects.filter(user=self.request.user).first()
            serializer.validated_data['created_by'] = current_user
            serializer.validated_data['last_updated_by'] = current_user
        return super(DomainEntityView, self).perform_create(serializer)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            _response = {
                'results': serializer.data
            }
            return Response(_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
       Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        _response = {
            'results': serializer.data
        }
        return Response(_response)

    def get(self, request, pk):
        queryset = self.get_queryset().get(pk)
        serializer = self.serializer_class(queryset)
        _response = {
            'results': serializer.data
        }
        return Response(_response, status=status.HTTP_200_OK)

    def put(self, request, pk):

        queryset = self.get_queryset().get(pk)

        if request.user == queryset.created_by:  # If creator is who makes request
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                _response = {
                    'results': serializer.data
                }
                return Response(_response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
