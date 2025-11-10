from rest_framework import viewsets
from .models import Orden
from .serializers import OrdenSerializer
from core.mixins import OptimizedQuerysetMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from django.conf import settings
from django.core.cache import cache
from tueste.models import Tueste
from molienda.models import Molienda
from ordenes_trilla.models import OrdenTrilla
from ordenes_seleccion_verde.models import OrdenSeleccionVerde
from .serializers import OrdenDetailSerializer
from typing import List, Dict, Any


class OrdenViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Orden.objects.all().order_by('-fecha_inicio_orden')
    serializer_class = OrdenSerializer
    select_related_fields = ['cliente', 'estado_orden']

    # ----------------- Helper interno reutilizable -----------------
    def _serialize_detalle(self, orden: Orden) -> Dict[str, Any]:
        """Serializa una orden con relaciones + KPIs (limitando últimos 20 registros por relación)."""
        base_data = OrdenDetailSerializer(orden).data

        def _sum(items, field):
            return round(sum(filter(None, (i.get(field) for i in items))), 2)

        def _avg(items, field):
            vals = list(filter(None, (i.get(field) for i in items)))
            return round(sum(vals) / len(vals), 2) if vals else 0

        tuestes = base_data.get('tuestes', [])
        moliendas = base_data.get('moliendas', [])
        trillas = base_data.get('trillas', [])
        selv = base_data.get('seleccion_verde', [])

        kpis = {
            'rendimiento_prom_tueste': _avg(tuestes, 'rendimiento'),
            'rendimiento_prom_trilla': _avg(trillas, 'rendimiento'),
            'peso_total_tueste_tostado': _sum(tuestes, 'peso_cafe_tostado') if tuestes else 0,
            'peso_total_molienda': _sum(moliendas, 'peso_moler'),
            'peso_total_trilla_bruto': _sum(trillas, 'peso_cafe_bruto'),
            'peso_total_trilla_verde': _sum(trillas, 'peso_cafe_verde'),
            'peso_total_seleccion_aceptado': _sum(selv, 'peso_aceptado'),
            'conteo_tuestes': len(tuestes),
            'conteo_moliendas': len(moliendas),
            'conteo_trillas': len(trillas),
            'conteo_seleccion_verde': len(selv),
        }
        base_data['kpis'] = kpis
        return base_data

    def _prefetch_detalle_queryset(self, base_qs):
        """Aplica los prefetch estandarizados de detalle a un queryset base."""
        return base_qs.select_related('cliente', 'estado_orden').prefetch_related(
            Prefetch('tueste_set', queryset=Tueste.objects.order_by('-fecha_ingreso')[:20]),
            Prefetch('molienda_set', queryset=Molienda.objects.order_by('-fecha')[:20]),
            Prefetch('ordentrilla_set', queryset=OrdenTrilla.objects.order_by('-fecha_ingreso')[:20]),
            Prefetch('ordenseleccionverde_set', queryset=OrdenSeleccionVerde.objects.order_by('-fecha_ingreso')[:20]),
        )

    @action(detail=True, methods=['get'])
    def detalle(self, request, pk=None):
        force_refresh = request.query_params.get('refresh') == '1'
        cache_key = f"orden_detalle:{pk}"
        if not force_refresh:
            cached = cache.get(cache_key)
            if cached is not None:
                return Response(cached)
        base_qs = self._prefetch_detalle_queryset(Orden.objects.filter(pk=pk))
        orden = base_qs.first()
        if not orden:
            return Response({'detail': 'No encontrado'}, status=404)
        data = self._serialize_detalle(orden)
        cache.set(cache_key, data, getattr(settings, 'ORDER_DETALLE_CACHE_SECONDS', 30))
        return Response(data)

    @action(detail=False, methods=['get'], url_path='detalle-bulk')
    def detalle_bulk(self, request):
        """Devuelve múltiples órdenes con mismo payload del detalle individual.

        Query Params:
          ids=1,2,3 (obligatorio, máximo 50)
          refresh=1 para forzar regeneración (omite cache)
        """
        ids_param = request.query_params.get('ids')
        if not ids_param:
            return Response({'detail': 'Parámetro ids requerido (ids=1,2,3)'}, status=400)
        try:
            raw_ids = [s.strip() for s in ids_param.split(',') if s.strip()]
            ids: List[int] = [int(x) for x in raw_ids]
        except ValueError:
            return Response({'detail': 'Formato ids inválido, usar números separados por coma'}, status=400)
        if not ids:
            return Response({'detail': 'Lista de ids vacía'}, status=400)
        if len(ids) > 50:
            return Response({'detail': 'Máximo 50 ids por solicitud'}, status=400)

        force_refresh = request.query_params.get('refresh') == '1'
        ttl = getattr(settings, 'ORDER_DETALLE_CACHE_SECONDS', 30)

        resultados: Dict[int, Dict[str, Any]] = {}
        missing_ids: List[int] = []
        if not force_refresh:
            for oid in ids:
                cached = cache.get(f"orden_detalle:{oid}")
                if cached is not None:
                    resultados[oid] = cached
                else:
                    missing_ids.append(oid)
        else:
            missing_ids = ids[:]

        if missing_ids:
            qs = self._prefetch_detalle_queryset(Orden.objects.filter(pk__in=missing_ids))
            orden_map = {o.pk: o for o in qs}
            for oid in missing_ids:
                orden = orden_map.get(oid)
                if not orden:
                    continue  # se omite id inexistente
                data = self._serialize_detalle(orden)
                resultados[oid] = data
                cache.set(f"orden_detalle:{oid}", data, ttl)

        # Mantener orden de entrada y marcar faltantes
        response_list = []
        for oid in ids:
            payload = resultados.get(oid)
            if payload is None:
                response_list.append({'id': oid, 'detail': 'No encontrado'})
            else:
                response_list.append(payload)

        return Response({'count': len(response_list), 'results': response_list})