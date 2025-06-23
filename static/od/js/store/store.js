import selectedInstancesReducer from "./selectedInstancesReducer.js";

const store = Redux.createStore(selectedInstancesReducer)
window.store = store;
