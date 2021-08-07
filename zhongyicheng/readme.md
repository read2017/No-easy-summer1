# 文件说明

- `fuzzyQuery`为调用elasticsearch的python模块，详情见`README.md`
- `scripts`文件夹下为数据导入相关脚本，其中`multiprocess_import.py`为导入脚本，`process_thread_cmp.py`为多进程、多线程对比benchmark脚本，`test.py`为查询测试脚本。\
- `container`文件夹下为容器相关脚本，其中`es-ik`下为elasticsearch-ik容器构建及运行脚本，`docker-compose.yml`为elasticsearch+logstash服务编排文件。

# 数据导入

目前只支持了全量导入，自动同步待添加。

## 并行处理

elasticsearch默认开启线程池，自动根据CPU核数调优，无需干预。

由于Python计算效率较低，且elasticsearch采用web api通信，单线程处理效率非常低。经测试速率约为40w条/90min，全量导入需60h，因此添加并行优化。

## 多线程vs多进程

小规模数据测试发现多线程CPU占用率只有100%+，多进程可以把全部核心用起来。估测是因为代码中有一个全局计数器变量，多线程调用时需加解锁。而多进程存在的问题即是由于python解释器被fork到其他进程中，计数器成为子进程的全局变量，最后结果未汇总到主进程中。

## TODO

- 支持自动同步数据库
- 改用elastic工具栈中的logstash
- ~~优化索引准确率~~

# 容器运行

*假设目前处在container文件夹*

- 首先需要`docker build es-ik/.`构建elasticsearch-ik容器
- elasticsearch-ik单容器直接使用`es-ik/docker-compose.yml`即可，或手动运行`docker run --rm -it -p port1:9200 -p port2:9300 -v [$PWD/es-ik/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml] -v data-export-dir-absolute:/usr/share/elasticsearch/data elasticsearch-ik`
- es+logstash组合运行`docker-compose up`调用container下的docker-compose.yml即可
- logstash还未配置好