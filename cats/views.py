from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from cats.models import Cat, Owner
from cats.serializers import CatSerializer, OwnerSerializer, CatListSerializer


# Собираем вьюсет, который будет уметь изменять или удалять отдельный объект.
# А ничего больше он уметь не будет.
class UpdateDeleteViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    pass


# Опишем собственный базовый класс вьюсета: он будет создавать экземпляр
# объекта и получать экземпляр объекта
class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    # В теле класса никакой код не нужен! Пустячок, а приятно.
    pass


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    # Пишем метод, а в декораторе разрешим работу со списком объектов
    # и переопределим URL на более презентабельный
    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        # Нужны только последние пять котиков белого цвета
        cats = Cat.objects.filter(color='White')[:5]
        # Передадим queryset cats сериализатору 
        # и разрешим работу со списком объектов
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        # Если запрошенное действие (action) — получение списка объектов
        # ('list')
        if self.action == 'list':
            # ...то применяем CatListSerializer
            return CatListSerializer
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return CatSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class LightCatViewSet(CreateRetrieveViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

# В тех случаях, когда нужно получить больше контроля и возможностей что-то
# «подкрутить» во вьюсетах, можно наследоваться от базового класса ViewSet
# Например, в приложении нужно создать вьюсет, который будет получать
# сериализованный объект одного котика (методом retrieve()) и полный список
# всех котиков (методом list())
# class CatViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Cat.objects.all()
#         serializer = CatSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Cat.objects.all()
#         cat = get_object_or_404(queryset, pk=pk)
#         serializer = CatSerializer(cat)
#         return Response(serializer.data) 
