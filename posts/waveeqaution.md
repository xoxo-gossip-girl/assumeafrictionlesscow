# The Wave Equation: A Quick Guide
### By Maramureş

<div class="presentation-wrapper">
    <div id="slide-viewer">
        <img src="static/slides/slide1.png" class="slide active" id="slide0">
        <img src="static/slides/slide2.png" class="slide" id="slide1">
        <img src="static/slides/slide3.png" class="slide" id="slide2">
    </div>

<div class="slide-controls">
        <button onclick="moveSlide(-1)">Previous</button>
        <button onclick="moveSlide(1)">Next</button>
</div>
</div>

<script>
    let index = 0;
    const slides = document.querySelectorAll('.slide');

    function moveSlide(step) {
        slides[index].classList.remove('active');
        index = (index + step + slides.length) % slides.length;
        slides[index].classList.add('active');
    }
</script>