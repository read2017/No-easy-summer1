import { PageContainer } from '@ant-design/pro-layout'
import { Input,Button } from 'antd'
import { Row, Col,Card,Tabs,Space } from 'antd'
import G6 from '@antv/g6'
import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom'
import styles from './index.less'
import TabPane from '@ant-design/pro-card/lib/components/TabPane'


const parseGraphData=()=>{
    const nodeParser=(node)=>{
        const ico={'E':'','P':''}
        const palette={'E':'#steelblue','P':'#fa8c16'}
        return {
            id: node.id,
            label: node.name,
            icon: {
                show: true,
                width: 24,
                height: 24,
                img: ico[node.category]
            },
            style: {
                fill: palette[node.category],
                stroke: palette[node.category],
                lineWidth:3,
            }
        }
    }
    const edgeParser=(edge)=>{
        return {
            id: edge.id,
            source: node.source,
            target: node.target,
            label: node.label
        }
    }
}

const MultiQuery = () => {
    const ref = React.useRef(null)
    let graph = null
    let container = null

    useEffect(() => {
    if(!graph) {
        container=ref.current
        const width = container.scrollWidth;
        const height = container.scrollHeight || 500;
        graph = new G6.Graph({
        container: ref.current,
        width,
        height,
        modes: {
            default: ['drag-canvas','zoom-canvas','drag-node','click-select']
        },
        layout: {
            type: 'force',
            nodeStrength: -100,
            //direction: 'LR'
        },
        defaultNode: {
            shape: 'node',
            size: 30,
            labelCfg: {
            style: {
                fill: '#000000A6',
                fontSize: 10
            }
            },
            style: {
            stroke: '#72CC4A',
            width: 150
            }
        },nodeStateStyles: {
            selected: {
                opacity: 0.8
            }
        },
        defaultEdge: {
            shape: 'polyline'
        }
        })
    }
    fetch('https://gw.alipayobjects.com/os/antvdemo/assets/data/relations.json')
    .then((res) => res.json())
    .then((data) => {
        graph.data({
        nodes: data.nodes.map(function(node,i){
            const palette={'h':'#steelblue','e':'#fa8c16',undefined:'#ff7875'}
            node.style={
                fill: palette[node.entityType],
                stroke: '#ffccc7'
            }
            return node;
        }),
        edges: data.edges.map(function (edge, i) {
            edge.id = 'edge' + i;
            return Object.assign({}, edge);
        }),
    });
    graph.render()
    const refreshDragedNodePosition=(e)=>{
        const model = e.item.get('model');
        model.fx = e.x;
        model.fy = e.y;
    }
    graph.on('node:dragstart', function (e) {
        graph.layout();
        refreshDragedNodePosition(e);
    });
    graph.on('node:drag', function (e) {
        const forceLayout = graph.get('layoutController').layoutMethods[0];
        forceLayout.execute();
        refreshDragedNodePosition(e);
    });
    graph.on('node:dragend', function (e) {
        e.item.get('model').fx = null;
        e.item.get('model').fy = null;
    });
});
    }, [])

    if (typeof window !== 'undefined')
      window.onresize = () => {
        if (!graph || graph.get('destroyed')) return;
        if (!container || !container.scrollWidth || !container.scrollHeight) return;
        console.log(container.scrollWidth, container.scrollHeight);
        graph.changeSize(container.scrollWidth, container.scrollHeight);
      };
    return (
        <PageContainer
  content={[
    /*<Row gutter={8  }>
        <Col offset={7} span={10}>
            <Button type="link">查实体</Button>
            <Button type="link">查路径</Button>
            <Button type="link">查资本系</Button>
        </Col>
  </Row>,*/
    <Row gutter={8}>
        <Col span={12} offset={6}>
            <Tabs type="line">
                <TabPane tab="查实体" key="1">
                    <Row gutter={8}>
                        <Col span={20}>
                            <Input></Input>
                        </Col>
                        <Col span={4}>
                        <Button type="primary">
                            搜索
                        </Button>
                        </Col>
                    </Row>
                </TabPane>
                <TabPane tab="查路径" key="2">
                    <Row gutter={8}>
                        <Col span={10}>
                            <Input placeholder="企业A"></Input>
                        </Col>
                        <Col span={10}>
                            <Input placeholder="企业B"></Input>
                        </Col>
                        <Col span={4}>
                        <Button type="primary">
                            搜索
                        </Button>
                        </Col>
                    </Row>
                </TabPane>
                <TabPane tab="查资本系" key="3">
                    <Row gutter={8}>
                        <Col span={20}>
                            <Input></Input>
                        </Col>
                        <Col span={4}>
                        <Button type="primary">
                            搜索
                        </Button>
                        </Col>
                    </Row>
                </TabPane>
            </Tabs>
        </Col>
        {/* <Col span={1}>
            <Button type="primary">
                搜索
            </Button>
        </Col> */}
    </Row>
  ]}
>
    <Card>
        <div id="mainGraph" className={styles.mainGraph} ref={ref}></div>
    </Card>
</PageContainer>
    )
}

export default MultiQuery