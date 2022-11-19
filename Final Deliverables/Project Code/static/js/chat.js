window.watsonAssistantChatOptions = {
    integrationID: "ca3dcf01-ad9f-4090-a5df-37124b9c6ff4", // The ID of this integration.
    region: "au-syd", // The region your integration is hosted in.
    serviceInstanceID: "8081617a-79f9-485b-be7c-defb8066a79f", // The ID of your service instance.
    onLoad: function(instance) {
        instance.render();
    }
};
setTimeout(function() {
    const t = document.createElement('script');
    t.src = "https://web-chat.global.assistant.watson.appdomain.cloud/versions/" + (window.watsonAssistantChatOptions.clientVersion || 'latest') + "/WatsonAssistantChatEntry.js";
    document.head.appendChild(t);
});