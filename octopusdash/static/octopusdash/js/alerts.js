
class Alert{

    alertsCount = 0;

    constructor(type,appendTo=null,message='',timeout=1000){
        this.message = message
        this.type = type
        this.container = document.createElement("div")
        this.container.classList =  'fixed max-w-[500px] left-0 right-0 mx-auto top-10' + ' w-full flex items-center  rounded p-3 border  justify-between ' + this.getStyle().containerClassList
        this.container.id = `alert-${this.alertsCount}`
        this.container.appendChild(this.getMessageContainer())
        this.container.appendChild(this.getCloseButton());
        document.body.appendChild(this.container);
        setTimeout(() => {
            this.container.remove()
        }, timeout);
        this.alertsCount +=1
    }

    getCloseButton(){
        this.button = document.createElement("button")
        let container = this.container
        this.button.classList = 'alert-button w-6 h-6 flex items-center justify-center text-xs rounded-full border ' + this.getStyle().buttonClassList
        this.button.dataset['container'] = this.container.id;
        this.button.innerHTML = '<i class="fa-solid fa-xmark"></i>';
        this.button.addEventListener("click",function(){
            container.remove();
        })

        return this.button
    }

    getMessageContainer(){
        this.messageContainer = document.createElement("div");
        this.messageContainer.classList = "flex basis-11/12 gap-2 items-center "
        let iconwrapper = document.createElement("div");
        iconwrapper.classList = 'w-10 h-10 rounded-lg flex items-center justify-center ' + this.getStyle().iconWrapperClassList
        iconwrapper.innerHTML = this.getStyle().icon;
        let message = document.createElement("p");
        message.classList = 'text-sm ' + this.getStyle().messageClassList;
        message.textContent = this.message
        this.messageContainer.appendChild(iconwrapper);
        this.messageContainer.appendChild(message)

        return this.messageContainer;
        
    }   

    getStyle(){
        switch (this.type) {
            case "success":
                return {
                    containerClassList: "bg-green-100 border-green-300",
                    iconWrapperClassList: "bg-green-300",
                    icon: "<i class='fa-solid fa-check-circle text-green-700'></i>",
                    messageClassList: "text-green-700",
                    buttonClassList: "border-green-300 text-green-500",
                };
            case "info":
                return {
                    containerClassList: "bg-blue-100 border-blue-300",
                    iconWrapperClassList: "bg-blue-300",
                    icon: "<i class='fa-solid fa-info-circle text-blue-700'></i>",
                    messageClassList: "text-blue-700",
                    buttonClassList: "border-blue-300 text-blue-500",
                };
            case "warning":
                return {
                    containerClassList: "bg-yellow-100 border-yellow-300",
                    iconWrapperClassList: "bg-yellow-300",
                    icon: "<i class='fa-solid fa-exclamation-triangle text-yellow-700'></i>",
                    messageClassList: "text-yellow-700",
                    buttonClassList: "border-yellow-300 text-yellow-500",
                };
            case "error":
                return {
                    containerClassList: "bg-rose-100 border-rose-300",
                    iconWrapperClassList: "bg-rose-300",
                    icon: "<i class='fa-solid fa-triangle-exclamation text-rose-700'></i>",
                    messageClassList: "text-rose-700",
                    buttonClassList: "border-rose-300 text-rose-500",
                };
            default:
                return {
                    containerClassList: "bg-gray-100 border-gray-300",
                    iconWrapperClassList: "bg-gray-300",
                    icon: "<i class='fa-solid fa-info-circle text-gray-700'></i>",
                    messageClassList: "text-gray-700",
                    buttonClassList: "border-gray-300 text-gray-500",
                };
        }

        
    }
}

document.querySelectorAll(".alert-button").forEach((button)=>{
    let container = document.getElementById(button.dataset['container'])

    button.addEventListener("click",function(){
        container.remove()
    })
    
})

window.Alert = Alert