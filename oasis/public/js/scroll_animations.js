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



    // gsap.registerPlugin(ScrollTrigger);

    // const sections = document.querySelectorAll(".section");

    // sections.forEach((section) => {
    //     gsap.fromTo(
    //       section,
    //       {
    //         opacity: 0.9,
    //         y: 0, 
    //         scale: 1,
    //       },
    //       {
    //         opacity: 1,
    //         y: 0,
    //         scale: 1,
    //         ease: 'power2.out',
    //         duration: 0.6, 
    //         scrollTrigger: {
    //           trigger: section,
    //           start: 'top 100%', 
    //           end: 'top 20%',
    //           scrub: true,
    //           toggleActions: 'play none none none',
    //         }
    //       }
    //     );
    // });

    // const toolItems = document.querySelectorAll('.tool-item');

    // toolItems.forEach(item => {
    //     item.addEventListener('mouseenter', () => {
    //         gsap.to(item, {
    //             rotationY: 180,
    //             scale: 1.2,
    //             duration: 0.6,
    //             ease: "back.out(1.7)"
    //         });
    //     });

    //     item.addEventListener('mouseleave', () => {
    //         gsap.to(item, {
    //             rotationY: 0,
    //             scale: 1,
    //             duration: 0.6,
    //             ease: "power2.inOut"
    //         });
    //     });
    // });
})
