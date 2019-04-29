import React, {Component} from 'react'
import {Tree, Menu, Dropdown, Form, Input, Button, Row, Col, Tooltip} from 'antd';
import '../css/demo.css'

const {TreeNode} = Tree;

function hasErrors(fieldsError) {
    return Object.keys(fieldsError).some(field => fieldsError[field]);
}

class HorizontalLoginForm extends Component {
    componentDidMount() {
        // To disabled submit button at the beginning.
        this.props.form.validateFields();
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
            }
        });
    }

    render() {
        const {
            getFieldDecorator, getFieldsError, getFieldError, isFieldTouched,
        } = this.props.form;

        // Only show error after a field is touched.
        return (
            <Form layout="inline" onSubmit={this.handleSubmit}>
                <Form.Item>
                    {getFieldDecorator('结点名称', {
                        rules: [{required: true, message: '结点名称不可为空!'}],
                    })(
                        <Input prefix="" placeholder="名称"/>
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('备注描述', {
                        rules: [{required: false, message: 'Please input your Password!'}],
                    })(
                        <Input placeholder="描述（可选）"/>
                    )}
                </Form.Item>
                <Form.Item>
                    <Button
                        type="primary"
                        htmlType="submit"
                        disabled={hasErrors(getFieldsError())}
                    >
                        提交
                    </Button>
                </Form.Item>
            </Form>
        );
    }
}


export class Demo extends Component {
    onSelect = (selectedKeys, info) => {
        console.log('selected', selectedKeys, info);
    }

    onCheck = (checkedKeys, info) => {
        console.log('onCheck', checkedKeys, info);
    }

