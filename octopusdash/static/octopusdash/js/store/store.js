import objectsReducer from "./objectsSlice.js";

const {createStore} = window.Redux;
const store = createStore(objectsReducer);

document.addEventListener("DOMContentLoaded",()=>{
    window.store = store;
})

export default store