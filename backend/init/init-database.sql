-- ClickHouse 数据库初始化脚本

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

-- -- 检查导入是否成功
-- SELECT '数据导入完成，总行数：' as message, count(*) as total_rows FROM entertainment.anime_info;

-- -- 显示前2行数据
-- SELECT '前2行数据预览：' as message;
-- SELECT * FROM entertainment.anime_info LIMIT 2;