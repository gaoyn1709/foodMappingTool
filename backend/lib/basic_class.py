class BasicNode(object):
    def __init__(self, node_id: str, name: str, parent_id: str, code: str = '', children=None, use_flag: bool = True,
                 note: str = ''):
        self.id = node_id
        self.name = name
        self.parent_id = parent_id
        self.code = code
        self.use_flag = use_flag
        self.note = note
        if children is None:
            children = []
        self.children = children

    def modify_info(self, new_name: str, new_note: str):
        self.name = new_name
        self.note = new_note

    def remove_child(self, child_id):
        self.children.remove(child_id)

    def add_child(self, child_id):
        if child_id not in self.children:
            self.children.append(child_id)

    def change_parent(self, new_parent_id):
        self.parent_id = new_parent_id

    def stop_in_use(self):
        self.use_flag = False

    def set_code(self, new_code: str):
        self.code = new_code

    def to_json(self):
        return self.__dict__

    def from_json(self, json_data):
        for key, value in json_data.items():
            self.__setattr__(key, value)


class GeneralFoodNode(BasicNode):
    def __init__(self, node_id: str, name: str, parent_id: str, field: str, code: str = '', children=None,
                 ontology=None, use_flag: bool = True, note: str = ''):
        super(GeneralFoodNode, self).__init__(node_id, name, parent_id, code, children, use_flag, note)
        self.field = field
        if ontology is None:
            ontology = []
        self.ontology = ontology

    def remove_ontology(self, standard_id):
        if standard_id in self.ontology:
            self.ontology.remove(standard_id)

    def add_ontology(self, standard_id):
        if standard_id not in self.ontology:
            self.ontology.append(standard_id)


class StandardFoodNode(BasicNode):
    def __init__(self, node_id: str, name: str, parent_id: str, code: str = '', children=None, use_flag: bool = True,
                 note: str = '', synonyms=None, entity=None):
        super(StandardFoodNode, self).__init__(node_id, name, parent_id, code, children, use_flag, note)
        if synonyms is None:
            synonyms = dict()
        self.synonyms = synonyms
        if entity is None:
            entity = dict()
        self.entity = entity

    def modify_synonyms(self, new_synonyms):
        self.synonyms = new_synonyms

    def add_entity(self, field: str, general_id: str, attribute_ids: list):
        if field not in self.entity:
            self.entity[field] = dict()
        self.entity[field][general_id] = attribute_ids


class StandardAttribute(BasicNode):
    def __init__(self, attribute_id: str, name: str, parent_id: str, code: str = '', children=None,
                 use_flag: bool = True,
                 note: str = ''):
        super(StandardAttribute, self).__init__(attribute_id, name, parent_id, code, children, use_flag, note)
