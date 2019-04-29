import React, {Component} from 'react'
import {Row, Col, Input} from 'antd'
import SearchTree from './searchTree'
import chemicalData from '../json/化学污染物食品分类.json'
import biologyData from '../json/微生物食品分类.json'
import explorData from '../json/暴发食品分类.json'
import '../css/searchForest.css'


class SearchForest extends Component {
    onChange = (e) => {
        const value = e.target.value;
        const searchBars = document.getElementsByClassName('subSearchBar');
        for (let i = 0; i < searchBars.length; i++) {
            let inputBar = searchBars[i].getElementsByTagName('input')[0];
            // inputBar.value = value;
            let nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            nativeInputValueSetter.call(inputBar, value);
            let ev2 = new Event('input', {bubbles: true});
            inputBar.dispatchEvent(ev2);
        }
    };

    render() {
        const Search = Input.Search;
        return (
            <div>
                <Row type='flex' justify='center'>
                    <Col span={12}>
                        <header>
                            <h1>协同搜索</h1>
                            <Search style={{marginBottom: 8}} placeholder="在三个领域同时搜索" onChange={this.onChange}/>
                        </header>
                    </Col>
                </Row>
                <Row type='flex' justify='center' align='top' gutter={48}>
                    <Col span={8}>
                        <header><h2>化学污染物食品分类</h2></header>
                        <SearchTree inputData={chemicalData}/>
                    </Col>
                    <Col span={8}>
                        <header><h2>微生物食品分类</h2></header>
                        <SearchTree inputData={explorData}/>
                    </Col>
                    <Col span={8}>
                        <header><h2>暴发食品分类</h2></header>
                        <SearchTree inputData={biologyData}/>
                    </Col>
                </Row>
            </div>
        )
    }
}

export default SearchForest;