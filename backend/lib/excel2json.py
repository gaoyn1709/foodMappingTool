import os
import pandas as pd
from backend.lib.config import CONFIG
from backend.lib.tool_function_lib import save_json_file
from backend.lib.all_data import all_data
from backend.lib.basic_class import StandardFoodNode, StandardAttribute, GeneralFoodNode


def dfs(root, func):
    func(root)
    for child in root['children']:
        dfs(child, func)


def generate_standard_foods():
    excel_file = 'backend/data/excelSrc/standardFoods/统一标准_食品_含同义词.xlsx'

    def make_tree_with_synonyms(file_path, ID, NAME, CODE, SYNONYM_NUM, SYNONYM):
        # 统一标准的食品结点转化为树状json
        df = pd.read_excel(file_path)
        df = df.replace(pd.np.nan, '', regex=True)
        cols = list(df.columns)
        start_index = cols.index(SYNONYM)
        i = 0
        root = {'id': 0, 'name': 'root', 'children': [], 'parent_id': -1, 'code': 'F', 'synonym_num': 0, 'synonyms': [],
                'path': []}
        parent_codes = [root['code']]
        nodes = {root['code']: root}
        while i < len(df):
            food_id = df[ID][i].item()
            name = df[NAME][i]
            code: str = df[CODE][i]
            synonym_num = df[SYNONYM_NUM][i].item()
            node = {'id': food_id, 'name': name, 'children': [], 'code': code,
                    'synonym_num': synonym_num, 'synonyms': []}
            for j in range(synonym_num):
                synonym = df[cols[start_index + j]][i]
                if synonym == '':
                    print('error in synonym of id: %d' % food_id)
                node['synonyms'].append(synonym)
            while not code.startswith(parent_codes[-1]):
                parent_codes.pop()
            parent_code = parent_codes[-1]
            parent_node = nodes[parent_code]
            node['parent_id'] = parent_node['id']
            node['path'] = parent_node['path'] + [name]
            nodes[code] = node
            parent_node['children'].append(node)
            parent_codes.append(code)
            i += 1
        return root

    food_tree = make_tree_with_synonyms(excel_file, ID='序号', NAME='一级分类名称', CODE='编码', SYNONYM_NUM='同义词数量',
                                        SYNONYM='同义词')
    json_tree_file = 'backend/data/jsonTreeFromExcel/standardFoodTree.json'
    save_json_file(json_tree_file, food_tree)
    # 根结点单独处理
    root_id = CONFIG.generate_new_id('食品')
    all_data.standard_foods[root_id] = StandardFoodNode(root_id, 'root', '')
    id_dict = {-1: root_id}  # excel中的id到实际系统id的映射

    # 其余结点DFS遍历进行插入操作即可
    def func(node):
        parent_id = id_dict[node['parent_id']]
        new_id = all_data.insert_standard_food(parent_id, node['name'])
        # 更新同义词
        synonym_with_notes = dict()
        for synonym in node['synonyms']:
            synonym_with_notes[synonym] = '百度百科'
        all_data.modify_standard_food_synonyms(new_id, synonym_with_notes)
        id_dict[node['id']] = new_id

    dfs(food_tree, func)


def generate_standard_attributes():
    pass


def generate_general_foods():
    pass


def load_from_excel():
    for file in [CONFIG.id_file, CONFIG.standard_foods_file, CONFIG.standard_foods_file, CONFIG.general_foods_file]:
        try:
            os.remove(file)
        except OSError:
            pass
    generate_standard_foods()
    generate_standard_attributes()
    generate_general_foods()


if __name__ == '__main__':
    load_from_excel()
