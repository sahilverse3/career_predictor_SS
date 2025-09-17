// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Advanced Particle Canvas Animation ---
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    class Particle {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            this.radius = Math.random() * 2 + 0.5;
            this.color = `rgba(135, 206, 235, ${Math.random() * 0.5 + 0.1})`; // Light blue color
            this.velocity = {
                x: (Math.random() - 0.5) * 0.2,
                y: (Math.random() - 0.5) * 0.2
            };
            this.opacity = 0; // Starts invisible
            this.alpha = Math.random() * 0.8 + 0.2; // Final opacity
            this.fadeSpeed = Math.random() * 0.02 + 0.01; // Fade-in speed
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = this.radius * 2;
            ctx.shadowColor = this.color;
            ctx.globalAlpha = this.opacity;
            ctx.fill();
            ctx.closePath();
        }

        update() {
            if (this.opacity < this.alpha) {
                this.opacity += this.fadeSpeed;
            }

            this.x += this.velocity.x;
            this.y += this.velocity.y;

            // Bounce off edges
            if (this.x + this.radius > canvas.width || this.x - this.radius < 0) {
                this.velocity.x = -this.velocity.x;
            }
            if (this.y + this.radius > canvas.height || this.y - this.radius < 0) {
                this.velocity.y = -this.velocity.y;
            }
        }
    }

    function initParticles() {
        particles = [];
        for (let i = 0; i < 150; i++) {
            particles.push(new Particle(Math.random() * canvas.width, Math.random() * canvas.height));
        }
    }

    function animateParticles() {
        requestAnimationFrame(animateParticles);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => p.update() & p.draw());
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    initParticles();
    animateParticles();

    // --- Interactive Ripple Effect on all form elements ---
    const interactiveElements = document.querySelectorAll('.form-control, .submit-btn');
    interactiveElements.forEach(element => {
        element.style.position = 'relative';
        element.style.overflow = 'hidden';

        element.addEventListener('click', function(e) {
            let x = e.clientX - element.getBoundingClientRect().left;
            let y = e.clientY - element.getBoundingClientRect().top;
            
            let ripple = document.createElement('span');
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            element.appendChild(ripple);
            
            ripple.classList.add('ripple');
            
            setTimeout(() => {
                ripple.remove();
            }, 800);
        });
    });

    // --- Entrance Animations on page load ---
    const animatedElements = document.querySelectorAll('.form-section, .submit-btn, .result-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0'; // Hide initially
    });

    function showElements() {
        animatedElements.forEach((el, index) => {
            setTimeout(() => {
                el.style.animation = `fadeInUp 0.8s forwards`;
                el.style.opacity = '1';
            }, index * 200); // Stagger the animation
        });
    }

    // Delay showing elements until the page is fully ready
    setTimeout(showElements, 100); 
});