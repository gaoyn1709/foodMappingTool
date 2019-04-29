import React, {Component} from 'react';
import {Tree, Input, Col, Popover, Row} from 'antd';
import OldFoodData from '../json/贵科院_食品_同义词'
// import NewFoodData from '../json/新标准_食品_同义词'
import chemData from '../json/chem.tmp'
import '../css/searchSynonym.css'

const {TreeNode} = Tree;
const Search = Input.Search;


class SearchTree extends Component {
    transformData(data) {
        const key = data.id.toString();
        const parentKey = (data.parent_id || 0).toString();
        const code = data.code;
        const title = data.name;
        const path = data.path.join('→');
        const synonyms = data.synonyms;
        const root = {
            key: key,
            title: title,
            code: code,
            parentKey: parentKey,
            children: [],
            synonyms: synonyms,
            path: path
        };

        for (let i = 0; i < data.children.length; i++) {
            root.children[i] = this.transformData(data.children[i]);
        }
        return root;
    };


    dataList = [];
    gData;

    generateList(data) {
        for (let i = 0; i < data.length; i++) {
            const node = data[i];
            this.dataList.push({
                key: node.key,
                title: node.title,
                code: node.code,
                parentKey: node.parentKey,
                synonyms: node.synonyms,
                path: node.path
            });
            if (node.children) {
                this.generateList(node.children);
            }
        }
    };


    onExpand = (expandedKeys) => {
        this.setState({
            expandedKeys,
            autoExpandParent: false,
        });
    };

    containQueryValue(item, value) {
        return item.title.indexOf(value) > -1 || item.synonyms.join('|').indexOf(value) > -1;
    }

    onChange = (e) => {
        const value = e.target.value;
        if (value === '') {
            this.setState({
                expandedKeys: [],
                searchValue: value,
                autoExpandParent: true
            });
            return;
        }
        const expandedKeys = this.dataList.map((item) => {
            if (this.containQueryValue(item, value)) {
                return item.parentKey;
            }
            return null;
        }).filter((item, i, self) => item && self.indexOf(item) === i);
        this.setState({
            expandedKeys,
            searchValue: value,
            autoExpandParent: true,
        });
    };

    constructor(props) {
        super(props);
        this.state = {
            expandedKeys: [],
            searchValue: '',
            autoExpandParent: true,
        };
        this.gData = [this.transformData(this.props.inputData)];
        this.generateList(this.gData);
    }

    detailContent = (item, searchValue) => {
        let synonyms = item.synonyms.join('|');
        const index = synonyms.indexOf(searchValue);
        const beforeStr = synonyms.substr(0, index);
        const afterStr = synonyms.substr(index + searchValue.length);
        synonyms = index > -1 ? (
            <span>
                    {beforeStr}
                <span style={{color: '#f50'}}>{searchValue}</span>
                {afterStr}
                </span>
        ) : <span>{synonyms || '无'}</span>;
        return (
            <div>
                <p>别称：{synonyms}</p>
                <p>编码：{item.code}</p>
                <p>路径：{item.path}</p>
            </div>
        )
    }
    treeNodeTitleWithPopover = ((item, title, searchValue) => {
        return (
            <Popover placement='right' title={item.title} content={this.detailContent(item, searchValue)}>
                {title}
            </Popover>
        );
    });

    render() {
        // console.log('render!');
        // const gData = [this.transformData(this.props.inputData)];
        // this.generateList(gData);
        // if (this.props.searchText !== '')
        //     this.getExpandedKeys(this.props.searchText);
        const {searchValue, expandedKeys, autoExpandParent} = this.state;
        const loop = data => data.map((item) => {
            const index_origin = item.title.indexOf(searchValue);
            const index_synonym = item.synonyms.join('|').indexOf(searchValue);
            let title = <span>{item.title}</span>;
            if (index_origin > -1) {
                const beforeStr = item.title.substr(0, index_origin);
                const afterStr = item.title.substr(index_origin + searchValue.length);
                title = (
                    <span>
                        {beforeStr}
                        <span className='nameSearched'>{searchValue}</span>
                        {afterStr}
                    </span>
                );
            } else if (index_synonym > -1) {
                title = (
                    <span className='synonymSearched'>{item.title}</span>
                )
            }
            if (item.children) {
                return (
                    <TreeNode blockNode={false} key={item.key}
                              title={this.treeNodeTitleWithPopover(item, title, searchValue)}>
                        {loop(item.children)}
                    </TreeNode>
                );
            }
            return <TreeNode blockNode={false} key={item.key} title={this.treeNodeTitleWithPopover(item, title)}/>;
        });
        // console.log(this.state);
        return (
            <div>
                <Row type='flex' justify={'center'}>
                    <Search className='searchBar' placeholder="输入关键词搜索" onChange={this.onChange}/>
                </Row>
                <Row type='flex' justify={'center'}>
                    <Col span={6}>
                        <Tree
                            className='tree'
                            blockNode={false}
                            onExpand={this.onExpand}
                            expandedKeys={expandedKeys}
                            autoExpandParent={autoExpandParent}
                        >
                            {loop(this.gData)}
                        </Tree>
                    </Col>
                </Row>
            </div>
        );
    }
}

SearchTree.defaultProps = {
    inputData: {id: 0, name: 'root', children: []},
    searchText: ''
};

class SearchSynonym extends Component {
    render() {
        return (
            <Row type='flex' justify='center'>
                <Col span={12} className='searchTree 6u'>
                    <header><h1>化学标准</h1></header>
                    <SearchTree inputData={chemData}/>
                </Col>
                <Col span={12} className='searchTree 6u'>
                    <header><h1>统一标准</h1></header>
                    <SearchTree inputData={OldFoodData}/>
                </Col>
            </Row>
        )
    }
}

export default SearchSynonym;