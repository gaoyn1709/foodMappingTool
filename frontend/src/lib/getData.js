import generalFoods from '../testData/general_foods'
import standardFoods from '../testData/standard_foods'
import standardAttributes from '../testData/standard_attributes'

export function getStandardFoods() {
    return standardFoods;
}

export function getStandardAttributes() {
    return standardAttributes;
}

export function getFieldFoods(field) {
    if (!(field in generalFoods))
        return [];
    return generalFoods[field];
}

export function getStandardFoodTree() {

}

export function getFieldFoodTree() {

}

export function getStandardAttributeTree() {

}