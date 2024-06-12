# Useful links
* https://pastebin.com/viqqJEZS
* https://httpie.io/



# Commands for copy and paste
Hins: copy only the command, not the response.

## Check cluster state

```
curl 127.0.0.1:9200/_cluster/health\?pretty=true
```
Output:
```
{
  "cluster_name" : "es_cluster",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 3,
  "number_of_data_nodes" : 3,
  "active_primary_shards" : 1,
  "active_shards" : 2,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
```
## Create an index with configured mapping
```
curl -XPUT 127.0.0.1:9200/movies -d '
{
"mappings": {
"properties" : {
"year" : {"type": "date"}
}}}' -H 'Content-Type: application/json'
```
Output:
```
{"acknowledged":true,"shards_acknowledged":true,"index":"movies"}
```
## insert one document

```
curl –XPUT 127.0.0.1:9200/movies/_doc/109487 -d '
{
"genre" : ["IMAX","Sci-Fi"], "title" : "Interstellar", "year" : 2014
}' -H 'Content-Type: application/json'
```
Output:
```
{"_index":"movies","_type":"_doc","_id":"109487","_version":1,"result":"created","_shards":{"total":2,"successful":2,"failed":0},"_seq_no":0,"_primary_term":1}
```
## insert many documents

```
curl -XPUT 127.0.0.1:9200/_bulk -d '
{ "create" : { "_index" : "movies", "_id" : "135569" } }
{ "id": "135569", "title" : "Star Trek Beyond", "year":2016 , "genre":["Action", "Adventure", "Sci-Fi"] }
{ "create" : { "_index" : "movies", "_id" : "122886" } }
{ "id": "122886", "title" : "Star Wars: Episode VII - The Force Awakens", "year":2015 , "genre":["Action", "Adventure", "Fantasy", "Sci-Fi", "IMAX"] }
{ "create" : { "_index" : "movies", "_id" : "109487" } }
{ "id": "109487", "title" : "Interstellar", "year":2014 , "genre":["Sci-Fi", "IMAX"] }
{ "create" : { "_index" : "movies", "_id" : "58559" } }
{ "id": "58559", "title" : "Dark Knight, The", "year":2008 , "genre":["Action", "Crime", "Drama", "IMAX"] }
{ "create" : { "_index" : "movies", "_id" : "1924" } }
{ "id": "1924", "title" : "Plan 9 from Outer Space", "year":1959 , "genre":["Horror", "Sci-Fi"] }
' -H 'Content-Type: application/json'
```
Output:
```
{"took":75,"errors":true,"items":[{"create":{"_index":"movies","_type":"_doc","_id":"135569","_version":1,"result":"created","_shards":{"total":2,"successful":2,"failed":0},"_seq_no":1,"_primary_term":1,"status":201}},{"create":{"_index":"movies","_type":"_doc","_id":"122886","_version":1,"result":"created","_shards":{"total":2,"successful":2,"failed":0},"_seq_no":2,"_primary_term":1,"status":201}},{"create":{"_index":"movies","_type":"_doc","_id":"109487","status":409,"error":{"type":"version_conflict_engine_exception","reason":"[109487]: version conflict, document already exists (current version [1])","index_uuid":"6Px8ALoVRASJqEHUEmZBBg","shard":"0","index":"movies"}}},{"create":{"_index":"movies","_type":"_doc","_id":"58559","_version":1,"result":"created","_shards":{"total":2,"successful":2,"failed":0},"_seq_no":3,"_primary_term":1,"status":201}},{"create":{"_index":"movies","_type":"_doc","_id":"1924","_version":1,"result":"created","_shards":{"total":2,"successful":2,"failed":0},"_seq_no":4,"_primary_term":1,"status":201}}]}
```
The error results from the duplicated document **109487**.

## Partial update API
```
curl -XPOST 127.0.0.1:9200/movies/_doc/109487/_update -d '
{
    "doc": {
        "title": "InterStellar"
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{"_index":"movies","_type":"_doc","_id":"109487","_version":2,"result":"updated","_shards":{"total":2,"successful":2,"failed":0},"_seq_no":8,"_primary_term":1}
```

## Delete a document
```
curl -XDELETE 127.0.0.1:9200/movies/_doc/58559\?pretty
```
Output:
```
{
  "_index" : "movies",
  "_type" : "_doc",
  "_id" : "58559",
  "_version" : 3,
  "result" : "not_found",
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "failed" : 0
  },
  "_seq_no" : 11,
  "_primary_term" : 1
}
```

