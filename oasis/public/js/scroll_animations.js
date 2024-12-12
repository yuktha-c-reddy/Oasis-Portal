document.addEventListener('DOMContentLoaded', () => {

    gsap.registerPlugin(ScrollTrigger);
    gsap.utils.toArray(".fade-in").forEach((section) => {
        gsap.from(section, {
            opacity: 0,
            y: 50, 
            duration: 0.8,
            ease: "power2.out",
            scrollTrigger: {
            trigger: section,
            start: "top 80%", 
            toggleActions: "play none none reverse", 
            },
        });
    });
})
