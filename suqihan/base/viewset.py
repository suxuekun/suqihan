from django.http.response import HttpResponse
from django.db.models.aggregates import Sum
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .. import utils
from ..base.permission import IsAuthenticatedReadOnly

BASE_PERMISSION_CLASSES = [IsAuthenticatedReadOnly]


class BaseViewSet(GenericViewSet):
    xsl_config =[];
    xsl_optimize = [];
    query_optimize_related = []
    query_limit_filter = {};
    
    def get_queryset(self):
        query_set = super(BaseViewSet,self).get_queryset();
        related_query_set = query_set.select_related(*self.query_optimize_related);
        filtered_query_set = related_query_set.filter(**self.query_limit_filter);
        return filtered_query_set
    
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def exist(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        selfid = request.query_params.get('id!');
        if selfid:
            count = queryset.exclude(id=selfid).exists()
        else:   
            count = queryset.exists()
        return HttpResponse(count);
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def count(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count();
        return HttpResponse(count);
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def distinct(self,request,*args,**kwargs):
        distinct_field = request.query_params['field']
        queryset = self.filter_queryset(self.get_queryset()).values_list(distinct_field).distinct();
        mid_result = list(queryset);
        result = [];
        for item in mid_result:
            result.append(item[0])
        return HttpResponse(utils.toJSON(result))
    
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def xslOptions(self,request,*args,**kwargs):
        return HttpResponse(utils.toJSON(self.xsl_config))
    
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def xsl(self,request,*args,**kwargs):
        require_fields = request.query_params.get('fields')
        if require_fields:
            fields_list = require_fields.split(",");
            print fields_list;
            fields = [f for f in self.xsl_config if f.get('value') in fields_list]
        else:
            fields = self.xsl_config;
#         fields_meta = self.get_serializer_class().Meta.model._meta.get_fields();
        queryset = self.filter_queryset(self.get_queryset()).select_related(*self.xsl_optimize)
#         fields = [{'header':f.name,'name':f.name} for f in fields_meta if (f.get_internal_type() != "ForeignKey" and f.get_internal_type() != "OneToOneField")];
        model = self.get_serializer_class().Meta.model
        name = model._meta.db_table
        if len(fields):
            return utils.csvUtil.wb_download(utils.csvUtil.export_xls(queryset, fields),name);
        else:
            return utils.csvUtil.wb_download(utils.csvUtil.export_model_xls(queryset,model),name);
    
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def fields(self,request,*args,**kwargs):
        fields = self.get_serializer_class().Meta.model._meta.get_fields();
        result = [f.name for f in fields];
        return HttpResponse(utils.toJSON(result))
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def field_info(self,request,*args,**kwargs):
        fields = self.get_serializer_class().Meta.model._meta.get_fields();
        result = [{f.name:f.get_internal_type()} for f in fields];
        return HttpResponse(utils.toJSON(result))
    
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def sum(self,request,*args,**kwargs):
        sum_field = request.query_params['field']
        queryset = self.filter_queryset(self.get_queryset()).aggregate(total=Sum(sum_field, field=sum_field))

        result = queryset;
        return HttpResponse(utils.toJSON(result))
    
    @list_route(methods=['get'], permission_classes=BASE_PERMISSION_CLASSES)
    def user_related(self,request,*args,**kwargs):
        user = request.user;
        link = request.query_params.get('link') or None;
        if link:
            key = link+"__user";
            query_kwargs = {
                key:user
            }
            queryset = self.filter_queryset(self.get_queryset().filter(**query_kwargs))
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(user=user))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)