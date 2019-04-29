import React, {Component} from 'react';
import {Tree, Input} from 'antd';

const {TreeNode} = Tree;
const Search = Input.Search;

// const x = 3;
// const y = 2;
// const z = 1;
// const transformData = (data) => {
//     const key = data.id.toString();
//     const parentKey = (data.parent_id||0).toString();
//     const code = data.code;
//     const title = data.name;
//     const root = {key: key, title: title, code: code, parentKey: parentKey, children: []};
//     for (let i = 0; i < data.children.length; i++) {
//         root.children[i] = transformData(data.children[i]);
//     }
//     return root;
// };
// const gData = [transformData(chemicalData)];
// console.log(gData);
// const dataList = [];
// const generateList = (data) => {
//     for (let i = 0; i < data.length; i++) {
//         const node = data[i];
//         dataList.push({key: node.key, title: node.title, code: node.code, parentKey: node.parentKey});
//         if (node.children) {
//             generateList(node.children);
//         }
//     }
// };
// generateList(gData);
class SearchTree extends Component {
    transformData(data) {
        const key = data.id.toString();
        const parentKey = (data.parent_id || 0).toString();
        const code = data.code;
        const title = data.name;
        const root = {key: key, title: title, code: code, parentKey: parentKey, children: []};
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
            this.dataList.push({key: node.key, title: node.title, code: node.code, parentKey: node.parentKey});
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
            if (item.title.indexOf(value) > -1) {
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

    render() {
        // console.log('render!');
        // const gData = [this.transformData(this.props.inputData)];
        // this.generateList(gData);
        // if (this.props.searchText !== '')
        //     this.getExpandedKeys(this.props.searchText);
        const {searchValue, expandedKeys, autoExpandParent} = this.state;
        const loop = data => data.map((item) => {
            const index = item.title.indexOf(searchValue);
            const beforeStr = item.title.substr(0, index);
            const afterStr = item.title.substr(index + searchValue.length);
            const title = index > -1 ? (
                <span>
                    {beforeStr}
                    <span style={{color: '#f50'}}>{searchValue}</span>
                    {afterStr}
                </span>
            ) : <span>{item.title}</span>;
            if (item.children) {
                return (
                    <TreeNode blockNode={false} key={item.key} title={title}>
                        {loop(item.children)}
                    </TreeNode>
                );
            }
            return <TreeNode blockNode={false} key={item.key} title={title}/>;
        });
        // console.log(this.state);
        return (
            <div>
                <Search className={'subSearchBar'} style={{marginBottom: 8}} placeholder="在此领域搜索"
                        onChange={this.onChange}/>
                <Tree
                    blockNode={false}
                    onExpand={this.onExpand}
                    expandedKeys={expandedKeys}
                    autoExpandParent={autoExpandParent}
                >
                    {loop(this.gData)}
                </Tree>
            </div>
        );
    }
}

SearchTree.defaultProps = {
    inputData: {id: 0, name: 'root', children: []},
    searchText: ''
};

export default SearchTree;