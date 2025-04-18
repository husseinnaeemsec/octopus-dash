// Select all inputs with the 'data-tooltip' attribute for tooltips
document.querySelectorAll("[data-tooltip]").forEach(input => {
    const config = {
        content: input.getAttribute("data-tooltip"),  // Get tooltip text
        placement: 'bottom',  // Position tooltip to the right
        animation: 'fade',  // Fade effect
        theme: 'light',  // Light theme
        delay: [100, 50],  // Small delay for better UX
        arrow:true,
        interactive:input.dataset['interactive'] === 'true',
        // trigger:input.dataset['trigger'] | null
    }

    tippy(input,config);
});

document.addEventListener("DOMContentLoaded",function(){
    if(window.Alert){
        document.querySelectorAll(".to-clipboard").forEach((ele)=>{
            ele.addEventListener("click",function(e){
                let text = e.target.dataset['value']
                copyToClipboard(text);
            })
        })
    }
})

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        new window.Alert("success",null,"Copied to clipboard!")
    }).catch(err => {
        new window.Alert("error",null,"Copyed to Clipboard")
    });
}