## Search documents
The command bellow searches documents with the term **trek** on the field **title**
```
curl 127.0.0.1:9200/movies/_search\?q=title:trek\&pretty

```
Output:
```
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.6739764,
    "hits" : [
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "135569",
        "_score" : 1.6739764,
        "_source" : {
          "id" : "135569",
          "title" : "Star Trek Beyond",
          "year" : 2016,
          "genre" : [
            "Action",
            "Adventure",
            "Sci-Fi"
          ]
        }
      }
    ]
  }
}
```
## search using request body
```
curl -XGET 127.0.0.1:9200/movies/_search\?pretty -d '
{
    "query": {
        "match": {
            "title": "star"
        }
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "took" : 9,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.1631508,
    "hits" : [
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "135569",
        "_score" : 1.1631508,
        "_source" : {
          "id" : "135569",
          "title" : "Star Trek Beyond",
          "year" : 2016,
          "genre" : [
            "Action",
            "Adventure",
            "Sci-Fi"
          ]
        }
      },
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "122886",
        "_score" : 0.752627,
        "_source" : {
          "id" : "122886",
          "title" : "Star Wars: Episode VII - The Force Awakens",
          "year" : 2015,
          "genre" : [
            "Action",
            "Adventure",
            "Fantasy",
            "Sci-Fi",
            "IMAX"
          ]
        }
      }
    ]
  }
}
```
## boolean query with a filter
```
curl -XGET 127.0.0.1:9200/movies/_search\?pretty -d'
{
    "query":{
        "bool": {
            "must": {"term": {"title": "trek"}},
            "filter": {"range": {"year": {"gte": 2010}}}
        }
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.6739764,
    "hits" : [
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "135569",
        "_score" : 1.6739764,
        "_source" : {
          "id" : "135569",
          "title" : "Star Trek Beyond",
          "year" : 2016,
          "genre" : [
            "Action",
            "Adventure",
            "Sci-Fi"
          ]
        }
      }
    ]
  }
}
```
## phrase matching
```
curl -XGET 127.0.0.1:9200/movies/_search\?pretty -d '
{
    "query": {
        "match_phrase": {
            "title": "star wars"
        }
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.8357882,
    "hits" : [
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "122886",
        "_score" : 1.8357882,
        "_source" : {
          "id" : "122886",
          "title" : "Star Wars: Episode VII - The Force Awakens",
          "year" : 2015,
          "genre" : [
            "Action",
            "Adventure",
            "Fantasy",
            "Sci-Fi",
            "IMAX"
          ]
        }
      }
    ]
  }
}
```
## slop
```
curl -XGET 127.0.0.1:9200/movies/_search\?pretty -d '
{
    "query": {
        "match_phrase": {
            "title": {"query": "star beyond", "slop": 1}
        }
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "took" : 6,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.8357882,
    "hits" : [
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "135569",
        "_score" : 1.8357882,
        "_source" : {
          "id" : "135569",
          "title" : "Star Trek Beyond",
          "year" : 2016,
          "genre" : [
            "Action",
            "Adventure",
            "Sci-Fi"
          ]
        }
      }
    ]
  }
}
```
## slop as priority
```
curl -XGET 127.0.0.1:9200/movies/_search\?pretty -d '
{
    "query": {
        "match_phrase": {
            "title": {"query": "star beyond", "slop": 100}
        }
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.8357882,
    "hits" : [
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "135569",
        "_score" : 1.8357882,
        "_source" : {
          "id" : "135569",
          "title" : "Star Trek Beyond",
          "year" : 2016,
          "genre" : [
            "Action",
            "Adventure",
            "Sci-Fi"
          ]
        }
      }
    ]
  }
}
```
## pagination
```
curl -XGET 127.0.0.1:9200/movies/_search\?pretty -d'
{
    "from": 2,
    "size": 2,
    "query": {"match": {"genre": "Sci-Fi"}}
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "took" : 6,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4,
      "relation" : "eq"
    },
    "max_score" : 0.45073897,
    "hits" : [
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "135569",
        "_score" : 0.40260923,
        "_source" : {
          "id" : "135569",
          "title" : "Star Trek Beyond",
          "year" : 2016,
          "genre" : [
            "Action",
            "Adventure",
            "Sci-Fi"
          ]
        }
      },
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "122886",
        "_score" : 0.33175898,
        "_source" : {
          "id" : "122886",
          "title" : "Star Wars: Episode VII - The Force Awakens",
          "year" : 2015,
          "genre" : [
            "Action",
            "Adventure",
            "Fantasy",
            "Sci-Fi",
            "IMAX"
          ]
        }
      }
    ]
  }
}
```

## using the fuzziness parameter
```
curl -XGET 127.0.0.1:9200/movies/_search\?pretty -d '
{
    "query": {
        "fuzzy": {
            "title": {"value": "intrsteller", "fuzziness": 2}
        }
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "took" : 23,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.3085446,
    "hits" : [
      {
        "_index" : "movies",
        "_type" : "_doc",
        "_id" : "109487",
        "_score" : 1.3085446,
        "_source" : {
          "genre" : [
            "IMAX",
            "Sci-Fi"
          ],
          "title" : "InterStellar",
          "year" : 2014
        }
      }
    ]
  }
}
```

## indexing n-grams
```
curl -XPUT 127.0.0.1:9200/movies\?pretty -d '
{
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram", "min_gram": 1,
                    "max_gram": 20
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom", "tokenizer": "standard", "filter": [
                        "lowercase", "autocomplete_filter"
                    ]
                }
            }
        }
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "movies"
}
```
## map your field with it
```
curl -XPUT 127.0.0.1:9200/movies/_mapping\?pretty -d '
{
    "properties" : {
        "title": {
            "type" : "text",
            "analyzer": "autocomplete"
        }
    }
}' -H 'Content-Type: application/json'
```
Output:
```
{
  "acknowledged" : true
}
```


