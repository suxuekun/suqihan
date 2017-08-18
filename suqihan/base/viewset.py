from django.db.models.aggregates import Sum
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .. import utils


class BaseViewSet(ModelViewSet):
    xsl_config =[];
    permission_classes_by_action = {}
    
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return super(BaseViewSet,self).get_permissions()
        
    @list_route(methods=['get'])
    def exist(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        selfid = request.query_params.get('id!');
        if selfid:
            count = queryset.exclude(id=selfid).exists()
        else:   
            count = queryset.exists()
        return Response(count);
    @list_route(methods=['get'])
    def count(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count();
        return Response(count);
    @list_route(methods=['get'])
    def distinct(self,request,*args,**kwargs):
        distinct_field = request.query_params['field']
        queryset = self.filter_queryset(self.get_queryset()).values_list(distinct_field).distinct();
        mid_result = list(queryset);
        result = [];
        for item in mid_result:
            result.append(item[0])
        return Response(result)
    
    @list_route(methods=['get'])
    def xslOptions(self,request,*args,**kwargs):
        return Response(self.xsl_config)
    
    @list_route(methods=['get'])
    def xsl(self,request,*args,**kwargs):
        require_fields = request.query_params.get('fields')
        if require_fields:
            fields_list = require_fields.split(",");
            fields = [f for f in self.xsl_config if f.get('value') in fields_list]
        else:
            fields = self.xsl_config;
        queryset = self.filter_queryset(self.get_queryset())
        model = self.get_serializer_class().Meta.model
        name = model._meta.db_table
        if len(fields):
            return utils.csvUtil.wb_download(utils.csvUtil.export_xls(queryset, fields),name);
        else:
            return utils.csvUtil.wb_download(utils.csvUtil.export_model_xls(queryset,model),name);
    
    @list_route(methods=['get'])
    def fields(self,request,*args,**kwargs):
        fields = self.get_serializer_class().Meta.model._meta.get_fields();
        result = [f.name for f in fields];
        return Response(result)
    @list_route(methods=['get'])
    def field_info(self,request,*args,**kwargs):
        fields = self.get_serializer_class().Meta.model._meta.get_fields();
        result = [{f.name:f.get_internal_type()} for f in fields];
        return Response(result)
    
    @list_route(methods=['get'])
    def sum(self,request,*args,**kwargs):
        sum_field = request.query_params['field']
        queryset = self.filter_queryset(self.get_queryset()).aggregate(total=Sum(sum_field, field=sum_field))

        result = queryset;
        return Response(result)
    
    @list_route(methods=['get'])
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