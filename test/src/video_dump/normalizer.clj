(ns video-dump.normalizer
  (:import  [java.io StringReader]
            [org.apache.lucene.analysis.tokenattributes CharTermAttribute]
            [org.apache.lucene.analysis.br BrazilianAnalyzer]
            [org.apache.lucene.util Version]))

(def analyzer (BrazilianAnalyzer. Version/LUCENE_30))

(defn normalize-str
  "Normalizes string str."
  [str]
  (let [stream (.tokenStream analyzer "str" (StringReader. str))]
    (loop [tokens []]
      (if-not (.incrementToken stream)
        (set tokens)
        (recur (conj tokens
                     (.term (.getAttribute stream CharTermAttribute))))))))