    render() {
        const WrappedHorizontalLoginForm = Form.create({name: 'horizontal_login'})(HorizontalLoginForm);
        const confirm = (
            <Tooltip placement="rightBottom" title={(
                <div>
                    <p>化学：小麦2012040103</p>
                    <Button>确认映射</Button>
                </div>
            )}>
                小麦2012040103
            </Tooltip>
        );
        const confirm1 = (
            <Tooltip placement="rightBottom" title={(
                <div className='tooltip1'>
                    <p className='p1'>当前映射：</p>
                    <p>→ 统一标准：<span className='p2'>蔬菜类_鳞茎葱类_百合</span></p>
                    <p className='p1'>与以下映射存在潜在冲突：</p>
                    <p>化学：<span className='p3'>蔬菜及其制品_新鲜蔬菜_鳞茎蔬菜_大葱</span></p>
                    <p>→ 统一标准：<span className='p2'>蔬菜类_鳞茎葱类_绿叶葱类_葱</span></p>
                    <p className='p1'>是否更改映射为：</p>
                    <p>→ 统一标准：<span className='p2'>蔬菜类_鳞茎葱类_绿叶葱类_葱</span></p>
                    <Button type="primary">是</Button>    <Button type="danger">否</Button>
                </div>
            )}>
                大葱1020601
            </Tooltip>
        );
        const menu = (
            <Menu>
                <Menu.Item key="0">
                    <a href="http://www.alipay.com/">插入结点</a>
                </Menu.Item>
                <Menu.Item key="1">
                    <a href="http://www.taobao.com/">删除结点</a>
                </Menu.Item>
                <Menu.Divider/>
                <Menu.Item key="3">查看映射关系</Menu.Item>
            </Menu>
        );

        const candidates = (
            <Dropdown trigger={['click']} placement="topRight" overlay={
                <Menu>
                    <Menu.Item key="0">
                        <a href="#">谷物→麦类→小麦</a>
                    </Menu.Item>
                    <Menu.Divider/>
                    <Menu.Item key="1">
                        <a href="#">谷物碾磨加工品→研磨粉/面→小麦粉</a>
                    </Menu.Item>
                    <Menu.Divider/>
                    <Menu.Item key="2">
                        <a href="#">谷物粉类制成品→小麦粉制品</a>
                    </Menu.Item>
                    <Menu.Divider/>
                    <Menu.Item key="3">
                        <a href="#">食用淀粉→谷类淀粉→麦淀粉→小麦淀粉</a>
                    </Menu.Item>
                    <Menu.Divider/>
                    <Menu.Item key="4">查看更多</Menu.Item>
                </Menu>
            }>
                <a className="ant-dropdown-link" href="#">
                    小麦2012040103
                </a>
            </Dropdown>
        );
        const dd = (
            <Dropdown overlay={menu} trigger={['click']} placement="topRight">
                <a className="ant-dropdown-link" href="#">
                    麦类F0A01
                </a>
            </Dropdown>)
        ;
        return (
            <Row>
                <Col span={6}>
                    {/*<WrappedHorizontalLoginForm/>*/}
                    {/*<Tree*/}
                    {/*defaultExpandedKeys={['0-0-0', '0-0-1']}*/}
                    {/*onSelect={this.onSelect}*/}
                    {/*>*/}
                    {/*<TreeNode className='GRE' title="谷物20120401" key="0-0">*/}
                    {/*<TreeNode className='GRE' title="稻谷2012040101" key="0-0-0"/>*/}
                    {/*<TreeNode title="玉米2012040102" key="0-0-0-1"/>*/}
                    {/*<TreeNode title={candidates} key="0-0-0-0"/>*/}
                    {/*<TreeNode className='GRE' title="大麦2012040104" key="0-0-1"/>*/}
                    {/*</TreeNode>*/}
                    {/*</Tree>*/}
                    <Tree
                        defaultExpandedKeys={['0-0-0', '0-0-1']}
                        onSelect={this.onSelect}
                    >
                        <TreeNode title="葱蒜类10206" className='GRE' key="0-0">
                            <TreeNode title="葱蒜其他1020600" className='BLA' key="0-0-0"/>
                            <TreeNode title={confirm1} className='BLA' key="0-0-0-1"/>
                            <TreeNode title="洋葱1020602" className='GRE' key="0-0-0-0"/>
                            <TreeNode title="圆葱1020603" className='BLA' key="0-0-1"/>
                        </TreeNode>
                    </Tree>
                </Col>
                <Col span={6}>
                    <Tree
                        defaultExpandedKeys={['0-0-0', '0-0-1']}
                        onSelect={this.onSelect}
                    >
                        <TreeNode title="鳞茎葱类（葱蒜类）F0B05" key="0-0">
                            <TreeNode title="鳞茎葱类F0B0501" key="0-0-0">
                                <TreeNode title="大蒜F0B050101" key="0-0-0-1"/>
                            </TreeNode>
                            <TreeNode title="绿叶葱类F0B0502" key="0-0-1">
                                <TreeNode title="韭菜F0B050201" key="0-0-1-0"/>
                                <TreeNode title="葱F0B050202" key="0-0-1-1"/>
                                <TreeNode title="青蒜F0B050203" key="0-0-1-2"/>
                                <TreeNode title="蒜薹F0B050204" key="0-0-1-3"/>
                                <TreeNode title="韭葱F0B050205" key="0-0-1-4"/>
                                <TreeNode title="蒜苗F0B050206" key="0-0-1-5"/>
                            </TreeNode>
                            <TreeNode title="百合F0B0503" key="0-0-2">
                            </TreeNode>
                        </TreeNode>
                    </Tree>
                    {/*<Tree*/}
                    {/*defaultExpandedKeys={['0-0-0', '0-0-1']}*/}
                    {/*onSelect={this.onSelect}*/}
                    {/*>*/}
                    {/*<TreeNode title="谷物F0A" key="0-0">*/}
                    {/*<TreeNode title="麦类F0A01" key="0-0-0">*/}
                    {/*<TreeNode title={confirm} key="0-0-0-1"/>*/}
                    {/*<TreeNode title="大麦F0A0102" key="0-0-0-0"/>*/}
                    {/*</TreeNode>*/}
                    {/*<TreeNode title="稻类F0A02" key="0-0-1">*/}
                    {/*<TreeNode title="稻谷F0A0201" key="0-0-1-0"/>*/}
                    {/*</TreeNode>*/}
                    {/*</TreeNode>*/}
                    {/*</Tree>*/}
                </Col>
            </Row>
        );
    }
}
