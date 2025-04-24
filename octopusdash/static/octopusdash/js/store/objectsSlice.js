export default function objectsReducer(state = { selected:[] } , action){
    switch(action.type){
        case 'REMOVE_FROM_SELECTED':
            let new_items = state.selected.filter((item) => item === action.payload )
            return {...state,selected:new_items}
        case 'ADD_TO_SELECTED':
            if(!state.selected.find((item) => item === action.payload )){
                let new_objects = state.selected
                new_objects.push(parseInt(action.payload))
                return {...state,selected:new_objects}
            }


            return state
        default:
            return state
    }
}