# レコメンド関連の記事に使用したNotebookリポジトリ

## 構成

- data ... データセットのディレクトリ
- data/MovieLens20M ... MovieLens20Mデータセットのディレクトリ
- data/MovieLens100k ... MovieLens100kデータセットのディレクトリ
- models ... 各手法で試したnotebookのディレクトリ

## データセットについて

今回はMovieLensのデータセットを二値分類のタスクで用いることができるようネガティブサンプリングし、かつ訓練／評価／予測用に分割している。   


1. データセットを取得しそれぞれのdata/ディレクトリへ格納   
それぞれ以下のURLより取得   
MovieLens100k:https://www.kaggle.com/rajmehra03/movielens100k  
MovieLens20M:https://www.kaggle.com/grouplens/movielens-20m-dataset


## 扱っている手法と記事

|手法|ディレクトリ|論文|
|:--|:--|:--|
||TransFM.ipynb|[Translation-based Factorization Machines for Sequential Recommendation](https://cseweb.ucsd.edu/~jmcauley/pdfs/recsys18a.pdf)|
|TransRec.ipynb|[Translation-based Recommendation](https://www.ijcai.org/proceedings/2018/0734.pdf)|
