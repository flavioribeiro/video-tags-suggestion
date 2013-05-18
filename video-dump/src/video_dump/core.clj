(ns video-dump.core
  (:use [video-dump.normalizer])
  (:require [clj-http.client :as client])
  (:import [redis.clients.jedis Jedis])
  (:gen-class))

(def redis (Jedis. "localhost"))

(defn get-videos
  ""
  [params]
  (:body (client/get "http://api.video.globoi.com/videos.json"
                     {:as :json
                      :query-params (assoc params :access_token "api")})))

(defn- persist-term-data
  ""
  [term tags]
  (let [key (str "term:" term)]
    (try
      (doall (map #(do
                     (.hincrBy redis key % 1)
                     (.incr redis (str key ":count")))
                  tags))
      (catch Exception e
        (println e)))))

(defn persist-video-data
  ""
  [video-json]
  (let [terms (normalize-str
               (str (:title video-json) " " (:description video-json)))
        tags (:tags video-json)]
    (doall (map #(persist-term-data % tags) terms))))

(defn -main [& args]
  (let [[per-page total-pages] args]
    (if (string? per-page)
      (println (apply str (interpose " " (normalize-str per-page))))
      (map #(doall (map persist-video-data
                        (get-videos {:page (inc %) :per_page per-page})))
           (range (Integer. total-pages))))))
