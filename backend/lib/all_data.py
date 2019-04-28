import os
from backend.lib.config import CONFIG
from backend.lib.tool_function_lib import load_json_file, save_json_file
from shutil import copy2
import time

from backend.lib.basic_class import GeneralFoodNode, StandardFoodNode, StandardAttribute


# 定义装饰器，实现版本管理功能
def version_control(func):
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
        except Exception as e:
            return str(e)
        # 没有出现异常，为有效操作
        self.operation_num += 1
        if self.operation_num >= self.save_version_interval:
            self.save_as_history()
            self.operation_num = 0
        else:
            self.save_version()
        return result

    return wrapper


class AllData(object):
    def __init__(self):
        # key: id, value: a StandardFoodNode object
        self.standard_foods = self.load_standard_foods()
        # key: id, value: a StandardAttribute object
        self.standard_attributes = self.load_standard_attributes()
        # key: field, value: dict {key :id, value: a GeneralFoodNode object}
        self.general_foods = self.load_general_foods()
        # 每10次有效操作存储一次历史版本
        self.operation_num = 0
        self.save_version_interval = 10

    @staticmethod
    def load_standard_foods():
        json_data = load_json_file(CONFIG.standard_foods_file)
        result = dict()
        for food in json_data:
            obj = StandardFoodNode('', '', '')
            obj.from_json(food)
            result[obj.id] = obj
        return result

    @staticmethod
    def load_general_foods():
        json_data = load_json_file(CONFIG.general_foods_file)
        result = dict()
        for food in json_data:
            obj = GeneralFoodNode('', '', '', '')
            obj.from_json(food)
            result[obj.id] = obj
        return result

    @staticmethod
    def load_standard_attributes():
        json_data = load_json_file(CONFIG.standard_attributes_file)
        result = dict()
        for food in json_data:
            obj = StandardAttribute('', '', '')
            obj.from_json(food)
            result[obj.id] = obj
        return result

    def save_version(self):
        # 每次操作后保存修改
        save_json_file(CONFIG.standard_foods_file, [x.to_json() for x in self.standard_foods.values()])
        save_json_file(CONFIG.standard_attributes_file, [x.to_json() for x in self.standard_attributes.values()])
        save_json_file(CONFIG.general_foods_file, [x.to_json() for x in self.general_foods.values()])

    def save_as_history(self):
        # 保存当前状态，并存为历史版本
        self.save_version()
        now_time = time.strftime('%Y%m%d-%H_%M_%S', time.localtime())
        folder_to_save = os.path.join(CONFIG.history_folder, now_time)
        os.makedirs(folder_to_save, exist_ok=True)
        copy2(CONFIG.standard_foods_file, folder_to_save)
        copy2(CONFIG.standard_attributes_file, folder_to_save)
        copy2(CONFIG.general_foods_file, folder_to_save)
        copy2(CONFIG.id_file, folder_to_save)

        # for example

    @version_control  # 对数据造成修改的操作添加此装饰器以便进行版本管理
    def insert_standard_food(self, parent_id: str, name: str, note: str = ''):
        """
        新增统一标准中的食品结点
        :param parent_id: 其父节点id
        :param name: 食品名称
        :param note: 备注
        :return: 新增结点id if 操作成功 else 错误信息的字符串
        """
        if parent_id not in self.standard_foods:
            # this should not happen without bug
            raise '新增标准食品失败！父节点%s不存在！' % parent_id
        parent_node: StandardFoodNode = self.standard_foods[parent_id]
        if parent_node.use_flag is False:
            return '新增标准食品失败！父节点已被移除，建议刷新页面以查看最新版本'
        # 从全局CONFIG中申请新id
        new_id = CONFIG.generate_new_id(field='食品')
        # 创建新结点
        new_node = StandardFoodNode(node_id=new_id, name=name, parent_id=parent_id, note=note)
        # 父结点的children中加入它的id
        parent_node.add_child(new_id)
        # 加入到standard_foods集合中
        self.standard_foods[new_id] = new_node
        return new_id

    @version_control
    def delete_standard_food(self, food_id: str):
        """
        删除统一标准中的食品结点
        :param food_id: 待删除结点的id
        :return: food_id if 操作成功 else 错误信息的字符串
        """
        if food_id not in self.standard_foods:
            raise Exception('删除标准食品失败！该结点%s不存在' % food_id)
        food_node: StandardFoodNode = self.standard_foods[food_id]
        if food_node.use_flag is False:
            raise Exception('删除标准食品失败！该食品已被移除，建议刷新页面以查看最新版本')
        # 从父结点的children中移除当前结点
        parent_node: StandardFoodNode = self.standard_foods[food_node.parent_id]
        parent_node.remove_child(food_id)

        # 递归设置当前结点及其孩子结点的use_flag，并移除相关映射关系
        def deprecate_food_and_its_children(root_id: str):
            root: StandardFoodNode = self.standard_foods[food_id]
            root.stop_in_use()  # 设置use_flag为False
            # 将该food_id从对应的各领域结点的ontology字段中移除
            for field, entity in root.entity:
                for general_id in entity.keys():
                    general_node: GeneralFoodNode = self.general_foods[field][general_id]
                    general_node.ontology.remove(root_id)
            # 深度优先遍历，移除所有孩子结点
            for child_id in root.children:
                deprecate_food_and_its_children(child_id)

        deprecate_food_and_its_children(food_id)
        return food_id

    @version_control
    def modify_standard_food_info(self, food_id: str, new_name: str, new_note: str):
        """
        修改指定id的标准结点的基本信息信息, name和note
        :param food_id:
        :param new_name:
        :param new_note:
        :return:
        """
        pass

    @version_control
    def modify_standard_food_synonyms(self, food_id: str, new_synonyms: dict):
        """
        修改指定id的标准结点的同义词信息
        :param new_synonyms:
        :return:
        """
        if food_id not in self.standard_foods:
            raise Exception('修改标准食品同义词失败！该结点%s不存在' % food_id)
        food_node: StandardFoodNode = self.standard_foods[food_id]
        if food_node.use_flag is False:
            raise Exception('修改标准食品同义词失败！该食品已被移除，建议刷新页面以查看最新版本')
        food_node.modify_synonyms(new_synonyms)
        return 'success'

    @version_control
    def insert_standard_attribute(self, parent_id: str, name: str, note: str = ''):
        """
        插入新的标准属性
        :param parent_id:
        :param name:
        :param note:
        :return:
        """
        # tips:  用CONFIG.generate_new_id(field='标准属性') 来自动生成新id，参考insert_standard_food
        pass

    @version_control
    def delete_standard_attribute(self, attribute_id: str):
        """
        删除指定的标准属性，参考delete_standard_food, 注意一定要弄清self.standard_foods的entity字段长什么样
        :param attribute_id:
        :return:
        """
        pass

    @version_control
    def add_mapping(self, field: str, general_id: str, standard_id: str, attribute_ids: list):
        """
        为某个领域的结点与统一标准的结点增加映射关系
        :param field: 领域名称
        :param general_id: 领域结点id
        :param standard_id: 统一标准id
        :param attribute_ids: 附加属性的id
        :return: 'success' if 操作成功 else 错误信息
        """
        if field not in self.general_foods:
            raise Exception('新增映射关系失败！领域名称“%s”错误!' % field)
        general_node: GeneralFoodNode = self.general_foods[field].get([general_id], None)
        if general_node is None:
            raise Exception('新增映射关系失败！领域“%s”中没有id为%s的结点！' % (field, general_node))
        standard_node: StandardFoodNode = self.standard_foods.get(standard_id, None)
        if standard_node is None:
            raise Exception('新增映射关系失败！统一标准中没有id为%s的结点' % standard_id)
        if general_node.use_flag is False or standard_node.use_flag is False:
            raise Exception('新增映射关系失败！映射结点已被删除，建议刷新页面以查看最新版本')
        if standard_id not in general_node.ontology:
            general_node.add_ontology(standard_id)
        standard_node.add_entity(field=field, general_id=general_id, attribute_ids=attribute_ids)
        return 'success'

    @version_control
    def delete_mapping(self, field: str, general_id: str):
        """
        删除某个结点到统一标准的映射
        :param field:
        :param general_id:
        :return:
        """
        pass

    def recoding(self):
        """
        根据当前的总体标准，按照以往的规则，为self.standard_nodes和self.standard_attributes设置编码
        :return:
        """
        pass

    def conflict_detect(self, field: str):
        """
        查找指定领域中映射存在冲突的结点
        :param field: 指定的领域
        :return: dict of {node_id:{conflict_field: conflict_id}}
        """
        pass


all_data = AllData()  # singleton


def test():
    # you can write your own test codes here for test purpose
    # test for insert_standard_foods
    root_id = CONFIG.generate_new_id('食品')
    all_data.standard_foods[root_id] = StandardFoodNode(root_id, 'root', '')
    all_data.insert_standard_food('食品0', 'food1')
    all_data.insert_standard_food('食品0', 'food2')
    all_data.insert_standard_food('食品1', 'food3')
    all_data.insert_standard_food('食品1', 'food4')
    all_data.insert_standard_food('食品3', 'food5')
    all_data.insert_standard_food('食品0', 'food6')
    all_data.insert_standard_food('食品0', 'food7')
    all_data.insert_standard_food('食品1', 'food8')
    all_data.insert_standard_food('食品1', 'food9')
    all_data.insert_standard_food('食品3', 'food10')


if __name__ == '__main__':
    test()
