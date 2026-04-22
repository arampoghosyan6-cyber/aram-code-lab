function scrollAppear() {
    var aboutText = document.querySelector('.about-text');
    var aboutPosition = aboutText.getBoundingClientRect().top;
    var screenPosition = window.innerHeight / 1.3;

    if(aboutPosition < screenPosition) {
        aboutText.classList.add('about-text-appear');
    }
}

window.addEventListener('scroll',scrollAppear);



/* function smoothScroll(target, duration) {
  var target = document.querySelector(target);
  var targetPosition = target.getBoundingClientRect().top;
  var startPosition = window.pageYOffset;
  var distance = targetPosition - startPosition;
  var startTime = null;

  function animation(currentTime) {
    if (startTime === null) startTime = currentTime;
    var timeElapsed = currentTime - startTime;
    var run = ease(timeElapsed, startPosition, distance, duration);
    window.scrollTo(0, run);
    if (timeElapsed < duration) requestAnimationFrame(animation);
  }

  function ease(t, b, c, d) {
    t /= d / 2;
    if (t < 1) return (c / 2) * t * t + b;
    t--;
    return (-c / 2) * (t * (t - 2) - 1) + b;
  }

  requestAnimationFrame(animation);
}

var section_home = document.querySelector("#home-link");
section_home.addEventListener("click", function () {
  smoothScroll("#home", 1000);
});

var section_about = document.querySelector("#about-link");
section_about.addEventListener("click", function () {
  smoothScroll("#about", 1000);
});

var section_services = document.querySelector("#services-link");
section_services.addEventListener("click", function () {
  smoothScroll("#services", 1000);
}); */
