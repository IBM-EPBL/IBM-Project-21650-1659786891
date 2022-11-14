window.watsonAssistantChatOptions = {
    integrationID: "*************************************", // The ID of this integration.
    region: "au-syd", // The region your integration is hosted in.
    serviceInstanceID: "**************************", // The ID of your service instance.
    onLoad: function(instance) {
        instance.render();
    }
};
setTimeout(function() {
    const t = document.createElement('script');
    t.src = "https://web-chat.global.assistant.watson.appdomain.cloud/versions/" + (window.watsonAssistantChatOptions.clientVersion || 'latest') + "/WatsonAssistantChatEntry.js";
    document.head.appendChild(t);
});