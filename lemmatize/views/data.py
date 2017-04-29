import abc
# Create your views here.
from typing import List, Tuple

from rest_framework.response import Response
from rest_framework.views import APIView

from lemmatize.data_work import processors
from lemmatize.models import Lemma, LemmaMeet


class ProcessorsView(APIView):
    def get(self, request):
        data = {}
        for processor in processors:
            _id = processor.__name__
            args = [{
                'name': name,
                'word': word,
                'type': _type.__name__
            } for name, word, _type in processor.args]
            data[_id] = {
                'name': processor.name,
                'desc': processor.desc,
                'id': _id,
                'args': args
            }
        return Response(data)


class BaseDataView(APIView, metaclass=abc.ABCMeta):
    fields = {}
    processors_list = tuple()

    def _fill(self, request):
        self.lemma = Lemma.objects.get(name=request.GET.get('word', 'сессия'))
        self.meets = LemmaMeet.objects.filter(lemma=self.lemma).order_by(
            "timestamp")

        self.kwargs = {}

        for field, (tp, default) in self.fields.items():
            val = tp(request.GET.get(field, default))
            self.kwargs[field] = val

    def _get_tss(self) -> List[int]:
        return [meet.timestamp for meet in self.meets]

    def get(self, request):
        self._fill(request)
        timestamps = self._get_tss()

        return Response(self._process(timestamps))

    def _process(self, timestamps: List[int]) -> List[Tuple[int, float]]:
        data = None
        for processor in self.processors_list[::-1]:
            data = processor(data or timestamps, **self.kwargs)

        return data