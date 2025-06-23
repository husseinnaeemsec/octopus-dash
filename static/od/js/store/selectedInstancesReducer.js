const initialState = {
    selected: [],
    select_all:false
};

export default function selectedInstancesReducer(state = initialState, action) {
    const payload = action.payload;
    switch (action.type) {

        case 'SET':
            return { selected: payload , select_all:false};
        
        case "SELECT_ALL":
            return { select_all:true , selected:[] }

        case 'DESELECT_ALL':
            return { selected: [] , select_all:false};

        case 'ADD':
            if (!state.selected.includes(payload)) {
                return { selected: [...state.selected, payload] , select_all:false };
            }
            return state;

        case 'REMOVE':
            return {
                selected: state.selected.filter(item => item !== payload),
                select_all:false
            };

        default:
            return state;
    }
}
