import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .elasticsearch_client import ElasticsearchClient


def dashboard(request):

    if "elasticsearch" not in request.session:
        return redirect("connect")

    context = {}

    return render(request, "dashboard.html", context)


def connect_to_elasticsearch(request):
    if request.method == "POST":
        host = request.POST.get("host")
        username = request.POST.get("username")
        password = request.POST.get("password")

        request.session["elasticsearch"] = {
            "host": host,
            "username": username,
            "password": password,
        }

        from elasticsearch import Elasticsearch

        try:

            if username and password:
                authentication = (username, password)
            else:
                authentication = None

            es = Elasticsearch(
                hosts=[host],
                http_auth=authentication,
            )
            if es.ping():
                return redirect("dashboard")
            else:
                messages.error(request, "Failed to connect to Elasticsearch.")
        except Exception as e:
            print(e)
            messages.error(request, f"Erro: {e}")

    return render(request, "connect.html")


def get_dashboard_data(request):
    try:
        response = {}
        es_client = ElasticsearchClient(request.session)
        cluster_stats = es_client.get_cluster_stats()
        cluster_health = es_client.get_cluster_health()
        cluster_settings = es_client.get_cluster_settings()

        active_replica_shards = cluster_health.get(
            "active_shards"
        ) - cluster_health.get("active_primary_shards")

        disk_available_percent = cluster_stats.get("nodes").get("fs").get(
            "free_in_bytes"
        ) / cluster_stats.get("nodes").get("fs").get("total_in_bytes")
        disk_usage_percent = 100 * (1 - disk_available_percent)

        heap_usage_percent = 100 * (
            cluster_stats.get("nodes").get("jvm").get("mem").get("heap_used_in_bytes")
            / cluster_stats.get("nodes").get("jvm").get("mem").get("heap_max_in_bytes")
        )

        cluster_health.update({"active_replica_shards": active_replica_shards})

        cluster_stats.update(
            {
                "disk_usage_percent": disk_usage_percent,
                "heap_usage_percent": heap_usage_percent,
            }
        )

        cluster_health = json.dumps(cluster_health.body)
        cluster_stats = json.dumps(cluster_stats.body)
        cluster_settings = json.dumps(cluster_settings.body)

        response.update(
            {
                "cluster_health": json.loads(cluster_health),
                "cluster_stats": json.loads(cluster_stats),
                "cluster_settings": json.loads(cluster_settings),
            }
        )

        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
