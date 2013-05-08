#! /bin/sh

curl http://localhost:8080/solr/test3/update --data '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'  
curl http://localhost:8080/solr/test3/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'

