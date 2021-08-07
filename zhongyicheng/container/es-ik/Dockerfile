#基础镜像使用elasticsearch:2.3.4;因为后面需要es-jdbc进行数据同步，而其只支持到2.3.4.也可以#选择官方推荐的logstash-jdbc-input 其使用Ruby语言实现
FROM elasticsearch:7.14.0
#作者
MAINTAINER zyc <rubbishzhyic@whu.edu.cn>

ENV VERSION 7.14.0
#安装扩展插件 注意其版本对应
#RUN elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v${IK_VERSION}/elasticsearch-analysis-ik-${IK_VERSION}.zip 
ADD http://github.com/medcl/elasticsearch-analysis-ik/releases/download/v${VERSION}/elasticsearch-analysis-ik-$VERSION.zip /tmp/
#ADD elasticsearch-analysis-ik-$VERSION.zip /tmp/
RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install -b file:///tmp/elasticsearch-analysis-ik-$VERSION.zip
RUN rm /tmp/*.zip
