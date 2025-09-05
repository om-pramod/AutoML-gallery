document.addEventListener('DOMContentLoaded', () => {
    const slideContainer = document.getElementById('slide-container');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const slideCounter = document.getElementById('slide-counter');

    // Configure highlight.js to look for Python
    hljs.configure({ languages: ['python'] });

    let currentSlideIndex = 0;

    function renderSlide() {
        const slide = slides[currentSlideIndex];
        let pointsHtml = '<ul>';
        slide.points.forEach(point => {
            const formattedPoint = point.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            pointsHtml += `<li>${formattedPoint}</li>`;
        });
        pointsHtml += '</ul>';

        let codeHtml = '';
        if (slide.code) {
            const escapedCode = slide.code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            codeHtml = `<pre><code class="language-python">${escapedCode.trim()}</code></pre>`;
        }

        const slideHtml = `
            <h2>${slide.title}</h2>
            ${pointsHtml}
            ${codeHtml}
        `;

        slideContainer.classList.add('fade-out');

        setTimeout(() => {
            slideContainer.innerHTML = slideHtml;

            const codeBlock = slideContainer.querySelector('pre code');
            if (codeBlock) {
                hljs.highlightElement(codeBlock);
            }

            slideContainer.classList.remove('fade-out');
        }, 300);
    }

    function updateNavigation() {
        slideCounter.textContent = `Slide ${currentSlideIndex + 1} / ${slides.length}`;
        prevBtn.disabled = currentSlideIndex === 0;
        nextBtn.disabled = currentSlideIndex === slides.length - 1;
    }

    nextBtn.addEventListener('click', () => {
        if (currentSlideIndex < slides.length - 1) {
            currentSlideIndex++;
            renderSlide();
            updateNavigation();
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentSlideIndex > 0) {
            currentSlideIndex--;
            renderSlide();
            updateNavigation();
        }
    });

    // Initial render
    renderSlide();
    updateNavigation();
});
