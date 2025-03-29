// Select all inputs with the 'data-tooltip' attribute for tooltips
document.querySelectorAll("[data-tooltip]").forEach(input => {
    tippy(input, {
        content: input.getAttribute("data-tooltip"),  // Get tooltip text
        placement: 'bottom',  // Position tooltip to the right
        animation: 'fade',  // Fade effect
        theme: 'light',  // Light theme
        delay: [100, 50],  // Small delay for better UX
        arrow:true,
    });
});