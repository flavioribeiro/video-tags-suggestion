(defproject video-dump "1.0.0-SNAPSHOT"
  :description "FIXME: write description"
  :dependencies [[org.clojure/clojure "1.3.0"]
                 [org.apache.lucene/lucene-analyzers "3.5.0"]
                 [clj-http "0.5.6"]
                 [redis.clients/jedis "2.0.0"]]
  :main video-dump.core)