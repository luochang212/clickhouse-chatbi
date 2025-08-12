# 启动 clickhouse 容器

参考：https://mp.weixin.qq.com/s/MO0l_bQ2ET_FnerLrFtUEA

## 1. 下载 clickhouse 镜像

```bash
docker pull clickhouse/clickhouse-server
```

## 2. 启动 clickhouse 容器

```bash
docker run -d \
  --name clickhouse-dev \
  -p 18123:8123 \
  -p 19000:9000 \
  -v $(pwd)/ch_data:/var/lib/clickhouse/ \
  -v $(pwd)/ch_logs:/var/log/clickhouse-server/ \
  -e CLICKHOUSE_USER=admin \
  -e CLICKHOUSE_PASSWORD=[YOUR_CK_PASSWORD] \
  --ulimit nofile=262144:262144 \
  --cap-add=SYS_NICE \
  --cap-add=IPC_LOCK \
  clickhouse/clickhouse-server
```

## 3. 检查服务是否启动

1）检查容器日志

```bash
docker logs clickhouse-dev
```

2）检查连通性，正常情况输出：Ok.

```bash
curl -u admin:[YOUR_CK_PASSWORD] "http://localhost:18123/"
```

3）检查数据库版本

```bash
curl -u admin:[YOUR_CK_PASSWORD] "http://localhost:18123/?query=SELECT%20version()"
```

## 4. 登录 ClickHouse 客户端

```bash
docker exec -it clickhouse-dev \
    clickhouse-client \
    --user admin \
    --password [YOUR_CK_PASSWORD]
```

## 5. 下载数据

1）从 [Kaggle](https://www.kaggle.com/datasets/tanishksharma9905/top-popular-anime) 下载 Top Popular Anime 数据集 popular_anime.csv
2）将 popular_anime.csv 文件复制到容器挂载的数据卷 ch_data 上

```bash
cp /path/to/popular_anime.csv ./ch_data/user_files/
```

## 6. 建库建表

```sql
-- 创建库
CREATE DATABASE IF NOT EXISTS entertainment;

-- 创建表
CREATE TABLE IF NOT EXISTS entertainment.anime_info (
  id UInt32 COMMENT '动画唯一标识ID',
  name String COMMENT '动画名称',
  genres String COMMENT '动画类型',
type String COMMENT '播出形式',
  episodes Float32 COMMENT '集数',
  status String COMMENT '播出状态',
  aired_from DateTime COMMENT '开始播出时间',
  aired_to DateTime COMMENT '结束播出时间',
  duration_per_ep String COMMENT '单集时长',
  score Float32 COMMENT '评分',
  scored_by Float64 COMMENT '评分人数',
  `rank` Float32 COMMENT '排名',
  rating String COMMENT '年龄分级',
  studios String COMMENT '制作工作室',
  producers String COMMENT '出品方',
  image String COMMENT '封面图片URL',
  trailer String COMMENT '预告片URL',
  synopsis String COMMENT '剧情简介'
)
ENGINE = MergeTree()
ORDER BY (`id`)
COMMENT '动画信息数据表';
```

## 7. 将 CSV 数据导入 ClickHouse 数据库

```sql
-- 将 csv 文件导入 clickhouse
INSERT INTO entertainment.anime_info
SELECT 
  id,
  name,
  genres,
type,
  episodes,
  status,
  toDateTime(replaceRegexpAll(aired_from, 'T|\\+.*', ' ')) AS aired_from,
  toDateTime(replaceRegexpAll(aired_to, 'T|\\+.*', ' ')) AS aired_to,
  duration_per_ep,
  score,
  scored_by,
  `rank`,
  rating,
  studios,
  producers,
  image,
  trailer,
  synopsis
FROM file('popular_anime.csv', 'CSVWithNames');

-- 检查导入是否成功
SELECT * FROM entertainment.anime_info LIMIT 2;

-- 看一下行数
SELECT count(*) FROM entertainment.anime_info;
```
