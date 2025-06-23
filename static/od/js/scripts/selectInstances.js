document.addEventListener("DOMContentLoaded", () => {
    const toggleSelectAllInstances = document.getElementById("checkbox-toggle-all");
    const instanceCheckBoxs = Array.from(document.querySelectorAll(".instance-checkbox"));
    const ids = instanceCheckBoxs.map(ele => parseInt(ele.dataset.id));

    instanceCheckBoxs.forEach(cb => cb.checked = false);
    toggleSelectAllInstances.checked = false;

    function updateMasterCheckbox() {
        const allChecked = instanceCheckBoxs.every(cb => cb.checked);
        toggleSelectAllInstances.checked = allChecked;
    }

    toggleSelectAllInstances.addEventListener("click", (e) => {
        const checked = e.target.checked;
        instanceCheckBoxs.forEach(cb => cb.checked = checked);
        if (checked) {
            window.store.dispatch({ type: "SET", payload: ids });
        } else {
            window.store.dispatch({ type: "DESELECT_ALL" });
        }
    });

    instanceCheckBoxs.forEach(cb => {
        cb.addEventListener("click", (e) => {
            const id = parseInt(cb.dataset.id);
            if (e.target.checked) {
                window.store.dispatch({ type: "ADD", payload: id });
            } else {
                window.store.dispatch({ type: "REMOVE", payload: id });
            }
            updateMasterCheckbox();
        });
    });

});
